# 🎮 Underban Game - Сборка APK

## Быстрый старт

### Вариант 1: Автоматическая сборка (рекомендуется)

```bash
./build_apk.sh
```

Скрипт сам все проверит и соберет APK.

### Вариант 2: Ручная сборка

```bash
# Установка buildozer (один раз)
pip3 install --user buildozer cython

# Сборка APK
buildozer -v android debug
```

APK будет в папке `bin/`

## Требования

- **ОС**: Linux (Ubuntu 20.04+)
- **Python**: 3.8+
- **Место**: ~10 GB свободного места
- **Время**: 30-60 минут (первая сборка)

## Установка зависимостей Ubuntu

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk \
    python3-dev build-essential libssl-dev libffi-dev \
    libsqlite3-dev zlib1g-dev libncurses5-dev
```

## Файлы в проекте

- `main.py` - главный файл игры ✅
- `buildozer.spec` - конфигурация сборки ✅
- `_face.png` - изображение босса ✅
- `dusha.png` - изображение души ✅
- `build_apk.sh` - скрипт автосборки ✅
- `README_BUILD.md` - подробная инструкция ✅

## Изменения в коде

В `main.py` добавлена поддержка:
- Кнопки "Назад" на Android
- Выход через ESC
- Адаптация под мобильные устройства

## Возможные проблемы

**Buildozer не найден:**
```bash
export PATH=$PATH:~/.local/bin
source ~/.bashrc
```

**Нет места на диске:**
Освободите минимум 10 GB

**Долго скачивает:**
При первой сборке buildozer скачивает Android SDK/NDK (~3-5 GB)

## Установка APK на телефон

### Через ADB (USB кабель):
```bash
adb install bin/*.apk
```

### Через файл:
1. Скопируйте APK на телефон
2. Откройте через файловый менеджер
3. Разрешите установку из неизвестных источников
4. Установите

## Дополнительные команды

```bash
# Очистка проекта
buildozer android clean

# Просмотр устройств
adb devices

# Логи приложения
adb logcat | grep python
```

## Поддержка

Подробная инструкция: `README_BUILD.md`

Документация Buildozer: https://buildozer.readthedocs.io/

---
**Автор**: Artomizer  
**Версия**: 1.0  
**Лицензия**: Свободная
