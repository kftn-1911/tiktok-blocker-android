# TikTok Blocker for Android

**Stop wasting time on TikTok.** This project blocks TikTok from being installed on an Android phone, so endless scrolling stops being one tap away.

It's a personal self-control tool: no root, no special app, just a USB cable and `adb`.

## How it works

Every Android app is identified by a unique package name. TikTok's is `com.zhiliaoapp.musically`.

Android allows only **one** app per package name, and only lets an app be updated by one signed with the **same key**. So the trick is:

1. Uninstall TikTok.
2. Install a tiny placeholder app that uses TikTok's package name, signed with a different key.

Now when the Play Store (or a backup restore) tries to install TikTok, Android refuses: the package name is taken by an app with a different signature.

The placeholder:
- has **no code**, no permissions, and no background activity (zero battery/data use)
- has **no launcher icon**, so it doesn't appear on the home screen or app drawer
- uses a dull name, **"Sys Cfg Cache"**, so it's easy to overlook in Settings → Apps
- has version `99.0` / versionCode `2100000000`, so nothing can "update" over it

## Quick install (no PC needed)

1. **Uninstall TikTok** from your phone first. The blocker can't install while TikTok is there.
2. Download **`tiktok-blocker.apk`** from the [latest release](https://github.com/kftn-1911/tiktok-blocker-android/releases/latest) and tap it.
3. Allow "Install unknown apps" for your browser or file manager when Android asks.
4. If Play Protect warns about an unknown app, tap **More details → Install anyway**. A notice that the app was "built for an older version of Android" is expected and harmless.

Then try installing TikTok from the Play Store: it should fail.

## Build it yourself

### Requirements

- Windows PC with PowerShell
- [Android SDK](https://developer.android.com/studio) (build-tools and one platform), e.g. installed by Android Studio
- Python 3 with `cryptography` (`pip install cryptography`). Java is **not** needed.
- `adb` and a phone with **USB debugging** enabled

### Usage

```powershell
.\build.ps1      # builds build\blocker.apk
.\install.ps1    # removes TikTok from the connected phone and installs the placeholder
```

## Files

| File | Purpose |
| --- | --- |
| `AndroidManifest.xml` | The whole placeholder app: TikTok's package name, no code |
| `build.ps1` | Builds and aligns the APK with `aapt2` and `zipalign` |
| `tools/v1sign.py` | Signs the APK with a fresh throwaway key (no Java needed) |
| `install.ps1` | Uninstalls TikTok and installs the placeholder via `adb` |

## Limits

This is a speed bump, not a lock: you own the phone, so you can always undo it.

- Uninstalling "Sys Cfg Cache" from Settings → Apps removes the block.
- The TikTok website still works in a browser. Block it with a DNS filter (e.g. NextDNS) if needed.
- Consider turning off app restore in Settings → Google → Backup so a restore can't bring TikTok back.

To undo it on purpose:

```powershell
adb uninstall com.zhiliaoapp.musically
```

## Disclaimer

Not affiliated with TikTok or ByteDance. Use it only on your own device.
