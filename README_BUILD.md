# Инструкция по сборке APK из Pygame приложения

## Требования

Для сборки APK вам понадобится:
- Linux (рекомендуется Ubuntu 20.04 или новее)
- Python 3.8+
- Java Development Kit (JDK) 17
- Около 10 GB свободного места на диске
- Стабильное интернет-соединение

## Шаг 1: Подготовка системы

### Установка необходимых пакетов (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk \
    python3-dev build-essential libssl-dev libffi-dev \
    libsqlite3-dev zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libreadline-dev libffi-dev wget libbz2-dev \
    autoconf automake libtool pkg-config cmake ninja-build \
    ccache libltdl-dev
```

### Установка Android SDK (необязательно, buildozer скачает сам):

Buildozer автоматически скачает Android SDK и NDK при первой сборке.

## Шаг 2: Установка Buildozer

```bash
pip3 install --user buildozer
pip3 install --user cython
```

Добавьте в PATH (если необходимо):
```bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

## Шаг 3: Подготовка проекта

Убедитесь, что в папке проекта есть:
- main.py (главный файл игры)
- buildozer.spec (конфигурационный файл)
- _face.png (изображение)
- dusha.png (изображение)

Все эти файлы уже присутствуют в вашем проекте!

## Шаг 4: Сборка APK

### Вариант 1: Используя готовый скрипт

```bash
chmod +x build_apk.sh
./build_apk.sh
```

### Вариант 2: Вручную

Перейдите в папку проекта:
```bash
cd /путь/к/вашему/проекту/underban
```

Инициализация buildozer (при первом запуске):
```bash
buildozer init
```

Примечание: файл buildozer.spec уже создан, поэтому этот шаг можно пропустить.

Сборка APK в режиме отладки:
```bash
buildozer -v android debug
```

Сборка APK в режиме релиза:
```bash
buildozer -v android release
```

## Шаг 5: Получение APK файла

После успешной сборки APK файл будет находиться в:
```
./bin/underban-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

или для релизной версии:
```
./bin/underban-1.0-arm64-v8a_armeabi-v7a-release-unsigned.apk
```

## Шаг 6: Установка на Android устройство

### Через ADB:
```bash
adb install bin/underban-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

### Через файловый менеджер:
1. Скопируйте APK файл на устройство
2. Откройте файл через файловый менеджер
3. Разрешите установку из неизвестных источников (если требуется)
4. Установите приложение

## Возможные проблемы и решения

### Проблема: "Command failed: ... NDK ..."
**Решение:** Buildozer скачивает NDK автоматически. Дождитесь завершения загрузки (может занять 10-30 минут).

### Проблема: "No space left on device"
**Решение:** Освободите минимум 10 GB на диске. Временные файлы buildozer занимают много места.

### Проблема: Ошибки компиляции
**Решение:** Убедитесь, что установлены все зависимости из Шага 1.

### Проблема: Pygame не работает на Android
**Решение:** На Android используется pygame_sdl2, который совместим с обычным pygame. Ваш код уже адаптирован.

### Проблема: Приложение вылетает при запуске
**Решение:** Проверьте логи:
```bash
adb logcat | grep python
```

## Оптимизация

### Уменьшение размера APK:
1. Оптимизируйте изображения (сожмите PNG файлы)
2. Удалите неиспользуемые ресурсы
3. Используйте ProGuard (для продвинутых пользователей)

### Улучшение производительности:
1. Используйте релизную сборку вместо debug
2. Оптимизируйте игровой код (меньше вычислений в цикле)
3. Используйте pygame.sprite для управления объектами

## Дополнительные команды Buildozer

Очистка проекта:
```bash
buildozer android clean
```

Просмотр списка устройств:
```bash
buildozer android adb -- devices
```

Запуск приложения на устройстве:
```bash
buildozer android deploy run
```

Просмотр логов:
```bash
buildozer android logcat
```

## Важные замечания

1. **Первая сборка** может занять 30-60 минут (скачивание SDK, NDK, компиляция зависимостей)
2. **Последующие сборки** будут намного быстрее (5-10 минут)
3. **Интернет** обязателен для первой сборки
4. **RAM**: рекомендуется минимум 4 GB оперативной памяти

## Подписание APK для Google Play

Для публикации в Google Play Store нужно подписать APK:

```bash
# Создание ключа
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias \
    -keyalg RSA -keysize 2048 -validity 10000

# Подписание APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore my-release-key.keystore \
    bin/underban-1.0-arm64-v8a_armeabi-v7a-release-unsigned.apk my-key-alias

# Оптимизация APK
zipalign -v 4 bin/underban-1.0-arm64-v8a_armeabi-v7a-release-unsigned.apk \
    bin/underban-1.0-signed.apk
```

## Контакты и поддержка

Если возникли проблемы:
1. Проверьте логи buildozer: `buildozer -v android debug`
2. Изучите документацию: https://buildozer.readthedocs.io/
3. Форум Kivy: https://groups.google.com/forum/#!forum/kivy-users

Удачи в сборке! 🚀
