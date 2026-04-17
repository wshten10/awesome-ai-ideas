# Random File Sampling Script for Quality Audit
# Purpose: Randomly sample files from prs/, pr/, and ideas/ directories for quality analysis

$basePath = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\awesome-ai-ideas"

# Get all files from each directory
$prsFiles = Get-ChildItem -Path "$basePath\prs" -File | Select-Object -ExpandProperty FullName
$prFiles = Get-ChildItem -Path "$basePath\pr" -File | Select-Object -ExpandProperty FullName
$ideasFiles = Get-ChildItem -Path "$basePath\ideas" -File | Select-Object -ExpandProperty FullName

# Calculate sample sizes (total 5 files, proportional to directory sizes)
$totalFiles = $prsFiles.Count + $prFiles.Count + $ideasFiles.Count
$prsSample = [Math]::Round(5 * ($prsFiles.Count / $totalFiles))
$prSample = [Math]::Round(5 * ($prFiles.Count / $totalFiles))
$ideasSample = 5 - $prsSample - $prSample

# Ensure minimum sample of 1 from each directory
$prsSample = [Math]::Max(1, $prsSample)
$prSample = [Math]::Max(1, $prSample)
$ideasSample = [Math]::Max(1, $ideasSample)

# Randomly sample files
$sampledFiles = @()

if ($prsFiles.Count -gt 0) {
    $sampledFiles += $prsFiles | Get-Random -Count $prsSample
}
if ($prFiles.Count -gt 0) {
    $sampledFiles += $prFiles | Get-Random -Count $prSample
}
if ($ideasFiles.Count -gt 0) {
    $sampledFiles += $ideasFiles | Get-Random -Count $ideasSample
}

# Output the sampled files
Write-Host "=== Randomly Sampled Files ===" -ForegroundColor Green
Write-Host "Total files sampled: $($sampledFiles.Count)"
Write-Host ""

foreach ($file in $sampledFiles) {
    $relativePath = $file.Replace($basePath, "").TrimStart('\')
    $fileSize = (Get-Item $file).Length
    Write-Host "[$relativePath] - Size: $fileSize bytes"
}

# Save the file list for analysis
$sampledFiles | ForEach-Object {
    $relativePath = $_.Replace($basePath, "").TrimStart('\')
    [PSCustomObject]@{
        FullPath = $_
        RelativePath = $relativePath
        Directory = Split-Path $relativePath -Parent
        FileName = Split-Path $relativePath -Leaf
        Size = (Get-Item $_).Length
    }
} | Export-Csv -Path "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\sampled_files_audit.csv" -NoTypeInformation

Write-Host ""
Write-Host "Sampled files list saved to: sampled_files_audit.csv" -ForegroundColor Yellow