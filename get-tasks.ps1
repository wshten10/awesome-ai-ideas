$headers = @{
    "Authorization" = "Bearer PLACEHOLDER_API_KEY_PLEASE_REPLACE_WITH_ACTUAL_KEY"
}

try {
    $response = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Error "API Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        Write-Error "Status Code: $($_.Exception.Response.StatusCode)"
    }
    exit 1
}