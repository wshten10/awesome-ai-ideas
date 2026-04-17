# List files in ava-agent/awesome-ai-ideas repository directories
# This script avoids --jq and --q flags and uses PowerShell for JSON parsing

# Change to the repository directory if needed
Set-Location -Path "ava-agent/awesome-ai-ideas" -ErrorAction SilentlyContinue

# Function to parse JSON response
function Parse-GhApiJson {
    param (
        [string]$jsonResponse
    )
    # Convert JSON string to PowerShell objects
    $jsonObject = $jsonResponse | ConvertFrom-Json
    return $jsonObject
}

# List files in prs/ directory
Write-Host "Listing files in prs/ directory..." -ForegroundColor Green
$prsResponse = gh api "repos/ava-agent/awesome-ai-ideas/contents/prs" --paginate
$prsFiles = Parse-GhApiJson -jsonResponse $prsResponse
$prsFileNames = $prsFiles.name | Where-Object { $_ -like "*" }
Write-Host "Found $($prsFileNames.Count) files in prs/ directory:"
$prsFileNames | ForEach-Object { Write-Host "  - $_" }

# List files in pr/ directory  
Write-Host "`nListing files in pr/ directory..." -ForegroundColor Green
$prResponse = gh api "repos/ava-agent/awesome-ai-ideas/contents/pr" --paginate
$prFiles = Parse-GhApiJson -jsonResponse $prResponse
$prFileNames = $prFiles.name | Where-Object { $_ -like "*" }
Write-Host "Found $($prFileNames.Count) files in pr/ directory:"
$prFileNames | ForEach-Object { Write-Host "  - $_" }

# List files in ideas/ directory
Write-Host "`nListing files in ideas/ directory..." -ForegroundColor Green
$ideasResponse = gh api "repos/ava-agent/awesome-ai-ideas/contents/ideas" --paginate
$ideasFiles = Parse-GhApiJson -jsonResponse $ideasResponse
$ideasFileNames = $ideasFiles.name | Where-Object { $_ -like "*" }
Write-Host "Found $($ideasFileNames.Count) files in ideas/ directory:"
$ideasFileNames | ForEach-Object { Write-Host "  - $_" }

# Export results to file for sampling
$allFiles = @()
$allFiles += @{"directory" = "prs"; "files" = $prsFileNames}
$allFiles += @{"directory" = "pr"; "files" = $prFileNames}  
$allFiles += @{"directory" = "ideas"; "files" = $ideasFileNames}

$allFiles | ConvertTo-Json -Depth 10 | Out-File -FilePath "file_listing.json"

Write-Host "`nFile listing saved to file_listing.json" -ForegroundColor Cyan