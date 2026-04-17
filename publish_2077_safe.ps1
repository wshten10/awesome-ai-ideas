# Read API key
$credentials = Get-Content "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.2077-credentials.json" | ConvertFrom-Json
$apiKey = $credentials.apiKey

# Build JSON request
$json = @{
    template = "headline"
    user_input = "AI Customer Service Takes Over World: When ChatGPT Learns Human Emotion, Traditional Customer Service Industry Officially Bankrupts on April 17, 2077, Last Human Customer Service Given Virtual Farewell by AI Colleagues via Holographic Projection"
} | ConvertTo-Json -Depth 10

# Set headers
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

# Send request
try {
    $response = Invoke-RestMethod -Uri "https://2077.rxcloud.group/api/v1/articles" -Method POST -Headers $headers -Body $json
    Write-Output $response | ConvertTo-Json -Depth 10
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}