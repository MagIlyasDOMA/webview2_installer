from typing import Literal


def is_webview2_installed() -> bool:
    """
    Checks if the WebView2 Evergreen Runtime is installed by searching
    for the corresponding CLSID in the Windows registry.
    """


def download_and_install_webview2(verbose: bool = False) -> bool:
    """
    Downloads and runs the WebView2 installer in silent mode.

    Returns:
        True if installation was started successfully
    """


def install_webview2_if_not_installed(verbose: bool = False) -> Literal[-1, 0, 1]:
    """
    Checks if WebView2 is installed, and if not, installs it

    Returns:
        0 if webview2 already installed
        1 if installation was started successfully
        -1 if installation was failed
    """

