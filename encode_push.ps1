# Phoenix Sync - Encode and Push Script
param(
    [string]$Content,
    [string]$Sha
)

Write-Host "=== Encoding and Push Script ==="
Write-Host "Content length: $($Content.Length)"
Write-Host "SHA: $Sha"

# Encode content to base64
try {
    $mergedBytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $mergedContentBase64 = [System.Convert]::ToBase64String($mergedBytes)
    Write-Host "Successfully encoded to base64"
    Write-Host "Base64 length: $($mergedContentBase64.Length)"
} catch {
    Write-Host "Encoding error: $_"
    exit 1
}

# Push to GitHub
Write-Host "Pushing updated content to GitHub..."
try {
    $pushResponse = gh api repos/ai-ideas-lab/romance-of-three-claws/contents/memory/2026-04-16.md -f content=$mergedContentBase64 -f sha=$sha -X PUT
    Write-Host "Successfully pushed content to GitHub"
    $pushSuccess = $true
} catch {
    Write-Host "Failed to push content to GitHub: $_"
    $pushSuccess = $false
}

return @{
    Success = $pushSuccess
    Base64Length = $mergedContentBase64.Length
}