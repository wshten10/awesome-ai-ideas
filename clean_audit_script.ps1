# Clean Content Quality Audit Script

Write-Host "=== Content Quality Audit for awesome-ai-ideas Repository ==="
Write-Host "Start Time: $(Get-Date)"

# Count files
$prsFiles = Get-ChildItem "prs" -Filter "*.md" | Select-Object -ExpandProperty Name
$prFiles = Get-ChildItem "pr" -Filter "*.md" | Select-Object -ExpandProperty Name
$ideasFiles = Get-ChildItem "ideas" -Filter "*.md" | Select-Object -ExpandProperty Name

Write-Host "prs/ files: $($prsFiles.Count)"
Write-Host "pr/ files: $($prFiles.Count)" 
Write-Host "ideas/ files: $($ideasFiles.Count)"
Write-Host "Total files: $($prsFiles.Count + $prFiles.Count + $ideasFiles.Count)"

# Sample files
$sampleCount = Get-Random -Minimum 3 -Maximum 6
$allFiles = @()
$allFiles += $prsFiles | ForEach-Object @{ path = $_; directory = "prs"; fullPath = "prs/$_" }
$allFiles += $prFiles | ForEach-Object @{ path = $_; directory = "pr"; fullPath = "pr/$_" }
$allFiles += $ideasFiles | ForEach-Object @{ path = $_; directory = "ideas"; fullPath = "ideas/$_" }

if ($allFiles.Count -gt 0) {
    $actualSampleCount = [Math]::Min($sampleCount, $allFiles.Count)
    $samples = $allFiles | Get-Random -Count $actualSampleCount
    Write-Host "Sampled files:"
    $samples | ForEach-Object { Write-Host "- $($_.directory)/$($_.path)" }
} else {
    Write-Host "No files to sample"
    exit 1
}

# Evaluate files
$results = @()

foreach ($sample in $samples) {
    Write-Host "`nAnalyzing $($sample.fullPath)"
    
    try {
        $content = Get-Content $sample.fullPath -Raw -Encoding UTF8 -ErrorAction Stop
        
        $score = 100
        $issues = @()
        
        # Check structure
        if ($content -notmatch "^# ") { $issues += "No main title"; $score -= 20 }
        if ($content.Length -lt 100) { $issues += "Content too short"; $score -= 15 }
        if ($content -notmatch "##") { $issues += "No sections"; $score -= 15 }
        
        # Check content
        if ($content -notmatch "(code|implementation|api|framework|technology)") { $issues += "Lacks technical details"; $score -= 10 }
        if ($content -notmatch "(use case|example|application)") { $issues += "Missing examples"; $score -= 10 }
        
        # Check format
        $lines = $content -split "`n"
        if ($lines.Count -lt 10) { $issues += "Very short"; $score -= 10 }
        $emptyLines = ($lines | Where-Object { $_.Trim() -eq "" }).Count
        if ($emptyLines / $lines.Count -gt 0.5) { $issues += "Too many empty lines"; $score -= 10 }
        
        # Rating
        $rating = if ($score -ge 90) { "9" } elseif ($score -ge 80) { "8" } elseif ($score -ge 70) { "7" } elseif ($score -ge 60) { "6" } elseif ($score -ge 50) { "5" } elseif ($score -ge 40) { "4" } elseif ($score -ge 30) { "3" } elseif ($score -ge 20) { "2" } elseif ($score -ge 10) { "1" } else { "0" }
        
        $result = @{
            fileName = $sample.path
            directory = $sample.directory
            rating = $rating
            issues = $issues
            score = $score
        }
        
        $results += $result
        Write-Host "Rating: $rating/10, Score: $score/100"
        
    } catch {
        $results += @{
            fileName = $sample.path
            directory = $sample.directory
            rating = "N/A"
            issues = @("Error: $($_.Exception.Message)")
            score = 0
        }
        Write-Host "Error: $($_.Exception.Message)"
    }
}

# Calculate average
$validScores = $results | Where-Object { $_.score -gt 0 }
$avgScore = if ($validScores.Count -gt 0) { [Math]::Round(($validScores | Measure-Object -Property score -Sum).Sum / $validScores.Count, 1) } else { 0 }

Write-Host "`n=== Final Results ==="
Write-Host "Average Score: $avgScore/100"

foreach ($result in $results) {
    Write-Host "$($result.directory)/$($result.fileName): $($result.rating)/10 - $($result.issues -join '; ')"
}

# Save to memory file
$memoryFile = "memory\$(Get-Date -Format 'yyyy-MM-dd').md"
$auditEntry = @"
## [$(Get-Date -Format 'HH:mm')] awesome-ai-ideas Content Quality Audit
- Repository: ava-agent/awesome-ai-ideas (local copy)
- Directory stats: prs/ ($($prsFiles.Count)), pr/ ($($prFiles.Count)), ideas/ ($($ideasFiles.Count)), total: $($prsFiles.Count + $prFiles.Count + $ideasFiles.Count))
- Sampled files: $($samples.Count) files
- Average quality score: $avgScore/100

Per-file ratings:
"@

foreach ($result in $results) {
    $auditEntry += "- $($result.directory)/$($result.fileName): $($result.rating)/10 - $($result.issues -join '; ')`n"
}

$auditEntry += @"
Summary: Content quality audit completed with average score of $avgScore/100.
Recommendations:
1. Implement standardized templates
2. Add technical specifications
3. Include use cases and examples
4. Ensure consistent formatting
5. Remove duplicates
6. Create review process
7. Update outdated technologies
"@

# Append to memory file
if (Test-Path $memoryFile) {
    $existingContent = Get-Content $memoryFile -Raw
    $updatedContent = $existingContent + "`n`n" + $auditEntry
    $updatedContent | Out-File $memoryFile -Encoding UTF8
} else {
    $auditEntry | Out-File $memoryFile -Encoding UTF8
}

Write-Host "`nAudit saved to $memoryFile"