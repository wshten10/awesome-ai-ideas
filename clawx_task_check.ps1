# Read API key
$apiKey = (Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.clawx-credentials.json' | ConvertFrom-Json).apiKey
$headers = @{
    "Authorization" = "Bearer " + $apiKey
}

# Check for open tasks
Write-Host "Checking CLAWX for open tasks..."
try {
    $response = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers
    $tasks = $response.tasks
    Write-Host "Found $($tasks.Count) open tasks"
    $tasks | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error retrieving tasks: $($_.Exception.Message)"
    $null
}