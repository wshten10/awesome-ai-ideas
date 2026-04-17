# Random File Sampling for Quality Audit
$basePath = "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\awesome-ai-ideas"

# Get all files from the three directories
$prsFiles = Get-ChildItem -Path "$basePath\prs" -File | Select-Object -ExpandProperty Name
$prFiles = Get-ChildItem -Path "$basePath\pr" -File | Select-Object -ExpandProperty Name  
$ideasFiles = Get-ChildItem -Path "$basePath\ideas" -File | Select-Object -ExpandProperty Name

Write-Host "Total files found:"
Write-Host "prs/: $($prsFiles.Count)"
Write-Host "pr/: $($prFiles.Count)" 
Write-Host "ideas/: $($ideasFiles.Count)"

# Random sampling - aim for 4-5 files total
$sampledFiles = @()
$sampledFiles += Get-Random -InputObject $prsFiles -Count 2
$sampledFiles += Get-Random -InputObject $prFiles -Count 1  
$sampledFiles += Get-Random -InputObject $ideasFiles -Count 1

Write-Host "`nSampled files:"
foreach ($file in $sampledFiles) {
    Write-Host "- $file"
}

# Output sampled files to CSV
$sampledFiles | ForEach-Object {
    $directory = ""
    if ($prsFiles -contains $_) { $directory = "prs" }
    elseif ($prFiles -contains $_) { $directory = "pr" }
    elseif ($ideasFiles -contains $_) { $directory = "ideas" }
    
    [PSCustomObject]@{
        FileName = $_
        Directory = $directory
        FullPath = "$basePath\$directory\$_"
    }
} | Export-Csv -Path "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\sampled-files-info.csv" -NoTypeInformation

Write-Host "`nSampled files information saved to CSV"