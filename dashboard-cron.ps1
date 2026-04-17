# Warehouse Data Dashboard Script
# This script generates a warehouse data dashboard report

Write-Host "=== Warehouse Data Dashboard ===" -ForegroundColor Green
Write-Host "Execution Time: $(Get-Date)" -ForegroundColor Cyan
Write-Host ""

# Get current directory and basic workspace info
$currentDir = Get-Location
$workspacePath = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace"

Write-Host "1. Workspace Information:" -ForegroundColor Yellow
Write-Host "   Current Directory: $currentDir"
Write-Host "   Workspace Path: $workspacePath"
$totalFiles = (Get-ChildItem $workspacePath | Measure-Object).Count
Write-Host "   Total Files: $totalFiles"
Write-Host ""

# Count different types of files
$psFiles = (Get-ChildItem $workspacePath -Filter "*.ps1" | Measure-Object).Count
$mdFiles = (Get-ChildItem $workspacePath -Filter "*.md" | Measure-Object).Count 
$csvFiles = (Get-ChildItem $workspacePath -Filter "*.csv" | Measure-Object).Count
$otherFiles = (Get-ChildItem $workspacePath | Where-Object { $_.Extension -notin @('.ps1', '.md', '.csv', '') } | Measure-Object).Count

Write-Host "2. File Type Statistics:" -ForegroundColor Yellow
Write-Host "   PowerShell Scripts (.ps1): $psFiles"
Write-Host "   Markdown Documents (.md): $mdFiles"
Write-Host "   CSV Files (.csv): $csvFiles"
Write-Host "   Other Files: $otherFiles"
Write-Host ""

# Check recent directories (last 7 days)
$recentDirs = Get-ChildItem $workspacePath | Where-Object { $_.PSIsContainer } | 
              Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } |
              Sort-Object LastWriteTime -Descending

Write-Host "3. Recently Updated Directories (Last 7 days):" -ForegroundColor Yellow
if ($recentDirs.Count -gt 0) {
    foreach ($dir in $recentDirs) {
        Write-Host "   $($dir.Name) - Last Updated: $($dir.LastWriteTime)"
    }
} else {
    Write-Host "   No updated directories in last 7 days"
}
Write-Host ""

# Check recent files (last 24 hours)
$recentFiles = Get-ChildItem $workspacePath | 
               Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) } |
               Sort-Object LastWriteTime -Descending |
               Select-Object -First 10

Write-Host "4. Recently Updated Files (Last 24 hours):" -ForegroundColor Yellow
if ($recentFiles.Count -gt 0) {
    foreach ($file in $recentFiles) {
        Write-Host "   $($file.Name) - Size: $([math]::Round($file.Length/1024, 2)) KB - Updated: $($file.LastWriteTime)"
    }
} else {
    Write-Host "   No updated files in last 24 hours"
}
Write-Host ""

# Check if any specific data files exist
$auditFiles = @("audit-results.csv", "sampled-files-info.csv")
$foundAuditFiles = 0

Write-Host "5. Audit File Status:" -ForegroundColor Yellow
foreach ($file in $auditFiles) {
    $filePath = Join-Path $workspacePath $file
    if (Test-Path $filePath) {
        $fileInfo = Get-Item $filePath
        Write-Host "   ✓ $file - Size: $([math]::Round($fileInfo.Length/1024, 2)) KB"
        $foundAuditFiles++
    } else {
        Write-Host "   ✗ $file - Not Found"
    }
}
Write-Host ""

# Generate summary statistics
Write-Host "6. Data Summary:" -ForegroundColor Yellow
Write-Host "   Total Files: $totalFiles"
Write-Host "   Script Files: $psFiles"
Write-Host "   Document Files: $mdFiles"
Write-Host "   CSV Files: $csvFiles"
Write-Host "   Recent Directories: $($recentDirs.Count)"
Write-Host "   Audit Files Present: $(if ($foundAuditFiles -eq $auditFiles.Count) { 'Yes' } else { 'No' })"
Write-Host ""

Write-Host "=== Dashboard Execution Complete ===" -ForegroundColor Green
Write-Host "Completion Time: $(Get-Date)"