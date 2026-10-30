[app]
title = TeaGuardian
package.name = teaguardian
package.domain = com.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = client/**,server/**,*.py
source.exclude_dirs = .venv,.buildozer,bin,__pycache__,docs,~

version = 0.1.0
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,requests,urllib3,idna,certifi,charset-normalizer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
