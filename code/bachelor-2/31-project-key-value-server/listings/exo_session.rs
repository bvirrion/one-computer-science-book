// exo_session.rs (exercise 1): the replies to a scripted session, without the network.
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod store;

use protocol::{parse, Reply};
use store::{Map, Sharded, Store};

fn main() {
    let store = Sharded::new(16, Map::new());
    let session = [
        "SET a 1", "SET b 2", "SET a 3", "GET a", "DEL b", "DEL b", "GET b", "COUNT",
        "SET c 4 5", "SET  c  4", "GET c", "DEL", "COUNT",
    ];
    for line in session {
        let reply = match parse(line) {
            Ok(cmd) => store.apply(&cmd, None),
            Err(reason) => Reply::Err(reason),
        };
        println!("> {line:<12} < {reply}");
    }
}
