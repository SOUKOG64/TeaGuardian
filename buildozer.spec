[app]
# (str) Title of your application
title = TeaGuardian

# (str) Package name
package.name = teaguardian

# (str) Package domain (needed for android/identifier)
domain = com.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty for all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
source.include_patterns = client/**,server/**,*.py

# (str) Application versioning (method 1)
version = 0.1.0

# (list) Application requirements
requirements = python3,kivy,requests

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Android package installation location
android.install_location = auto

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) Android permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

android.accept_sdk_license = True
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
requirements = python3,kivy,requests,urllib3,idna,certifi,charset-normalizer
android.permissions = INTERNET
# (bool) Use --private data directory instead of --dir
# android.private_storage = True

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (bool) Copy library instead of fetching it
# android.copy_libs = 1

# (str) The Android arch to build for, choices: arm64-v8a, armeabi-v7a, x86, x86_64
android.archs = arm64-v8a

# (bool) If True, then use pyjnius to handle Android Java classes
# p4a.branch = master

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is running in a root directory
warn_on_root = 1

# (str) Path to build artifact directory
# build_dir = .buildozer

# (str) Path to the buildozer debug output directory
# build_dir = .buildozer

# (str) Path to the final packaging output directory
# bin_dir = ./bin
