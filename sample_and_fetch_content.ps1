# Script to randomly sample 3-5 files and fetch their content
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

# Function to fetch file content
function Get-GithubFileContent {
    param (
        [string]$filePath
    )
    $url = "https://raw.githubusercontent.com/$repo/main/$filePath"
    
    try {
        $response = Invoke-RestMethod -Uri $url -Method Get
        return $response
    }
    catch {
        Write-Host "Error fetching $filePath content: $_"
        return ""
    }
}

# Get all files from each directory
$prsFiles = Get-GithubDirContents "prs"
$prFiles = Get-GithubDirContents "pr"  
$ideasFiles = Get-GithubDirContents "ideas"

# Combine all files and sample 3-5 files
$allFiles = @()
$allFiles += $prsFiles | ForEach-Object { @{name = $_; dir = "prs"} }
$allFiles += $prFiles | ForEach-Object { @{name = $_; dir = "pr"} }
$allFiles += $ideasFiles | ForEach-Object { @{name = $_; dir = "ideas"} }

# Randomly sample 4 files (between 3-5)
$numSamples = Get-Random -Minimum 3 -Maximum 6
$sampledFiles = $allFiles | Get-Random -Count $numSamples

Write-Host "=== Sampled $numFiles files ==="
foreach ($file in $sampledFiles) {
    Write-Host "[$($file.dir)/$($file.name)]"
}

# Fetch and save content for each sampled file
$samplesDir = "sampled_files"
New-Item -ItemType Directory -Force -Path $samplesDir | Out-Null

$contentData = @()
foreach ($file in $sampledFiles) {
    $filePath = "$($file.dir)/$($file.name)"
    Write-Host "`nFetching content for: $filePath"
    
    $content = Get-GithubFileContent $filePath
    if ($content) {
        $fileObj = @{
            name = $file.name
            dir = $file.dir
            path = $filePath
            content = $content
        }
        $contentData += $fileObj
        
        # Save to file
        $outFile = "$samplesDir/$($file.dir)_$($file.name)"
        Set-Content -Path $outFile -Value $content
        Write-Host "Saved to: $outFile"
    }
}

# Save sample metadata
$sampleMeta = $contentData | ConvertTo-Json -Depth 3
Set-Content -Path "sample_metadata.json" -Value $sampleMeta
Write-Host "`nSaved sample metadata to sample_metadata.json"