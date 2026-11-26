# Removes TikTok from the connected phone and immediately installs the placeholder.
# Needs: adb on PATH, USB debugging enabled, build\blocker.apk (run build.ps1 first).
$pkg = "com.zhiliaoapp.musically"
adb shell pm uninstall $pkg              # fails harmlessly if TikTok is not installed
adb install build\blocker.apk
adb shell "dumpsys package $pkg | grep versionName"   # should print versionName=99.0
