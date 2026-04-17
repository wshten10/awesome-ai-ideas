# PowerShell script to list files in awesome-ai-ideas repository directories
# This avoids shell escaping issues with $variables

# Set GitHub repository and directory paths
$repo = "ava-agent/awesome-ai-ideas"
$directories = @("prs", "pr", "ideas")

foreach ($dir in $directories) {
    Write-Host "Listing files in $repo/$dir/"
    
    # Get files using gh api
    $files = gh api repos/$repo/contents/$dir --paginate
    
    # Extract file names
    $fileNames = $files | Where-Object { $_.type -eq "file" } | ForEach-Object { $_.name }
    
    Write-Host "Files found in $dir/:"
    $fileNames | ForEach-Object { Write-Host "  - $_" }
    
    # Save to file for later use
    $fileNames | Out-File -FilePath "files-$dir.txt"
    Write-Host "Saved $($fileNames.Count) files to files-$dir.txt"
}

Write-Host "File listing complete. Ready for sampling."