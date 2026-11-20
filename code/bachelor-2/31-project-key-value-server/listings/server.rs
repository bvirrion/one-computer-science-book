// server.rs: one connection's loop, then three ways to serve many connections.
use crate::log::Log;
use crate::protocol::{parse, Command, Reply, MAX_LINE};
use crate::store::Store;
use std::io::{self, BufRead, BufReader, BufWriter, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

pub struct Shared {
    pub store: Box<dyn Store>,
    pub log: Option<Mutex<Log>>,
}

/// Read lines until QUIT or end of stream; answer each with one line.
pub fn handle(stream: TcpStream, shared: &Shared) -> io::Result<()> {
    let mut reader = BufReader::new(stream.try_clone()?);
    let mut writer = BufWriter::new(stream);
    let mut line = Vec::new();
    loop {
        line.clear();
        let limit = MAX_LINE as u64 + 2; // the line, "\r" and "\n"
        let n = (&mut reader).take(limit).read_until(b'\n', &mut line)?;
        if n == 0 {
            return Ok(()); // the client closed the connection
        }
        if line.last() != Some(&b'\n') {
            let reason = if n as u64 == limit { "line too long" } else { "no newline" };
            writeln!(writer, "{}", Reply::Err(reason.to_string()))?;
            return writer.flush(); // the stream cannot be resynchronised: close it
        }
        let text = String::from_utf8_lossy(&line);
        let cmd = parse(text.trim_end_matches(['\r', '\n']));
        let reply = match &cmd {
            Ok(cmd) => shared.store.apply(cmd, shared.log.as_ref()),
            Err(reason) => Reply::Err(reason.clone()),
        };
        writeln!(writer, "{reply}")?;
        if cmd == Ok(Command::Quit) {
            return writer.flush();
        }
        if reader.buffer().is_empty() {
            writer.flush()?; // no request waiting: send the replies now
        }
    }
}

/// M2: one connection at a time; the next client waits for the previous one.
pub fn serve_one_at_a_time(listener: TcpListener, shared: Arc<Shared>) -> io::Result<()> {
    for stream in listener.incoming() {
        let _ = handle(stream?, &shared);
    }
    Ok(())
}

/// M3: a new thread for every connection.
pub fn serve_thread_per_connection(listener: TcpListener, shared: Arc<Shared>)
    -> io::Result<()> {
    for stream in listener.incoming() {
        let (stream, shared) = (stream?, Arc::clone(&shared));
        thread::spawn(move || handle(stream, &shared));
    }
    Ok(())
}

/// M3: a fixed pool of workers takes the connections from one queue.
pub fn serve_pool(listener: TcpListener, shared: Arc<Shared>, workers: usize)
    -> io::Result<()> {
    let (queue, jobs) = mpsc::channel::<TcpStream>();
    let jobs = Arc::new(Mutex::new(jobs));
    for _ in 0..workers {
        let (jobs, shared) = (Arc::clone(&jobs), Arc::clone(&shared));
        thread::spawn(move || loop {
            let next = jobs.lock().unwrap().recv(); // the guard is dropped here
            match next {
                Ok(stream) => {
                    let _ = handle(stream, &shared);
                }
                Err(_) => return, // the queue is closed
            }
        });
    }
    for stream in listener.incoming() {
        queue.send(stream?).expect("a worker is alive");
    }
    Ok(())
}
