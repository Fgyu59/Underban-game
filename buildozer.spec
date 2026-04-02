[app]

# Название приложения
title = Underban Game

# Имя пакета
package.name = underban

# Домен пакета (уникальный идентификатор)
package.domain = org.artomizer

# Исходная директория
source.dir = .

# Расширения файлов для включения
source.include_exts = py,png,jpg,jpeg,kv,atlas

# Версия приложения
version = 1.0

# Зависимости Python
requirements = python3,kivy,pygame_sdl2,android

# Ориентация (landscape, portrait или all)
orientation = landscape

# Включить все изображения
source.include_patterns = *.png,*.jpg

# Полноэкранный режим
fullscreen = 1

# Разрешения Android
android.permissions = INTERNET

# API уровень Android
android.api = 31

# Минимальный API уровень
android.minapi = 21

# Android NDK версия
android.ndk = 25b

# Android SDK версия
android.sdk = 31

# Bootstrap
p4a.bootstrap = sdl2

# Иконка приложения (если есть)
# icon.filename = %(source.dir)s/icon.png

# Presplash изображение (если есть)
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# Лог уровень (0 = только ошибки, 1 = информация, 2 = отладка)
log_level = 2

# Отображать предупреждения
warn_on_root = 1
