// Shared by the chapter's tests: compile Moor, run it on rv and on the
// interpreter of chapter 4.
#![allow(dead_code)]
use std::process::Command;

pub struct RvRun {
    pub output: String,
    pub exit: i32, // -1 for a fault or the step limit
    pub fault: String,
    pub instructions: u64,
}

const SCRIPT: &str = r#"
import sys
from rv import Machine, RVFault
m = Machine(open(sys.argv[1]).read(), inputs=[int(x) for x in sys.argv[3:]])
try:
    code, fault = m.run(max_steps=int(sys.argv[2])), ""
except RVFault as e:
    code, fault = -1, e.msg
sys.stdout.write(f"{code}\n{m.stats['instructions']}\n{fault}\n{m.output_text}")
"#;

pub fn rv_run(asm: &str, inputs: &[i32], max_steps: u64) -> RvRun {
    let dir = std::env::temp_dir().join(format!("moorc-test-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let file = dir.join(format!("p{}.S", COUNTER.fetch_add(1, std::sync::atomic::Ordering::Relaxed)));
    std::fs::write(&file, asm).unwrap();
    let mut args = vec!["-c".to_string(), SCRIPT.to_string(), file.display().to_string(),
                        max_steps.to_string()];
    args.extend(inputs.iter().map(|x| x.to_string()));
    let out = Command::new("python3").args(&args)
        .env("PYTHONPATH", std::fs::canonicalize("../../../shared/rv").unwrap())
        .output().expect("python3");
    std::fs::remove_file(&file).unwrap();
    let text = String::from_utf8(out.stdout).unwrap();
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
    let mut parts = text.splitn(4, '\n');
    RvRun {
        exit: parts.next().unwrap().parse().unwrap(),
        instructions: parts.next().unwrap().parse().unwrap(),
        fault: parts.next().unwrap().to_string(),
        output: parts.next().unwrap_or("").to_string(),
    }
}

static COUNTER: std::sync::atomic::AtomicUsize = std::sync::atomic::AtomicUsize::new(0);
