# Script to list files in awesome-ai-ideas repository directories
Write-Host "Listing files in awesome-ai-ideas repository..."
Write-Host "============================================="

# Repository information
$repo = "ava-agent/awesome-ai-ideas"
$directories = @("prs", "pr", "ideas")

# Initialize result array
$allFiles = @()

# Process each directory
foreach ($dir in $directories) {
    Write-Host "Listing files in $dir..."
    
    try {
        # Use gh api to get directory contents
        $response = gh api repos/$repo/contents/$dir --paginate
        
        # Convert JSON to PowerShell objects
        $files = $response | ConvertFrom-Json
        
        if ($files -and $files.Count -gt 0) {
            $fileCount = $files.Count
            Write-Host "  Found $fileCount files in $dir"
            
            # Process each file
            foreach ($file in $files) {
                $name = $file.name
                $sha = $file.sha
                $download_url = $file.download_url
                $html_url = $file.html_url
                $size = if ($file.size) { $file.size } else { 0 }
                
                Write-Host "    - $name (Size: $size bytes)"
                
                # Add to results
                $allFiles += [PSCustomObject]@{
                    Name = $name
                    Path = "$dir/$name"
                    Sha = $sha
                    DownloadUrl = $download_url
                    HtmlUrl = $html_url
                    Size = $size
                    Directory = $dir
                }
            }
        } else {
            Write-Host "  No files found in $dir"
        }
    }
    catch {
        Write-Host "  Error processing directory $dir"
    }
}

Write-Host "============================================="
Write-Host "Total files found: $($allFiles.Count)"

# Output results as JSON for easy parsing
$jsonOutput = $allFiles | ConvertTo-Json -Depth 2
Set-Content -Path "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\gh-files-output.json" -Value $jsonOutput
Write-Host "Results saved to gh-files-output.json"