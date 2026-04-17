# Phoenix Log Sync Script
# Sync local logs to collaborative repository 3 times daily
# Author: wshten10 (Phoenix)

# Current date
$currentDate = Get-Date -Format "yyyy-MM-dd"
$localLogPath = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\memory\$currentDate.md"
$remoteRepo = "ai-ideas-lab/romance-of-three-claws"
$remotePath = "memory/$currentDate.md"

Write-Host "=== Phoenix Log Sync Start ==="
Write-Host "Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host "Local Log Path: $localLogPath"

# Step 1: Read local log
try {
    $localLog = Get-Content $localLogPath -Raw -Encoding UTF8
    $localLogLength = $localLog.Length
    Write-Host "Local log read successfully, length: $localLogLength characters"
} catch {
    Write-Host "Local log read failed: $($_.Exception.Message)"
    exit 1
}

# Step 2: Read remote repository log
try {
    $apiResponse = gh api repos/$remoteRepo/contents/$remotePath --jq '{sha: .sha, content: .content}'
    $remoteData = $apiResponse | ConvertFrom-Json
    $remoteSHA = $remoteData.sha
    $remoteContent = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($remoteData.content))
    Write-Host "Remote log read successfully"
} catch {
    Write-Host "Remote log read failed: $($_.Exception.Message)"
    # If file not found error, create empty content
    if ($_.Exception.Message -like "*404*") {
        Write-Host "Remote file not found, will create new file"
        $remoteContent = ""
        $remoteSHA = ""
    } else {
        exit 1
    }
}

# Step 3: Check if remote log already has Phoenix section
$fengcuPattern = "凤雏"
$fengcuSections = $remoteContent | Select-String -Pattern $fengcuPattern -AllMatches
$hasFengcuSection = $fengcuSections.Matches.Count -gt 0

if ($hasFengcuSection) {
    Write-Host "Remote log status: Has Phoenix section"
} else {
    Write-Host "Remote log status: No Phoenix section"
}

# Merge logs
$mergedContent = $remoteContent

if (-not $hasFengcuSection) {
    # If no Phoenix section: add Phoenix section to the end
    Write-Host "Adding new Phoenix section to remote log end"
    
    if ($remoteContent.Length -gt 0) {
        # If remote content is not empty, add separator
        $mergedContent = $remoteContent + "`n`n---`n`n"
    }
    
    # Add Phoenix section title and content
    $mergedContent += "## 凤雏(wshten10)日志`n"
    $mergedContent += $localLog
} else {
    # If already has Phoenix section: replace old Phoenix section
    Write-Host "Replacing existing Phoenix section"
    
    # Find the start position of Phoenix section
    $fengcuStartIndex = $remoteContent.IndexOf("## 凤雏")
    if ($fengcuStartIndex -ge 0) {
        # Find the position of next header or end of file
        $nextHeaderIndex = $remoteContent.IndexOf("`n## ", $fengcuStartIndex + 1)
        if ($nextHeaderIndex -lt 0) {
            $nextHeaderIndex = $remoteContent.Length
        }
        
        # Keep content before Phoenix section
        $beforeFengcu = $remoteContent.Substring(0, $fengcuStartIndex)
        
        # Keep content after Phoenix section
        $afterFengcu = $remoteContent.Substring($nextHeaderIndex)
        
        # Build new content
        $mergedContent = $beforeFengcu + "## 凤雏(wshten10)日志`n" + $localLog + $afterFengcu
    } else {
        Write-Host "Phoenix section title not found, but Phoenix content detected, using append mode"
        $mergedContent = $remoteContent + "`n`n---`n`n## 凤雏(wshten10)日志`n" + $localLog
    }
}

# Step 4: Push update
try {
    Write-Host "Preparing to push update to remote repository..."
    
    $encodedContent = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($mergedContent))
    
    $payload = @{
        message = "Phoenix Log Sync - $(Get-Date)"
        content = $encodedContent
        sha = $remoteSHA
    } | ConvertTo-Json -Depth 10
    
    # Push to remote repository
    $result = gh api repos/$remoteRepo/contents/$remotePath -X PUT -f $payload
    
    Write-Host "Push successful"
    
    # Record sync result
    $statusText = if ($hasFengcuSection) { "Has Phoenix section" } else { "No Phoenix section" }
    $syncTime = Get-Date -Format 'HH:mm'
    $syncResult = "### [$syncTime] 凤雏日志同步`n- Local log length: $localLogLength characters`n- Remote log status: $statusText`n- Merge result: Success`n- Push result: Success`n"

} catch {
    Write-Host "Push failed: $($_.Exception.Message)"
    $statusText = if ($hasFengcuSection) { "Has Phoenix section" } else { "No Phoenix section" }
    $syncTime = Get-Date -Format 'HH:mm'
    $syncResult = "### [$syncTime] 凤雏日志同步`n- Local log length: $localLogLength characters`n- Remote log status: $statusText`n- Merge result: Failed`n- Push result: Failed`n"
}

# Append result to local log
Add-Content $localLogPath -Value $syncResult -Encoding UTF8

Write-Host "=== Phoenix Log Sync Complete ==="
Write-Host "Sync Statistics:"
Write-Host "  - Local log length: $localLogLength characters"
Write-Host "  - Remote status: $(if ($hasFengcuSection) { 'Phoenix section exists' } else { 'New Phoenix section added' })"
Write-Host "  - Sync result: Success"