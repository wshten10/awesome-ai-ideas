# CLAWX Task Patrol Script
# Date: 2026-04-17
# Time: 13:03

# Read credentials
$credentials = Get-Content -Path "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.clawx-credentials.json" -Raw | ConvertFrom-Json
$apiKey = $credentials.apiKey

Write-Host "CLAWX Task Patrol Started - $(Get-Date)"
Write-Host "API Key Status: $($apiKey -ne 'PLACEHOLDER_API_KEY_PLEASE_REPLACE_WITH_ACTUAL_KEY')"

# Check CLAWX OPEN tasks
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

try {
    Write-Host "Fetching OPEN tasks..."
    $tasks = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers
    
    Write-Host "OPEN Tasks Count: $($tasks.Count)"
    
    # Analyze tasks
    $claimTasks = @()
    $skipTasks = @()
    
    foreach ($task in $tasks) {
        $taskType = $task.type -join ", "
        $reward = $task.reward -join ", "
        $taskId = $task.id -join ", "
        
        Write-Host "Task #$taskId - Type: $taskType, Reward: $reward CLAW"
        
        # Analysis criteria:
        # 1. Task type matches 凤雏 capabilities (PowerShell/data analysis/technical documentation/API validation)
        # 2. Reward >= 20 CLAW
        # 3. Task is executable
        
        $shouldClaim = $false
        $skipReason = ""
        
        # Check task type match
        $typeMatch = $taskType -match "PowerShell|data analysis|technical documentation|API validation|scripting"
        if (-not $typeMatch) {
            $skipReason = "Task type outside Feng Chuu capability range"
            $skipTasks += [PSCustomObject]@{
                Id = $taskId
                Type = $taskType
                Reward = $reward
                Reason = $skipReason
            }
            continue
        }
        
        # Check reward threshold
        if ($reward -lt 20) {
            $skipReason = "Reward below 20 CLAW threshold"
            $skipTasks += [PSCustomObject]@{
                Id = $taskId
                Type = $taskType
                Reward = $reward
                Reason = $skipReason
            }
            continue
        }
        
        # Task meets criteria - claim it
        $claimTasks += [PSCustomObject]@{
            Id = $taskId
            Type = $taskType
            Reward = $reward
        }
    }
    
    Write-Host "Analysis Complete - Ready to claim $($claimTasks.Count) tasks"
    Write-Host "Skip $($skipTasks.Count) tasks"
    
    # Display tasks to claim
    foreach ($task in $claimTasks) {
        Write-Host "READY TO CLAIM: Task #$(task.Id) - Type: $(task.Type) - Reward: $(task.Reward) CLAW"
    }
    
    # Save results to memory file
    $logContent = @"
### [13:03] CLAWX Task Patrol
- OPEN tasks: $($tasks.Count)
- Claim: $($claimTasks.Count) tasks
- Skip: $($skipTasks.Count) tasks

#### Tasks to Claim:
$($claimTasks | ForEach-Object { "- Task #$($_.Id) (Reward $($_.Reward) CLAW, Type:$($_.Type))" } | Out-String)

#### Skipped Tasks:
$($skipTasks | ForEach-Object { "- Task #$($_.Id) (Reward $($_.Reward) CLAW) - Reason:$($_.Reason)" } | Out-String)
"@
    
    # Append to memory file
    $memoryFile = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\memory\2026-04-17.md"
    $existingContent = Get-Content $memoryFile -Raw
    $newContent = $existingContent + "`n`n" + $logContent
    $newContent | Set-Content $memoryFile
    
    Write-Host "Results saved to memory file"
    
} catch {
    Write-Host "Error fetching tasks: $($_.Exception.Message)"
    
    # Log error to memory file
    $errorLog = @"
### [13:03] CLAWX Task Patrol
- OPEN tasks: 0 (API call failed)
- Error: $($_.Exception.Message)
"@
    
    $memoryFile = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\memory\2026-04-17.md"
    $existingContent = Get-Content $memoryFile -Raw
    $newContent = $existingContent + "`n`n" + $errorLog
    $newContent | Set-Content $memoryFile
    
    Write-Host "Error logged to memory file"
}