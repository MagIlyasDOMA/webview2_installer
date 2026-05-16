<a name="doc_en"></a>
# WebView2 Installer
#### [Документация на русском](#doc_ru)

A library for checking and automatically installing the WebView2 Evergreen Runtime on Windows.

Supported architectures: **x86**, **x64**, **ARM64**.

## 📦 Distribution Methods

### 1. Python Package (wheel)
```bash
pip install webview2-installer
```

### 2. DLL Library
Pre-built DLL files for integration into C/C++ projects:
- `webview2_installer_x86.dll` — for 32-bit Windows
- `webview2_installer_x64.dll` — for 64-bit Windows
- `webview2_installer_arm64.dll` — for ARM64 Windows

## 🚀 Usage in Python
```python
from webview2_installer import (
    is_webview2_installed,
    install_webview2_if_not_installed,
    download_and_install_webview2
)

# Check if WebView2 is installed
if is_webview2_installed():
    print("✅ WebView2 is already installed")
else:
    print("❌ WebView2 not found")

# Install if not installed (recommended method)
result = install_webview2_if_not_installed(verbose=True)
if result == 0:
    print("✅ WebView2 is already installed")
elif result == 1:
    print("✅ WebView2 installation started")
else:
    print("❌ WebView2 installation failed")

# Force download and installation
success = download_and_install_webview2(verbose=True)
if success:
    print("✅ Installation successfully started")
```

### Return values for install_webview2_if_not_installed()
| Value | Description                       |
|-------|-----------------------------------|
| 0     | WebView2 is already installed     |
| 1     | Installation successfully started |
| -1    | Installation failed               |

## 🔧 Using the DLL in C/C++
### Function Signatures

```c
// Checks if WebView2 is installed
bool is_webview2_installed(void);

// Downloads and installs WebView2 (silent installation)
bool download_and_install_webview2(void);

// With verbose output
bool download_and_install_webview2_verbose(void);

// Installs if not installed (0 = already installed, 1 = success, -1 = error)
int install_webview2_if_not_installed(void);

// With verbose output
int install_webview2_if_not_installed_verbose(void);
```

### C Example
```c
#include <windows.h>
#include <stdio.h>

typedef bool (*is_installed_fn)(void);
typedef int (*install_if_needed_fn)(void);

int main() {
    HMODULE dll = LoadLibrary("webview2_installer_x64.dll");
    if (!dll) return 1;
    
    is_installed_fn is_installed = (is_installed_fn)GetProcAddress(dll, "is_webview2_installed");
    install_if_needed_fn install_if_needed = (install_if_needed_fn)GetProcAddress(dll, "install_webview2_if_not_installed");
    
    if (is_installed && install_if_needed) {
        int result = install_if_needed();
        printf("Result: %d\n", result);
    }
    
    FreeLibrary(dll);
    return 0;
}
```

## 🛠️ Development and Building
### Requirements
- Rust (2021 edition)
- Python 3.8+
- Visual Studio Build Tools (Windows)
- cargo, rustup
- rcedit

### Building the DLL
```shell
# Build release versions for all architectures
python build_dll.py

# Build debug versions
python build_dll.py --debug

# Dynamic linking (requires VC++ Redist)
python build_dll.py --dynamic
```

### Building the Python Package
```shell
# Install development dependencies
pip install -e ".[dev]"

# Build the package
python -m build

# Or via devscript
devscript build_wheel
```

### Cleaning Build Files
```shell
devscript clean
```

## 📋 System Requirements
- **OS:** Windows 7 / 8 / 10 / 11
- **Architectures:** x86, x64, ARM64
- **Python: 3.8+** (for Python package)
- **Internet:** required for downloading the installer

## 🔍 How It Works
- **Installation Check:** Checks for WebView2 registry keys in Windows registry
- **Download:** Downloads the official Microsoft installer
- **Installation:** Runs in silent mode (/silent /install)
- **Cleanup:** Temporary files are automatically deleted

## 📄 License
MIT License

## 🤝 Contributing
PRs and Issues are welcome! Please ensure changes work on all target architectures.

## ⚠️ Known Limitations
- Windows only (target platform)
- Synchronous installation — you need to wait for WebView2 to finish installing

---

<a href="doc_ru"></a>
# WebView2 Installer
#### [Documentation in English](#doc_en)

