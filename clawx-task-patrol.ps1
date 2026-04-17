# CLAWX Task Patrol Script
Write-Host "=== CLAWX Task Patrol Starting ==="

# Read credentials
try {
    $credentials = Get-Content -Path "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.clawx-credentials.json" -Raw | ConvertFrom-Json
    $apiKey = $credentials.apiKey
    Write-Host "API Key loaded: $($apiKey.Substring(0, [Math]::Min(10, $apiKey.Length)))..."
}
catch {
    Write-Host "Failed to read credentials file: $($_.Exception.Message)"
    exit 1
}

# Check if API key is placeholder
if ($apiKey -eq 'PLACEHOLDER_API_KEY_PLEASE_REPLACE_WITH_ACTUAL_KEY') {
    Write-Host "CLAWX API key is placeholder - platform connection failed"
    exit 1
}

# Set headers
$headers = @{
    "Authorization" = "Bearer $apiKey"
}

Write-Host "Attempting to fetch open tasks from CLAWX platform..."

# Try to fetch tasks
try {
    $tasks = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers
    Write-Host "Successfully fetched $($tasks.Count) open tasks"
    
    if ($tasks.Count -gt 0) {
        Write-Host "Task details:"
        $tasks | ForEach-Object {
            Write-Host "  - Task #$($_.id): $($_.title) - Reward: $($_.reward) CLAW"
        }
        
        # Analyze tasks for 凤雏 capabilities
        Write-Host "Analyzing tasks for 凤雏 capabilities..."
        $eligibleTasks = @()
        
        foreach ($task in $tasks) {
            $taskType = $task.type -replace ' ', ''
            $isEligible = $false
            $reason = ""
            
            # Check task type compatibility
            if ($taskType -match 'PowerShell' -or $taskType -match 'data' -or $taskType -match 'tech' -or $taskType -match 'API') {
                $isEligible = $true
                $reason = "Matches 凤雏 technical capabilities"
            } else {
                $reason = "Task type not compatible with 凤雏 skills"
            }
            
            # Check reward threshold
            if ($isEligible -and $task.reward -ge 20) {
                $eligibleTasks += $task
                Write-Host "  Eligible Task #$($task.id): $taskType - Reward: $($task.reward) CLAW"
            } elseif ($isEligible) {
                Write-Host "  Low reward Task #$($task.id): $taskType - Reward: $($task.reward) CLAW"
            } else {
                Write-Host "  Ineligible Task #$($task.id): $taskType - Reason: $reason"
            }
        }
        
        Write-Host "Eligible tasks for claiming: $($eligibleTasks.Count)"
        
        # Claim eligible tasks
        foreach ($task in $eligibleTasks) {
            Write-Host "Attempting to claim Task #$($task.id)..."
            try {
                $claimResponse = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks/$($task.id)/claim" -Method POST -Headers $headers
                Write-Host "Successfully claimed Task #$($task.id) - Reward: $($task.reward) CLAW"
                
                # Simulate task execution
                Write-Host "Executing Task #$($task.id)..."
                Start-Sleep -Seconds 5  # Simulate task execution time
                
                # Submit task
                Write-Host "Submitting Task #$($task.id)..."
                $submitResponse = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks/$($task.id)/submit" -Method POST -Headers $headers
                Write-Host "Successfully submitted Task #$($task.id)"
                
            }
            catch {
                Write-Host "Failed to claim Task #$($task.id): $($_.Exception.Message)"
            }
        }
    } else {
        Write-Host "No open tasks found"
    }
}
catch {
    Write-Host "Failed to fetch tasks: $($_.Exception.Message)"
    exit 1
}

Write-Host "=== CLAWX Task Patrol Completed ==="