#!/bin/bash

# Скрипт автоматической сборки APK для Underban Game
# Автор: Artomizer

set -e  # Остановка при ошибках

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Сборка APK для Underban Game с помощью Buildozer  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Python
print_status "Проверка Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 не найден! Установите Python 3.8 или новее."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_success "Найден: $PYTHON_VERSION"

# Проверка наличия pip
print_status "Проверка pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 не найден! Установите pip3."
    exit 1
fi
print_success "pip3 установлен"

# Проверка наличия buildozer
print_status "Проверка buildozer..."
if ! command -v buildozer &> /dev/null; then
    print_warning "Buildozer не найден. Устанавливаю..."
    pip3 install --user buildozer
    pip3 install --user cython
    export PATH=$PATH:~/.local/bin
    print_success "Buildozer установлен"
else
    print_success "Buildozer уже установлен"
fi

# Проверка необходимых файлов
print_status "Проверка файлов проекта..."
REQUIRED_FILES=("main.py" "buildozer.spec" "_face.png" "dusha.png")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Файл $file не найден!"
        exit 1
    fi
done
print_success "Все необходимые файлы найдены"

# Проверка свободного места на диске
print_status "Проверка свободного места..."
FREE_SPACE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$FREE_SPACE" -lt 10 ]; then
    print_warning "Мало свободного места на диске (${FREE_SPACE}GB). Рекомендуется минимум 10GB."
    read -p "Продолжить? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_success "Свободного места: ${FREE_SPACE}GB"
fi

# Выбор типа сборки
echo ""
echo "Выберите тип сборки:"
echo "1) Debug (для тестирования)"
echo "2) Release (для публикации)"
read -p "Ваш выбор (1 или 2): " BUILD_TYPE

case $BUILD_TYPE in
    1)
        BUILD_MODE="debug"
        print_status "Выбран режим: Debug"
        ;;
    2)
        BUILD_MODE="release"
        print_status "Выбран режим: Release"
        ;;
    *)
        print_error "Неверный выбор!"
        exit 1
        ;;
esac

# Очистка предыдущей сборки (опционально)
echo ""
read -p "Очистить предыдущую сборку? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Очистка проекта..."
    buildozer android clean
    print_success "Проект очищен"
fi

# Начало сборки
echo ""
print_status "════════════════════════════════════════════════"
print_status "Начинаю сборку APK в режиме $BUILD_MODE..."
print_status "Это может занять 30-60 минут при первой сборке"
print_status "════════════════════════════════════════════════"
echo ""

START_TIME=$(date +%s)

# Запуск buildozer
if [ "$BUILD_MODE" = "debug" ]; then
    buildozer -v android debug
else
    buildozer -v android release
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

echo ""
print_success "════════════════════════════════════════════════"
print_success "Сборка успешно завершена!"
print_success "Время сборки: ${MINUTES} минут ${SECONDS} секунд"
print_success "════════════════════════════════════════════════"
echo ""

# Поиск APK файла
print_status "Поиск APK файла..."
APK_FILE=$(find bin -name "*.apk" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")

if [ -n "$APK_FILE" ]; then
    APK_SIZE=$(du -h "$APK_FILE" | cut -f1)
    print_success "APK создан: $APK_FILE"
    print_success "Размер: $APK_SIZE"
    echo ""
    
    # Опции установки
    echo "Что делать дальше?"
    echo "1) Установить на подключенное устройство (через ADB)"
    echo "2) Только показать путь к APK"
    echo "3) Выход"
    read -p "Ваш выбор (1-3): " NEXT_ACTION
    
    case $NEXT_ACTION in
        1)
            print_status "Проверка подключенных устройств..."
            DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)
            
            if [ "$DEVICES" -gt 0 ]; then
                print_status "Установка APK на устройство..."
                adb install -r "$APK_FILE"
                print_success "APK установлен!"
            else
                print_error "Устройства не найдены. Подключите Android устройство через USB."
            fi
            ;;
        2)
            echo ""
            echo "────────────────────────────────────────────────"
            echo "Путь к APK: $APK_FILE"
            echo "────────────────────────────────────────────────"
            ;;
        *)
            print_status "Выход"
            ;;
    esac
else
    print_error "APK файл не найден в папке bin/"
    exit 1
fi

echo ""
print_success "Готово! 🚀"
echo ""
echo "Инструкция по установке:"
echo "1. Скопируйте APK на Android устройство"
echo "2. Откройте файловый менеджер на устройстве"
echo "3. Нажмите на APK файл"
echo "4. Разрешите установку из неизвестных источников (если требуется)"
echo "5. Установите приложение"
echo ""
