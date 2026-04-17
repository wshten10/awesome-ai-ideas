# Read credentials
Write-Host "Reading credentials..."
$json = Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.clawx-credentials.json' -Raw
Write-Host "Credentials JSON length: $($json.Length)"
$creds = $json | ConvertFrom-Json
Write-Host "API Key: $($creds.apiKey.Substring(0, 10))..." # Show first 10 chars

$headers = @{ "Authorization" = "Bearer $($creds.apiKey)" }
Write-Host "Headers prepared"

try {
    Write-Host "Attempting API call..."
    $tasks = Invoke-RestMethod -Uri "https://money.rxcloud.group/api/v1/tasks?status=open" -Headers $headers
    Write-Host "API call successful!"
    Write-Host "Tasks response type: $($tasks.GetType().Name)"
    Write-Host "Number of tasks: $($tasks.Count)"
    
    # Display task details
    $tasks | ForEach-Object {
        Write-Host "`n=== Task $($_.id) ==="
        Write-Host "Title: $($_.title)"
        Write-Host "Description: $($_.description)"
        Write-Host "Reward: $($_.reward) $CLAW"
        Write-Host "Type: $($_.type)"
        Write-Host "Created: $($_.created_at)"
        Write-Host "Requirements: $($_.requirements)"
    }
    
    # Export full task data
    $tasks | ConvertTo-Json -Depth 10 | Out-File "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\tasks-data.json"
    
} catch {
    Write-Host "API Error: $($_.Exception.Message)"
    Write-Host "Error Type: $($_.Exception.GetType().Name)"
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode)"
        $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        $errorBody = $reader.ReadToEnd()
        Write-Host "Response Body: $errorBody"
    } else {
        Write-Host "No response object available"
    }
}