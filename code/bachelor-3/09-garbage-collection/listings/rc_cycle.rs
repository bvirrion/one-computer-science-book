// rc_cycle.rs -- two Rc pointers in a cycle are never dropped; a Weak back pointer breaks it.
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Member {
    name: &'static str,
    friend: RefCell<Option<Rc<Member>>>, // strong: keeps the friend alive
    sponsor: RefCell<Weak<Member>>,      // weak: does not
}

impl Drop for Member {
    fn drop(&mut self) {
        println!("  drop {}", self.name);
    }
}

fn member(name: &'static str) -> Rc<Member> {
    Rc::new(Member { name, friend: RefCell::new(None), sponsor: RefCell::new(Weak::new()) })
}

fn main() {
    println!("strong cycle:");
    {
        let (ann, bob) = (member("Ann"), member("Bob"));
        *ann.friend.borrow_mut() = Some(Rc::clone(&bob));
        *bob.friend.borrow_mut() = Some(Rc::clone(&ann));
        println!("  counts {} {}", Rc::strong_count(&ann), Rc::strong_count(&bob));
    } // the two locals go; each count falls to 1, never to 0
    println!("  (end of scope: nothing dropped)");

    println!("weak back pointer:");
    let cleo = member("Cleo");
    {
        let dan = member("Dan");
        *cleo.friend.borrow_mut() = Some(Rc::clone(&dan));
        *dan.sponsor.borrow_mut() = Rc::downgrade(&cleo);
        println!("  counts {} {}, weak {}", Rc::strong_count(&cleo), Rc::strong_count(&dan),
                 Rc::weak_count(&cleo));
    }
    let alive = cleo.friend.borrow().as_ref().map(|d| d.sponsor.borrow().upgrade().is_some());
    println!("  Dan's sponsor still there: {:?}", alive);
    drop(cleo); // Cleo's count reaches 0: Cleo dropped, then Dan
    println!("end of main");
}
