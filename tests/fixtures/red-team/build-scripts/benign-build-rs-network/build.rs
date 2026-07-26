// Realistic benign build.rs that fetches a prebuilt artifact and uses cargo
// env vars — must NOT trip the deterministic signal.
use std::env;

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();
    let _resp = ureq::get("https://artifacts.example/libfoo.a").call();
    println!("cargo:rustc-link-search=native={out_dir}");
}
