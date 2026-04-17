# Simple PowerShell script for file sampling and analysis
Write-Host "=== Content Quality Audit - Simple Version ==="

# Sample specific files for analysis (using fixed files to avoid sampling issues)
$sampled_files = @(
    @{name = "0140-ai-resume-doctor.md"; dir = "prs"},
    @{name = "2026-04-05-ai-financial-navigation-assistant.md"; dir = "pr"},
    @{name = "ai-personal-growth-coach.md"; dir = "ideas"},
    @{name = "0353-ai-orchestration-engine.md"; dir = "prs"}
)

Write-Host "Sampled files for analysis:"
$sampled_files | ForEach-Object { Write-Host "   - $($_.dir)/$($_.name)" }

# Function to analyze a single file
function Analyze-Content {
    param ($file, $dir)
    
    Write-Host "`n=== Analyzing $dir/$file ==="
    
    try {
        $url = "https://raw.githubusercontent.com/ava-agent/awesome-ai-ideas/main/$dir/$file"
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing
        $content = $response.Content
        
        $lines = $content.Split("`n").Count
        $rating = 3  # Default rating
        $issues = @()
        
        # Basic checks
        if ($lines -lt 30) {
            $rating -= 1
            $issues += "Very short content"
        }
        if ($lines -gt 150) {
            $rating += 1
            $issues += "Long content, may need better structure"
        }
        
        if ($content -notmatch "description") {
            $rating -= 1
            $issues += "Missing description"
        }
        
        if ($content -notmatch "features|capabilities") {
            $rating -= 1
            $issues += "Missing features section"
        }
        
        if ($content -match "TODO|FIXME") {
            $rating -= 1
            $issues += "Contains placeholders"
        }
        
        if ($content -match "\d{4}-\d{2}-\d{2}") {
            $issues += "Contains hardcoded dates"
        }
        
        # Final rating bounds
        $rating = [Math]::Max(1, [Math]::Min(5, $rating))
        
        Write-Host "Rating: $rating/5"
        Write-Host "Lines: $lines"
        Write-Host "Issues: $($issues.Count)"
        $issues | ForEach-Object { Write-Host "   - $_" }
        
        return @{
            File = $file
            Dir = $dir
            Rating = $rating
            Lines = $lines
            Issues = $issues
        }
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)"
        return @{
            File = $file
            Dir = $dir
            Error = $_.Exception.Message
        }
    }
}

# Analyze all sampled files
$results = @()
foreach ($fileInfo in $sampled_files) {
    $result = Analyze-Content -file $fileInfo.name -dir $fileInfo.dir
    $results += $result
}

Write-Host "`n=== Summary ==="
$totalRating = 0
$validResults = 0
foreach ($result in $results) {
    if (-not $result.Error) {
        $totalRating += $result.Rating
        $validResults += 1
        Write-Host "$($result.Dir)/$($result.File): $($result.Rating)/5"
    }
}

if ($validResults -gt 0) {
    $avgRating = [Math]::Round($totalRating / $validResults, 1)
    Write-Host "Average rating: $avgRating/5"
}