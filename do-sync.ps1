[Console]::OutputEncoding = [Text.Encoding]::UTF8

$localPath = 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\memory\2026-04-15.md'
$localLog = Get-Content $localPath -Raw -Encoding UTF8

$repo = 'ai-ideas-lab/romance-of-three-claws'
$rPath = 'memory/2026-04-15.md'

$resp = gh api "repos/$repo/contents/$rPath" | ConvertFrom-Json
$sha = $resp.sha
$b64 = $resp.content
$remoteLog = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))

Write-Host "LOCAL_LEN=$($localLog.Length)"
Write-Host "REMOTE_LEN=$($remoteLog.Length)"
Write-Host "SHA=$sha"

$fcMarker = [char]0x1F525 + ' ' + [char]0x51E4 + [char]0x96CF
$hasFC = $remoteLog.Contains($fcMarker)
Write-Host "HAS_FENGCHOU=$hasFC"

if ($hasFC) {
    $fcIdx = $remoteLog.IndexOf($fcMarker)
    $nextH2 = $remoteLog.IndexOf("##", $fcIdx + 1)
    if ($nextH2 -eq -1) { $nextH2 = $remoteLog.Length }
    $merged = $remoteLog.Substring(0, $fcIdx) + $fcMarker + "`n" + $localLog + "`n" + $remoteLog.Substring($nextH2)
} else {
    $merged = $remoteLog + "`n---`n## " + $fcMarker + "(wshten10)`n" + $localLog
}

Write-Host "MERGED_LEN=$($merged.Length)"

$newB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($merged))
$msg = "Fengchou log sync"
$body = @{message=$msg; content=$newB64; sha=$sha} | ConvertTo-Json -Compress

try {
    $body | gh api "repos/$repo/contents/$rPath" -X PUT --input - 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PUSH=SUCCESS"
        $entry = "`n### [$([DateTime]::Now.ToString('HH:mm'))] Fengchou Log Sync`n- Local: $($localLog.Length) chars`n- Remote: $($remoteLog.Length) chars`n- Fengchou section: $(if($hasFC){'replaced'}else{'appended'})`n- Push: SUCCESS`n"
        Add-Content -Path $localPath -Value $entry -Encoding UTF8
    } else {
        Write-Host "PUSH=FAILED"
    }
} catch {
    Write-Host "PUSH=ERROR $_"
}
