[app]
title = just_you
package.name = just_you
package.domain = org.justyou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0,kivymd,pyjnius

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

android.permissions = SYSTEM_ALERT_WINDOW, PACKAGE_USAGE_STATS, FOREGROUND_SERVICE, RECEIVE_BOOT_COMPLETED

android.services = LockService:main.py

android.api = 33
android.minapi = 21
android.sdk = 33