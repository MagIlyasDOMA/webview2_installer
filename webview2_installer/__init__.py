import platform, sys
from pathlib import Path
from typing_extensions import Literal

__all__ = ['is_webview2_installed', 'install_webview2_if_not_installed',
           'download_and_install_webview2', '__version__']
__version__ = '1.0.0'

if platform.system() != "Windows": raise OSError("This script only works on Windows")

_bits = sys.maxsize.bit_length() + 1
_machine = platform.machine().lower()
_is_arm = _machine in ('arm64', 'aarch64')
_is_x86 = _machine in ('x86_64', 'i386', 'i686', 'amd64', 'x86')

if _is_arm and _bits == 64: _arch = 'arm64'
elif _is_x86 and _bits == 64: _arch = 'x64'
elif _is_x86 and _bits == 32: _arch = 'x86'
else: raise OSError("Unsupported architecture")

_dll_path = Path(__file__).parent / f'webview2_installer_{_arch}.dll'

if not _dll_path.is_file(): raise FileNotFoundError(f'{_dll_path} does not exist')

import ctypes

DLL = ctypes.CDLL(str(_dll_path))


def is_webview2_installed() -> bool:
    """Checks if WebView2 Evergreen Runtime is installed"""
    return DLL.is_webview2_installed()

def download_and_install_webview2(verbose: bool = False) -> bool:
    """
    Downloads and runs the WebView2 installer in silent mode

    Returns:

    - ``True`` if successful
    - ``False`` if failed
    """
    return DLL.download_and_install_webview2_verbose() if verbose \
        else DLL.download_and_install_webview2()


def install_webview2_if_not_installed(verbose: bool = False) -> Literal[0, 1, -1]:
    """
    Checks if WebView2 is installed, and if not, installs it

    Returns:

    - ``0`` if already installed
    - ``1`` if installation was started successfully
    - ``-1`` if installation failed
    """
    return DLL.install_webview2_if_not_installed_verbose() if verbose \
        else DLL.install_webview2_if_not_installed()