Библиотека для проверки установки и автоматической установки WebView2 Evergreen Runtime на Windows.

Поддерживает архитектуры: **x86**, **x64**, **ARM64**.

## 📦 Способы распространения

### 1. Python пакет (wheel)
```bash
pip install webview2-installer
```

### 2. DLL библиотека
Готовые DLL файлы для интеграции в C/C++ проекты:
- `webview2_installer_x86.dll` — для 32-bit Windows
- `webview2_installer_x64.dll` — для 64-bit Windows
- `webview2_installer_arm64.dll` — для ARM64 Windows

## 🚀 Использование в Python
```python
from webview2_installer import (
    is_webview2_installed,
    install_webview2_if_not_installed,
    download_and_install_webview2
)

# Проверить, установлен ли WebView2
if is_webview2_installed():
    print("✅ WebView2 уже установлен")
else:
    print("❌ WebView2 не найден")

# Установить, если не установлен (рекомендуемый способ)
result = install_webview2_if_not_installed(verbose=True)
if result == 0:
    print("✅ WebView2 уже установлен")
elif result == 1:
    print("✅ Установка WebView2 запущена")
else:
    print("❌ Ошибка установки WebView2")

# Принудительная загрузка и установка
success = download_and_install_webview2(verbose=True)
if success:
    print("✅ Установка успешно запущена")
```

### Возвращаемые значения install_webview2_if_not_installed()
| Значение | Описание                   |
|----------|----------------------------|
| 0        | WebView2 уже установлен    |
| 1        | Установка успешно запущена |
| -1       | Ошибка установки           |

## 🔧 Использование DLL в C/C++
### Сигнатуры функций
```c
// Проверяет установлен ли WebView2
bool is_webview2_installed(void);

// Загружает и устанавливает WebView2 (тихая установка)
bool download_and_install_webview2(void);

// С подробным выводом
bool download_and_install_webview2_verbose(void);

// Устанавливает если не установлен (0 = уже есть, 1 = успешно, -1 = ошибка)
int install_webview2_if_not_installed(void);

// С подробным выводом
int install_webview2_if_not_installed_verbose(void);
```

### Пример на C
```c
#include <windows.h>
#include <stdio.h>

typedef bool (*is_installed_fn)(void);
typedef int (*install_if_needed_fn)(void);

int main() {
    HMODULE dll = LoadLibrary("webview2_installer_x64.dll");
    if (!dll) return 1;
    
    auto is_installed = (is_installed_fn)GetProcAddress(dll, "is_webview2_installed");
    auto install_if_needed = (install_if_needed_fn)GetProcAddress(dll, "install_webview2_if_not_installed");
    
    if (is_installed && install_if_needed) {
        int result = install_if_needed();
        printf("Result: %d\n", result);
    }
    
    FreeLibrary(dll);
    return 0;
}
```

## 🛠️ Разработка и сборка
### Требования
- Rust (2021 edition)
- Python 3.8+
- Visual Studio Build Tools (Windows)
- cargo, rustup
- rcedit

### Сборка DLL
```shell
# Собрать release версии для всех архитектур
python build_dll.py

# Собрать debug версии
python build_dll.py --debug

# Динамическая линковка (требуется VC++ Redist)
python build_dll.py --dynamic
```

### Сборка Python пакета
```shell
# Установка зависимостей разработки
pip install -e ".[dev]"

# Сборка пакета
python -m build

# Или через devscript
devscript build_wheel
```

### Очистка файлов сборки
```shell
devscript clean
```

## 📋 Требования к системе
- **ОС:** Windows 7 / 8 / 10 / 11
- **Архитектуры:** x86, x64, ARM64
- **Python: 3.8+** (для Python пакета)
- **Интернет:** требуется для загрузки установщика

## 🔍 Как это работает
1. **Проверка установки:** через реестр Windows проверяется наличие ключей WebView2
2. **Загрузка:** скачивается официальный установщик от Microsoft
3. **Установка:** запускается в тихом режиме (`/silent /install`)
4. **Очистка:** временные файлы автоматически удаляются

## 📄 Лицензия
MIT License

## 🤝 Вклад в проект
PR и Issues приветствуются! Убедитесь, что изменения работают на всех целевых архитектурах.

## ⚠️ Известные ограничения
- Только Windows (целевая платформа)
- Установка синхронная — требуется подождать, пока webview2 установится
