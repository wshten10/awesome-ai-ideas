# Simple audit without complex syntax
Write-Host "Content Quality Audit Started"

$repo = "ava-agent/awesome-ai-ideas"

# Collect sample files
$files = @()

# Get some root markdown files
$rootFiles = gh api repos/$repo/contents | ConvertFrom-Json | Where-Object { $_.type -eq "file" -and $_.name.EndsWith(".md") }
$rootFiles | ForEach-Object { $files += @{name=$_.name; path=$_.name; dir="root"; url=$_.download_url} }

# Get some docs files  
$docsFiles = gh api repos/$repo/contents/docs | ConvertFrom-Json | Where-Object { $_.type -eq "file" }
$docsFiles | ForEach-Object { $files += @{name=$_.name; path="docs/$($_.name)"; dir="docs"; url=$_.download_url} }

# Get some memory files
$memoryFiles = gh api repos/$repo/contents/memory | ConvertFrom-Json | Where-Object { $_.type -eq "file" }
$memoryFiles | ForEach-Object { $files += @{name=$_.name; path="memory/$($_.name)"; dir="memory"; url=$_.download_url} }

Write-Host "Found $($files.Count) files, sampling 4..."

# Random sample
$sample = $files | Get-Random -Count 4
$sample | ForEach-Object { Write-Host " Selected: $($_.path)" }

# Analyze files
$results = @()
foreach ($file in $sample) {
    Write-Host "`nAnalyzing $($file.path)"
    try {
        $content = Invoke-WebRequest -Uri $file.url -UseBasicParsing
        $text = $content.Content
        
        if ($file.name.EndsWith(".md")) {
            $wordCount = ($text -split ' ').Count
            $lineCount = ($text -split "`n").Count
            $hasIssues = $wordCount -lt 100
            
            $quality = if ($wordCount -gt 1000) { "Excellent" }
            elseif ($wordCount -gt 500) { "Good" }
            elseif ($wordCount -gt 200) { "Fair" }
            else { "Poor" }
            
            $results += @{
                File=$file.name; Path=$file.path; Directory=$file.dir;
                WordCount=$wordCount; LineCount=$lineCount;
                Quality=$quality; Issues=$hasIssues
            }
            
            Write-Host "  Quality: $quality, Words: $wordCount"
        }
        else {
            $results += @{
                File=$file.name; Path=$file.path; Directory=$file.dir;
                Quality="Code"
            }
            Write-Host "  Type: Code file"
        }
    }
    catch {
        Write-Host "  Error reading file"
        $results += @{File=$file.name; Error="Could not read file"}
    }
}

# Save results
$json = $results | ConvertTo-Json -Depth 2 | Out-File -FilePath "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\content-quality-audit.json"
Write-Host "`nResults saved to content-quality-audit.json"
Write-Host "Audit completed"