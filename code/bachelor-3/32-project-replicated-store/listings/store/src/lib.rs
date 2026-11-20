//! A replicated key-value store: the protocol, a write-ahead log, Raft as a pure state
//! machine, a deterministic simulator for it, the networked node, a client and a
//! linearisability checker. Standard library only.
pub mod client;
pub mod lincheck;
pub mod node;
pub mod protocol;
pub mod raft;
pub mod sim;
pub mod wal;
