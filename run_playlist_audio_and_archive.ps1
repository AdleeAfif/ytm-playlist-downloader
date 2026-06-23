param(
    [Parameter(Mandatory = $true)]
    [string]$PlaylistUrl,

    [string]$AudioFormat = "mp3",
    [int]$AudioQuality = 192
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DownloadsDir = Join-Path $env:USERPROFILE "Downloads"
$AudioDir = Join-Path $DownloadsDir "youtube_playlist_audio"
$ArchiveBase = Join-Path $DownloadsDir ("youtube_playlist_audio_{0}" -f (Get-Date -Format "yyyyMMdd_HHmmss"))

New-Item -ItemType Directory -Force -Path $AudioDir | Out-Null

Push-Location $ScriptDir
try {
    python -m pip install -r requirements_youtube_audio.txt

    python youtube_playlist_audio.py `
        $PlaylistUrl `
        --output $AudioDir `
        --audio-format $AudioFormat `
        --audio-quality $AudioQuality `
        --archive (Join-Path $AudioDir "downloaded.txt")
}
finally {
    Pop-Location
}

$rarCandidates = @(
    (Get-Command "rar.exe" -ErrorAction SilentlyContinue).Source,
    (Get-Command "WinRAR.exe" -ErrorAction SilentlyContinue).Source,
    "C:\Program Files\WinRAR\Rar.exe",
    "C:\Program Files\WinRAR\WinRAR.exe",
    "C:\Program Files (x86)\WinRAR\Rar.exe",
    "C:\Program Files (x86)\WinRAR\WinRAR.exe"
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

if ($rarCandidates) {
    $rarPath = $rarCandidates
    $rarArchive = "$ArchiveBase.rar"
    & $rarPath a -r -ep1 $rarArchive (Join-Path $AudioDir "*")
    Write-Host "Created RAR archive: $rarArchive"
}
else {
    $zipArchive = "$ArchiveBase.zip"
    Compress-Archive -Path (Join-Path $AudioDir "*") -DestinationPath $zipArchive -Force
    Write-Host "WinRAR/RAR was not found. Created ZIP archive instead: $zipArchive"
}

Write-Host "Audio folder: $AudioDir"
