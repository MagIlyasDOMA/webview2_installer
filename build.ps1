$targets = @(
    "x86_64-pc-windows-msvc",
    "i686-pc-windows-msvc",
    "aarch64-pc-windows-msvc"
)

foreach ($target in $targets) {
    Write-Host "Building for $target..." -ForegroundColor Green
    cargo build --release --target $target

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Successfully built for $target" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to build for $target" -ForegroundColor Red
    }
}

Write-Host "`nBuild complete!" -ForegroundColor Cyan
Write-Host "Output locations:" -ForegroundColor Yellow
Write-Host "  x64:  target\x86_64-pc-windows-msvc\release\webview2_installer.dll"
Write-Host "  x86:  target\i686-pc-windows-msvc\release\webview2_installer.dll"
Write-Host "  ARM64: target\aarch64-pc-windows-msvc\release\webview2_installer.dll"

New-Item -ItemType Directory -Force -Path "webview2_installer/dlls/win32"
New-Item -ItemType Directory -Force -Path "webview2_installer/dlls/win_amd64"
New-Item -ItemType Directory -Force -Path "webview2_installer/dlls/win_arm64"

Copy-Item -Path "target/i686-pc-windows-msvc/release/webview2_installer.dll" -Destination "webview2_installer/dlls/win32"
Copy-Item -Path "target/x86_64-pc-windows-msvc/release/webview2_installer.dll" -Destination "webview2_installer/dlls/win_amd64"
Copy-Item -Path "target/aarch64-pc-windows-msvc/release/webview2_installer.dll" -Destination "webview2_installer/dlls/win_arm64"
