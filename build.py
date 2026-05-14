import argparse, subprocess, sys, os
from bidict import bidict
from pathlib import Path
from shutil import copy2
from typing import Literal

BuildMode = Literal['release', 'debug']

targets = bidict(
    x64="x86_64-pc-windows-msvc",
    x86="i686-pc-windows-msvc",
    arm64="aarch64-pc-windows-msvc"
)


def format_dll_filename(arch: str = '') -> str:
    arch = '_' + arch if arch else ''
    return f'webview2_installer{arch}.dll'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_const', const='debug',
                        default='release', help='debug mode', dest='build_mode')
    parser.add_argument('--dynamic', '-s', action='store_false',
                        help='use dynamic linking', dest='static')

    args = parser.parse_args()
    build_mode = args.build_mode
    cwd = Path.cwd()

    dist_dir = cwd / 'dist'
    dist_dir.mkdir(exist_ok=True)


    if args.static: os.environ['RUSTFLAGS'] = '-C target-feature=+crt-static'
    else: print("Warning: This uses dynamic linking and requires Visual C++ Redistributable "
                "to be installed on the user's PC.", file=sys.stderr)

    for arch, target in targets.items():
        full_name = f'{arch} ({target})'
        print('Building dll for', full_name)
        argv = ['cargo', 'build']
        if args.build_mode == 'release': argv.append('--release')
        argv.extend(['--target', target])
        dll_process = subprocess.run(argv, text=True)
        if dll_process.returncode == 0:
            print('✓ Successfully built dll for', full_name)
            dll_path = cwd / 'target' / target / build_mode / format_dll_filename()
            dist_path = dist_dir / format_dll_filename(arch)
            copy2(dll_path, dist_path)
            print('DLL paths:', dll_path, dist_path, sep='\n')
        else: print("✗ Failed to build dll for", full_name, file=sys.stderr)
        print()


if __name__ == '__main__': main()
