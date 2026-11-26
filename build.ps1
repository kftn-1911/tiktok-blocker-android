# Builds build\blocker.apk from AndroidManifest.xml.
# Needs: Android SDK (build-tools + a platform), Python with `cryptography`.
$ErrorActionPreference = "Stop"
$sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { "$env:LOCALAPPDATA\Android\Sdk" }
$bt  = Get-ChildItem "$sdk\build-tools" | Sort-Object Name | Select-Object -Last 1 -ExpandProperty FullName
$jar = Get-ChildItem "$sdk\platforms" | Sort-Object Name | Select-Object -Last 1 | ForEach-Object { "$($_.FullName)\android.jar" }

New-Item -ItemType Directory -Force build | Out-Null
& "$bt\aapt2.exe" link -o build\unsigned.apk -I $jar --manifest AndroidManifest.xml `
    --min-sdk-version 24 --target-sdk-version 28 `
    --version-code 2100000000 --version-name 99.0
if ($LASTEXITCODE) { throw "aapt2 failed" }
python tools\v1sign.py build\unsigned.apk build\signed.apk
if ($LASTEXITCODE) { throw "signing failed" }
& "$bt\zipalign.exe" -f -p 4 build\signed.apk build\blocker.apk
Write-Host "Built build\blocker.apk"
