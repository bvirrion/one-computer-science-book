// client.rs: send one command to a node, follow redirects to the leader.
use crate::node::address;
use crate::protocol::{parse_reply, Command, Reply};
use std::io::{BufRead, BufReader, Write};
use std::net::TcpStream;
use std::time::Duration;

/// One request to one node: its reply, or the error that prevented it.
pub fn ask(base: u16, node: u32, command: &Command) -> std::io::Result<Reply> {
    let mut stream = TcpStream::connect(address(base, node))?;
    stream.set_read_timeout(Some(Duration::from_secs(2)))?;
    writeln!(stream, "{command}")?;
    let mut line = String::new();
    BufReader::new(stream).read_line(&mut line)?;
    parse_reply(line.trim_end()).map_err(std::io::Error::other)
}

/// Asks `node`, then the node it redirects to, at most `hops` times; returns every
/// (node, reply) on the way, the last one being the answer.
pub fn ask_leader(
    base: u16,
    mut node: u32,
    command: &Command,
    hops: usize,
) -> Vec<(u32, Result<Reply, String>)> {
    let mut trail = Vec::new();
    for _ in 0..hops {
        let reply = ask(base, node, command).map_err(|e| e.to_string());
        let next = match &reply {
            Ok(Reply::Redirect(n)) if *n != 0 => Some(*n),
            _ => None,
        };
        trail.push((node, reply));
        match next {
            Some(n) => node = n,
            None => break,
        }
    }
    trail
}
