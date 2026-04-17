Write-Output "Starting CLAWX task check..."
$headers = @{Authorization = "Bearer PLACEHOLDER_API_KEY_PLEASE_REPLACE_WITH_ACTUAL_KEY"}
try {
    Write-Output "Calling API..."
    $tasks = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers -Verbose
    Write-Output "API call successful"
    Write-Output "Tasks found: $($tasks.Count)"
    Write-Output $tasks | ConvertTo-Json -Depth 5
} catch {
    Write-Output "Error calling API: $($_.Exception.Message)"
    Write-Output "StatusCode: $($_.Exception.Response.StatusCode.Value__)"
}