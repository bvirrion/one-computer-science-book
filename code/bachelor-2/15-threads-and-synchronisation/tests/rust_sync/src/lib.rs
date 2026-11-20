//! Tests of chapter 15: the writer-preferring readers-writers lock of exercise 9.
#[path = "../../../exercises/rwlock.rs"]
pub mod rwlock;

#[cfg(test)]
mod tests {
    use super::rwlock::RwLockW;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::{mpsc, Arc};
    use std::thread;
    use std::time::Duration;

    #[test]
    fn readers_share_writers_exclude() {
        let lock = Arc::new(RwLockW::default());
        let inside = Arc::new(AtomicUsize::new(0)); // readers + 1000 * writers inside
        let mut handles = Vec::new();
        for t in 0..8 {
            let (lock, inside) = (Arc::clone(&lock), Arc::clone(&inside));
            handles.push(thread::spawn(move || {
                for _ in 0..2000 {
                    if t % 4 == 0 {
                        lock.write_lock();
                        assert_eq!(inside.fetch_add(1000, Ordering::SeqCst), 0);
                        inside.fetch_sub(1000, Ordering::SeqCst);
                        lock.write_unlock();
                    } else {
                        lock.read_lock();
                        assert!(inside.fetch_add(1, Ordering::SeqCst) < 1000);
                        inside.fetch_sub(1, Ordering::SeqCst);
                        lock.read_unlock();
                    }
                }
            }));
        }
        for h in handles {
            h.join().unwrap();
        }
    }

    #[test]
    fn a_waiting_writer_blocks_new_readers() {
        let lock = Arc::new(RwLockW::default());
        lock.read_lock(); // a reader is inside
        let (tx, rx) = mpsc::channel();
        let w = {
            let (lock, tx) = (Arc::clone(&lock), tx.clone());
            thread::spawn(move || {
                lock.write_lock();
                tx.send("writer").unwrap();
                lock.write_unlock();
            })
        };
        thread::sleep(Duration::from_millis(100)); // the writer is now waiting
        let r = {
            let lock = Arc::clone(&lock);
            thread::spawn(move || {
                lock.read_lock();
                tx.send("reader").unwrap();
                lock.read_unlock();
            })
        };
        thread::sleep(Duration::from_millis(100));
        assert!(rx.try_recv().is_err()); // neither has entered
        lock.read_unlock(); // the first reader leaves
        assert_eq!(rx.recv().unwrap(), "writer");
        assert_eq!(rx.recv().unwrap(), "reader");
        w.join().unwrap();
        r.join().unwrap();
    }
}
