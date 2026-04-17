# PowerShell script to list files in GitHub repository directories
# Fixed to handle JSON structure properly

Write-Host "=== Listing files in ava-agent/awesome-ai-ideas repository ==="

# Function to get files from a directory
function Get-GithubDirFiles {
    param (
        [string]$RepoPath,
        [string]$DirName
    )
    
    Write-Host "`nListing files in $DirName/ directory:"
    try {
        $response = gh api "repos/ava-agent/awesome-ai-ideas/contents/$DirName" --paginate
        
        # Parse JSON response
        $json = $response | ConvertFrom-Json
        
        # Check if it's an array (files list) or object
        if ($json -is [array]) {
            $files = $json | Where-Object { $_.type -eq "file" } | Select-Object -ExpandProperty name
        } elseif ($json.type -eq "dir") {
            $files = $json | Select-Object -ExpandProperty content | Where-Object { $_.type -eq "file" } | Select-Object -ExpandProperty name
        } else {
            $files = @()
        }
        
        if ($files) {
            $files | ForEach-Object { Write-Host "   - $_" }
            Write-Host "   Total: $($files.Count) files"
            return $files
        } else {
            Write-Host "   No files found in $DirName/ directory"
            return @()
        }
    }
    catch {
        Write-Host "   Error accessing $DirName/ directory: $($_.Exception.Message)"
        return @()
    }
}

# Get files from each directory
$prs_files = Get-GithubDirFiles -RepoPath "ava-agent/awesome-ai-ideas" -DirName "prs"
$pr_files = Get-GithubDirFiles -RepoPath "ava-agent/awesome-ai-ideas" -DirName "pr"  
$ideas_files = Get-GithubDirFiles -RepoPath "ava-agent/awesome-ai-ideas" -DirName "ideas"

# Summary
Write-Host "`n=== Summary ==="
Write-Host "prs/ directory: $($prs_files.Count) files"
Write-Host "pr/ directory: $($pr_files.Count) files" 
Write-Host "ideas/ directory: $($ideas_files.Count) files"
Write-Host "Total files: $($prs_files.Count + $pr_files.Count + $ideas_files.Count) files"

# Output PowerShell object for script use
[PSCustomObject]@{
    prs_files = $prs_files
    pr_files = $pr_files
    ideas_files = $ideas_files
    total_count = $prs_files.Count + $pr_files.Count + $ideas_files.Count
}