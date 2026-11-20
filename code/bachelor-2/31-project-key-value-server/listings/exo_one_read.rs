// exo_one_read.rs (exercise 2): a server that takes one read() for one request.
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;
use std::time::Duration;

fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:44318")?;
    let server = thread::spawn(move || -> std::io::Result<()> {
        let (mut stream, _) = listener.accept()?;
        let mut buf = [0u8; 1024];
        loop {
            let n = stream.read(&mut buf)?; // the bug: n bytes are not one line
            if n == 0 {
                return Ok(());
            }
            println!("the server got one request: {:?}", String::from_utf8_lossy(&buf[..n]));
        }
    });
    let mut client = TcpStream::connect("127.0.0.1:44318")?;
    client.write_all(b"SET a 1\nGET a\n")?; // two requests in one write
    thread::sleep(Duration::from_millis(100));
    client.write_all(b"GE")?; // one request in two writes
    thread::sleep(Duration::from_millis(100));
    client.write_all(b"T a\n")?;
    thread::sleep(Duration::from_millis(100));
    drop(client);
    server.join().unwrap()
}
