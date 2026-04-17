# 凤雏日志同步脚本
param(
    [string]$localLogPath = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\memory\2026-04-15.md",
    [string]$remoteRepo = "ai-ideas-lab/romance-of-three-claws",
    [string]$remotePath = "memory/2026-04-15.md"
)

# 第一步：读取本地日志
$localLog = Get-Content $localLogPath -Raw
Write-Host "本地日志长度: $($localLog.Length)字符"

# 第二步：读取远程协作仓库日志
try {
    $remoteResponse = gh api "repos/$remoteRepo/contents/$remotePath"
    $remoteSha = $remoteResponse.sha
    $remoteContentBase64 = $remoteResponse.content
    $remoteLog = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($remoteContentBase64))
    Write-Host "远程日志状态: 已获取SHA: $remoteSha"
} catch {
    Write-Host "远程日志状态: 获取失败 - $($_.Exception.Message)"
    return
}

# 第三步：合并日志
$fengchouMarker = "🔥 凤雏"
$fengchouHeader = "## 🔥 凤雏(wshten10)日志"

$hasFengchouPart = $remoteLog -match $fengchouMarker
$mergeResult = ""

if ($hasFengchouPart) {
    Write-Host "远程日志状态: 有凤雏部分"
    
    # 提取凤雏部分的开头位置
    $fengchouStartIndex = $remoteLog.IndexOf($fengchouMarker)
    $fengchouEndIndex = $remoteLog.IndexOf("##", $fengchouStartIndex + 1)
    
    if ($fengchouEndIndex -eq -1) {
        $fengchouEndIndex = $remoteLog.Length
    }
    
    # 用凤雏本地日志替换旧的凤雏部分
    $beforeFengchou = $remoteLog.Substring(0, $fengchouStartIndex)
    $afterFengchou = $remoteLog.Substring($fengchouEndIndex)
    $mergeResult = $beforeFengchou + $fengchouMarker + "`n" + $localLog + "`n" + $afterFengchou
    Write-Host "合并结果: 成功（替换凤雏部分）"
} else {
    Write-Host "远程日志状态: 无凤雏部分"
    
    # 在远程日志末尾追加分隔线和凤雏部分
    $mergeResult = $remoteLog + "`n" + "---`n" + $fengchouHeader + "`n" + $localLog
    Write-Host "合并结果: 成功（追加凤雏部分）"
}

# 第四步：推送更新
try {
    $mergedContentBase64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($mergeResult))
    
    $payload = @{
        message = "凤雏日志同步 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        content = $mergedContentBase64
        sha = $remoteSha
    } | ConvertTo-Json -Depth 10
    
    $updateResponse = gh api "repos/$remoteRepo/contents/$remotePath" -X PUT -F message=$payload.message -F content=$payload.content -F sha=$payload.sha
    
    Write-Host "推送结果: 成功"
    
    # 记录同步结果
    $logEntry = @"
### [$(Get-Date -Format 'HH:mm')] 凤雏日志同步
- 本地日志长度: $($localLog.Length)字符
- 远程日志状态: $(if ($hasFengchouPart) {"有凤雏部分"} else {"无凤雏部分"})
- 合并结果: 成功
- 推送结果: 成功
"@
    
    Add-Content $localLogPath $logEntry
    Write-Host "同步结果已记录到本地日志"
    
} catch {
    Write-Host "推送结果: 失败 - $($_.Exception.Message)"
    
    # 记录失败结果
    $logEntry = @"
### [$(Get-Date -Format 'HH:mm')] 凤雏日志同步
- 本地日志长度: $($localLog.Length)字符
- 远程日志状态: $(if ($hasFengchouPart) {"有凤雏部分"} else {"无凤雏部分"})
- 合并结果: 成功
- 推送结果: 失败 - $($_.Exception.Message)
"@
    
    Add-Content $localLogPath $logEntry
    Write-Host "同步失败结果已记录到本地日志"
}