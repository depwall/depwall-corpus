// Realistic benign build.rs: cc invocation + cargo env vars, no network.
use std::env;
use std::path::PathBuf;

fn main() {
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
    cc::Build::new().file("src/shim.c").out_dir(&out_dir).compile("shim");
    println!("cargo:rustc-link-search=native={}", out_dir.display());
    println!("cargo:rerun-if-changed=src/shim.c");
}
