import argparse, subprocess, sys, os, tomllib
from datetime import date
from pathlib import Path
from shutil import copy2
from typing import Literal, TypedDict, Union, List

BuildMode = Literal['release', 'debug']

targets = dict(
    x64="x86_64-pc-windows-msvc",
    x86="i686-pc-windows-msvc",
    arm64="aarch64-pc-windows-msvc"
)


class VersionMetadata(TypedDict):
    version: str
    company: str
    copyright: str
    description: str
    product: str
    internal_name: str
    original_filename: str


def get_toml_metadata(arch: str = '') -> VersionMetadata:
    with open('Cargo.toml', 'rb') as file: raw_data = tomllib.load(file)
    current_year = date.today().year

    project_data = raw_data['package']
    name = project_data['name']
    author = project_data['authors'][0]
    copyright = f"Copyright (c) {2026 if current_year == 2026 else f'2026-{current_year}'} {author}"
    description = project_data['description']

    version: list = project_data['version'].split('.')

    if len(version) < 4: version.extend(['0'] * (4 - len(version)))
    elif len(version) > 4: raise ValueError("Incorrect version")

    return dict(
        version='.'.join(version),
        company=author,
        copyright=copyright,
        description=description,
        product=name,
        internal_name= name,
        original_filename=format_dll_filename(arch),
    )


def set_metadata(dll_path: Path, metadata: VersionMetadata, *, argv_only: bool = False
                 ) -> Union[List[str], subprocess.CompletedProcess]:
    argv = [
        'rcedit', str(dll_path),
        '--set-version-string', 'CompanyName', metadata['company'],
        '--set-version-string', 'LegalCopyright', metadata['copyright'],
        '--set-version-string', 'FileDescription', metadata['description'],
        '--set-version-string', 'InternalName', metadata['internal_name'],
        '--set-version-string', 'OriginalFilename', metadata['original_filename'],
        '--set-version-string', 'ProductName', metadata['product'],
        '--set-file-version', metadata['version'],
        '--set-product-version', metadata['version'],
    ]
    return subprocess.run(argv, text=True) if not argv_only else argv


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

    package_dir = cwd / 'webview2_installer'

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
            set_metadata(dll_path, get_toml_metadata(arch))
            dist_path = dist_dir / format_dll_filename(arch)
            package_path = package_dir / format_dll_filename(arch)
            copy2(dll_path, dist_path)
            copy2(dll_path, package_path)
            print('DLL paths:', dll_path, dist_path, package_path, sep='\n')
        else: print("✗ Failed to build dll for", full_name, file=sys.stderr)
        print()


if __name__ == '__main__': main()
