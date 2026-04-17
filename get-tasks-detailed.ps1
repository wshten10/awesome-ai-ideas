$headers = @{
    "Authorization" = "Bearer PLACEHOLDER_API_KEY_PLEASE_REPLACE_WITH_ACTUAL_KEY"
}

try {
    Write-Host "Attempting to fetch tasks..."
    $response = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers -Verbose
    Write-Host "API call successful!"
    Write-Host "Response type: $($response.GetType())"
    
    if ($response) {
        $response | ConvertTo-Json -Depth 5
    } else {
        Write-Host "API returned empty response"
    }
} catch {
    Write-Host "API Error Details:"
    Write-Host "Exception: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)"
        Write-Host "Response Headers: $($_.Exception.Response.Headers)"
    }
    Write-Host "Error Type: $($_.Exception.GetType())"
}