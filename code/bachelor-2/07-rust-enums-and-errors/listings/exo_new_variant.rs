// capture: exit
// exo_new_variant.rs: the library adds a loan state; the fine function was written before.
#[allow(dead_code)]
enum LoanState {
    Out { days: u32 },
    Returned,
    Lost, // the new variant
}

fn fine_cents(s: &LoanState) -> u32 {
    match s {
        LoanState::Out { days } if *days > 21 => 10 * (days - 21),
        LoanState::Out { .. } => 0,
        LoanState::Returned => 0,
    }
}

fn main() {
    println!("{}", fine_cents(&LoanState::Out { days: 30 }));
}
