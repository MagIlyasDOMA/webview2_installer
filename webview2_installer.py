import winreg, requests, subprocess, tempfile, os
from typing import Optional
from tqdm import tqdm

__all__ = ['WEBVIEW2_BOOTSTRAPPER_URL', 'is_webview2_installed',
           'download_and_install_webview2', 'install_webview2_if_not_installed']

WEBVIEW2_BOOTSTRAPPER_URL = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"


if os.name != 'nt': raise OSError("Windows is required")


def _echo(verbose: bool, *values, sep: str = ' ', end: str = '\n'):
    if verbose: print(*values, sep=sep, end=end)


def is_webview2_installed() -> bool:
    """
    Checks if the WebView2 Evergreen Runtime is installed by searching
    for the corresponding CLSID in the Windows registry.
    """
    # CLSID for WebView2 Evergreen Runtime
    clsid = '{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}'
    # Registry paths to check
    registry_paths = [
        r'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\\' + clsid,  # For 32-bit on 64-bit system
        r'Software\Microsoft\EdgeUpdate\Clients\\' + clsid,  # Normal path
    ]
    # Check in HKEY_LOCAL_MACHINE
    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ):
                return True
        except FileNotFoundError:
            pass
    # Check in HKEY_CURRENT_USER (less common, but possible)
    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ):
                return True
        except FileNotFoundError:
            pass
    return False


def _download_file_to_temp(verbose: bool = True):
    response = requests.get(WEBVIEW2_BOOTSTRAPPER_URL, stream=True)
    with tempfile.NamedTemporaryFile('wb', delete=False, suffix='.exe') as tmp_file:
        if verbose:
            with tqdm(
                desc="Downloading Evergreen Bootstrapper",
                total=int(response.headers.get('content-length', 0)),
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as progressbar:
                for data in response.iter_content(chunk_size=1024):
                    progressbar.update(len(data))
                    tmp_file.write(data)
        else: tmp_file.write(response.content)
        return tmp_file.name


def download_and_install_webview2(verbose: bool = True) -> bool:
    """
    Downloads and runs the WebView2 installer in silent mode.

    Returns:
        True if installation was started successfully
    """

    bootstrapper = _download_file_to_temp(verbose)
    print("Download complete. Starting installation (silent mode)...")

    # Run the installation in silent mode
    # /silent - no UI, /install - installation mode
    try:
        subprocess.run([bootstrapper, '/silent', '/install'], check=True)
        _echo(verbose, "WebView2 installation started successfully.")
        return True
    except subprocess.CalledProcessError as e:
        _echo(verbose, f"Error running the installer: {e}")
        return False
    finally:
        # Delete the temporary file (not immediately, as the installer may still be using it)
        try: os.unlink(bootstrapper)
        except PermissionError: pass


def install_webview2_if_not_installed(verbose: bool = False) -> Optional[bool]:
    """
    Checks if WebView2 is installed, and if not, installs it
    """
    if is_webview2_installed():
        _echo(verbose, "WebView2 is already installed")
        return None
    else:
        _echo(verbose, "WebView2 not found. Downloading installer...")
        return download_and_install_webview2(verbose)
