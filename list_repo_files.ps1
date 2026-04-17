# Script to list files in prs/, pr/, and ideas/ directories via gh API
$repo = "ava-agent/awesome-ai-ideas"

# Function to get directory contents
function Get-GithubDirContents {
    param (
        [string]$path
    )
    $url = "https://api.github.com/repos/$repo/contents/$path"
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Get
        return $response | Where-Object { $_.type -eq "file" } | Select-Object -ExpandProperty name
    }
    catch {
        Write-Host "Error fetching $path contents: $_"
        return @()
    }
}

# Get files from each directory
Write-Host "Fetching repository contents..."

$prsFiles = Get-GithubDirContents "prs"
$prFiles = Get-GithubDirContents "pr"  
$ideasFiles = Get-GithubDirContents "ideas"

# Display stats
Write-Host "`n=== Directory Statistics ==="
Write-Host "prs/ directory files: $($prsFiles.Count)"
Write-Host "pr/ directory files: $($prFiles.Count)"
Write-Host "ideas/ directory files: $($ideasFiles.Count)"
Write-Host "Total files: $($prsFiles.Count + $prFiles.Count + $ideasFiles.Count)"

# Write stats to file for later use
$stats = @"
prs_files: $($prsFiles.Count)
pr_files: $($prFiles.Count)  
ideas_files: $($ideasFiles.Count)
total_files: $($prsFiles.Count + $prFiles.Count + $ideasFiles.Count)
"@

Set-Content -Path "repo_stats.txt" -Value $stats

Write-Host "`n=== Sample Files ==="
Write-Host "prs/ files: $($prsFiles -join ', ')"
Write-Host "pr/ files: $($prFiles -join ', ')"  
Write-Host "ideas/ files: $($ideasFiles -join ', ')"