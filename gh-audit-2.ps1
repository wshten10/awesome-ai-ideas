# PowerShell script for awesome-ai-ideas content audit
# Finds PR- files in root directory and ideas directory

# Set GitHub repository and directory paths
$repo = "ava-agent/awesome-ai-ideas"

# Find PR- files in root directory
$prFilesRoot = @()
$allFiles = gh api repos/$repo/contents --paginate | Where-Object { $_.type -eq "file" -and $_.path -match "^PR-" }

foreach ($file in $allFiles) {
    Write-Host "Found PR file: $($file.path)"
    $prFilesRoot += $file.path
}

# Find files in ideas directory if it exists
$ideasFiles = @()
try {
    $ideasDir = gh api repos/$repo/contents/ideas --paginate
    if ($ideasDir) {
        $ideasFiles = $ideasDir | Where-Object { $_.type -eq "file" }
        foreach ($file in $ideasFiles) {
            Write-Host "Found ideas file: $($file.path)"
        }
    }
} catch {
    Write-Host "No ideas directory or empty"
}

# Output file counts
Write-Host "========================================"
Write-Host "PR- files in root: $($prFilesRoot.Count)"
Write-Host "Files in ideas/: $($ideasFiles.Count)"
Write-Host "========================================"

# Save file lists
$prFilesRoot | Out-File -FilePath "pr-files-root.txt"
$ideasFiles | Select-Object -ExpandProperty path | Out-File -FilePath "ideas-files.txt"

# Randomly sample 4 files total (3 from root PR files, 1 from ideas if available)
Write-Host "Random sampling files for audit..."

$sampledFiles = @()

# Sample from PR- files in root (up to 3)
if ($prFilesRoot.Count -gt 0) {
    $countFromPr = [Math]::Min(3, $prFilesRoot.Count)
    $randomPrFiles = Get-Random -InputObject $prFilesRoot -Count $countFromPr
    $sampledFiles += $randomPrFiles
    Write-Host "Sampled from PR root: $countFromPr files"
}

# Sample from ideas files (1 if available, otherwise take one more from PR)
if ($ideasFiles.Count -gt 0) {
    $countFromIdeas = [Math]::Min(1, $ideasFiles.Count)
    $randomIdeasFile = Get-Random -InputObject $ideasFiles -Count $countFromIdeas | Select-Object -ExpandProperty path
    $sampledFiles += $randomIdeasFile
    Write-Host "Sampled from ideas: $countFromIdeas files"
} elseif ($prFilesRoot.Count -gt $sampledFiles.Count) {
    # If no ideas files, sample one more from PR files
    $additionalPrFile = Get-Random -InputObject $prFilesRoot -Count 1
    $sampledFiles += $additionalPrFile
    Write-Host "Sampled additional PR file"
}

# Save sampled files
$sampledFiles | Out-File -FilePath "sampled-files.txt"

Write-Host "Final sampled files:"
$sampledFiles | ForEach-Object { Write-Host "  - $_" }

Write-Host "Ready for content analysis"