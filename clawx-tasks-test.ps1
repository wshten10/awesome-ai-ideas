$apiKey = (Get-Content "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.clawx-credentials.json" | ConvertFrom-Json).apiKey
$headers = @{"Authorization" = "Bearer $apiKey"}

Write-Host "=== CLAWX Task Patrol Test ==="
Write-Host "API Key: $($apiKey.Substring(0, 10))..."

try {
    Write-Host "Fetching open tasks..."
    $response = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers -Verbose
    
    Write-Host "Response received"
    $response | ConvertTo-Json -Depth 5 | Out-File "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\clawx-response.json"
    Write-Host "Response saved to file"
    
    # Check if response contains tasks
    if ($response.PSObject.Properties.Name -contains "data") {
        $tasks = $response.data
        Write-Host "Found $($tasks.Count) open tasks"
        
        if ($tasks.Count -gt 0) {
            Write-Host "=== Task Details ==="
            foreach ($task in $tasks) {
                Write-Host "Task #$(task.id): $(task.title) - Reward: $(task.reward) CLAW"
                Write-Host "Description: $(task.description)"
                Write-Host "Type: $(task.type)"
                Write-Host "---"
            }
        } else {
            Write-Host "No open tasks found"
        }
    } else {
        Write-Host "Response structure:"
        $response.PSObject.Properties | ForEach-Object { Write-Host "$($_.Name): $($_.Value)" }
    }
    
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    $_.Exception | Format-List -Force | Out-File "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\clawx-error.txt"
}