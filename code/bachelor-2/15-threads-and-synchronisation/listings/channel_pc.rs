// channel_pc.rs: producers send into a bounded channel; one consumer receives.
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::sync_channel::<u64>(8); // at most 8 messages in flight
    for _ in 0..2 {
        let tx = tx.clone();
        thread::spawn(move || {
            for k in 1..=100_000 {
                tx.send(k).unwrap();             // waits while the channel is full
            }
        });                                      // tx dropped: one sender fewer
    }
    drop(tx);                                    // keep no sender here, or recv never ends
    let sum: u64 = rx.iter().sum();              // ends when every sender is dropped
    println!("sum received: {sum}");
}
