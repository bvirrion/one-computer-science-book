// client.rs: one connection, one request line, one reply line.
use std::io::{self, BufRead, BufReader, Write};
use std::net::TcpStream;
use std::thread;
use std::time::Duration;

pub struct Client {
    reader: BufReader<TcpStream>,
    writer: TcpStream,
}

impl Client {
    /// Connect, retrying for a second while the server starts.
    pub fn connect(addr: &str) -> io::Result<Client> {
        let mut tries = 0;
        let stream = loop {
            match TcpStream::connect(addr) {
                Ok(s) => break s,
                Err(_) if tries < 100 => tries += 1,
                Err(e) => return Err(e),
            }
            thread::sleep(Duration::from_millis(10));
        };
        stream.set_nodelay(true)?;
        Ok(Client { reader: BufReader::new(stream.try_clone()?), writer: stream })
    }

    pub fn send(&mut self, line: &str) -> io::Result<()> {
        self.writer.write_all(format!("{line}\n").as_bytes())
    }

    /// Bytes as they are, for the tests that split a request.
    pub fn write_raw(&mut self, bytes: &[u8]) -> io::Result<()> {
        self.writer.write_all(bytes)
    }

    pub fn receive(&mut self) -> io::Result<String> {
        let mut reply = String::new();
        self.reader.read_line(&mut reply)?;
        Ok(reply.trim_end().to_string())
    }

    pub fn request(&mut self, line: &str) -> io::Result<String> {
        self.send(line)?;
        self.receive()
    }
}
