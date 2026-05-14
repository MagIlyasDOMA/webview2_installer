use std::io::{Write, Read};
use std::path::PathBuf;
use std::process::Command;
use indicatif::{ProgressBar, ProgressStyle};
use reqwest::blocking::Client;
use tempfile::NamedTempFile;
use winreg::enums::{HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE};
use winreg::RegKey;
use pyo3::prelude::*;

const WEBVIEW2_BOOTSTRAPPER_URL: &str = "https://go.microsoft.com/fwlink/p/?LinkId=2124703";
const WEBVIEW2_CLSID: &str = "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}";

fn _is_webview2_installed() -> bool {
    let registry_paths = [
        format!(r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{}", WEBVIEW2_CLSID),
        format!(r"Software\Microsoft\EdgeUpdate\Clients\{}", WEBVIEW2_CLSID),
    ];

    // Check in HKLM
    for path in &registry_paths {
        if let Ok(_key) = RegKey::predef(HKEY_LOCAL_MACHINE).open_subkey(path) {
            return true;
        }
    }

    // Check in HKCU
    for path in &registry_paths {
        if let Ok(_key) = RegKey::predef(HKEY_CURRENT_USER).open_subkey(path) {
            return true;
        }
    }

    false
}

fn _download_file_to_temp(verbose: bool) -> Result<PathBuf, Box<dyn std::error::Error>> {
    let client = Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .build()?;

    let response = client.get(WEBVIEW2_BOOTSTRAPPER_URL).send()?;
    let total_size = response.content_length().unwrap_or(0);

    let mut temp_file = NamedTempFile::with_suffix(".exe")?;
    let temp_path = temp_file.path().to_path_buf();

    let mut reader = response;

    if verbose && total_size > 0 {
        let pb = ProgressBar::new(total_size);
        pb.set_style(ProgressStyle::default_bar()
            .template("{msg}: {percent}% {bytes}/{total_bytes} [{bar:40}] {bytes_per_sec}")
            .unwrap()
            .progress_chars("=> "));
        pb.set_message("Downloading Evergreen Bootstrapper");

        let mut written = 0u64;
        let mut buffer = [0u8; 8192];

        loop {
            let bytes_read = reader.read(&mut buffer)?;
            if bytes_read == 0 { break; }
            temp_file.write_all(&buffer[..bytes_read])?;
            written += bytes_read as u64;
            pb.set_position(written);
        }

        pb.finish_with_message("Download complete");
    } else {
        let mut buffer = Vec::new();
        reader.read_to_end(&mut buffer)?;
        temp_file.write_all(&buffer)?;
    }

    temp_file.flush()?;
    Ok(temp_path)
}

fn _download_and_install_webview2(verbose: bool) -> Result<bool, Box<dyn std::error::Error>> {
    let bootstrapper_path = _download_file_to_temp(verbose)?;

    if verbose {
        println!("Download complete. Starting installation (silent mode)...");
    }

    // Run the installation in silent mode
    let output = Command::new(&bootstrapper_path)
        .args(["/silent", "/install"])
        .output();

    // Try to delete the temporary file
    let _ = std::fs::remove_file(&bootstrapper_path);

    match output {
        Ok(status) if status.status.success() => {
            if verbose {
                println!("WebView2 installation started successfully.");
            }
            Ok(true)
        }
        Ok(status) => {
            if verbose {
                eprintln!("Error running the installer: {:?}", status);
            }
            Ok(false)
        }
        Err(e) => {
            if verbose {
                eprintln!("Error running the installer: {}", e);
            }
            Ok(false)
        }
    }
}

/// Checks if WebView2 Evergreen Runtime is installed
#[unsafe(no_mangle)]
pub extern "C" fn is_webview2_installed() -> bool {
    _is_webview2_installed()
}

/// Downloads and runs the WebView2 installer in silent mode
/// Returns: 1 if successful, 0 if failed
#[unsafe(no_mangle)]
pub extern "C" fn download_and_install_webview2() -> i32 {
    match _download_and_install_webview2(false) {
        Ok(true) => 1,
        Ok(false) => 0,
        Err(_) => 0,
    }
}

/// Downloads and runs the WebView2 installer in silent mode with verbose
/// Returns: 1 if successful, 0 if failed
#[unsafe(no_mangle)]
pub extern "C" fn download_and_install_webview2_verbose() -> i32 {
    match _download_and_install_webview2(true) {
        Ok(true) => 1,
        Ok(false) => 0,
        Err(_) => 0,
    }
}

/// Checks if WebView2 is installed, and if not, installs it
///
/// Returns:
/// - 0 if already installed
/// - 1 if installation was started successfully
/// - -1 if installation failed
#[unsafe(no_mangle)]
pub extern "C" fn install_webview2_if_not_installed() -> i32 {
    _install_webview2_if_not_installed(false)}

/// Checks if WebView2 is installed, and if not, installs it with verbose
///
/// Returns:
/// - 0 if already installed
/// - 1 if installation was started successfully
/// - -1 if installation failed
#[unsafe(no_mangle)]
pub extern "C" fn install_webview2_if_not_installed_verbose() -> i32 {
    _install_webview2_if_not_installed(true)}

fn _install_webview2_if_not_installed(verbose: bool) -> i32 {
    if _is_webview2_installed() {
        if verbose {println!("WebView2 is already installed");}
        0
    } else {
        if verbose {println!("WebView2 not found. Downloading installer...");}
        match _download_and_install_webview2(verbose) {
            Ok(_result) => 1,
            Err(e) => {
                if verbose {eprintln!("Error: {}", e);}
                -1
            }
        }
    }
}


// In dev

#[pyfunction]
#[pyo3(name="is_webview2_installed")]
fn is_webview2_installed_python() -> bool {_is_webview2_installed()}

#[pyfunction]
#[pyo3(name="download_and_install_webview2", signature=(verbose=false))]
fn download_and_install_webview2_python(verbose: bool) -> bool {
    match _download_and_install_webview2(verbose) {
        Ok(true) => true,
        Ok(false) => false,
        Err(_) => false,
    }
}

#[pyfunction]
#[pyo3(name="install_webview2_if_not_installed", signature=(verbose=false))]
fn install_webview2_if_not_installed_python(verbose: bool) -> i32 {
    _install_webview2_if_not_installed(verbose)}

#[pymodule]
fn webview2_installer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_webview2_installed_python, m)?)?;
    m.add_function(wrap_pyfunction!(download_and_install_webview2_python, m)?)?;
    m.add_function(wrap_pyfunction!(install_webview2_if_not_installed_python, m)?)?;
    Ok(())
}
