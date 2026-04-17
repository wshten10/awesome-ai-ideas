# Simple script to sample files and fetch content
$repo = "ava-agent/awesome-ai-ideas"

# Sample 4 files randomly from each directory (we'll combine and select from all)
$samples = @(
    # prs directory samples
    @{dir = "prs"; file = "0140-ai-resume-doctor.md"},
    @{dir = "prs"; file = "0421-ai-personal-growth-coach.md"},
    @{dir = "prs"; file = "907-homeworkpeace.md"},
    
    # pr directory samples  
    @{dir = "pr"; file = "2026-04-05-ai-financial-navigation-assistant.md"},
    @{dir = "pr"; file = "PR-944-JusticeKit-AI.md"},
    @{dir = "pr"; file = "ai-multimodal-emotion-assistant-352.md"},
    
    # ideas directory samples
    @{dir = "ideas"; file = "ai-career-soft-skills-coach.md"},
    @{dir = "ideas"; file = "ai-personal-growth-coach.md"},
    @{dir = "ideas"; file = "ai-error-diagnostician.md"}
)

# Randomly select 4 files
$selectedSamples = $samples | Get-Random -Count 4

Write-Host "=== Selected Samples ==="
foreach ($sample in $selectedSamples) {
    Write-Host "[$($sample.dir)/$($sample.file)]"
}

# Create output directory
New-Item -ItemType Directory -Force -Path "sampled_files" | Out-Null

# Fetch content for each selected file
foreach ($sample in $selectedSamples) {
    $filePath = "$($sample.dir)/$($sample.file)"
    $url = "https://raw.githubusercontent.com/$repo/main/$filePath"
    $outputFile = "sampled_files/$($sample.dir)_$($sample.file)"
    
    Write-Host "`nFetching: $filePath"
    
    try {
        $content = Invoke-RestMethod -Uri $url -Method Get
        Set-Content -Path $outputFile -Value $content
        Write-Host "✓ Saved to: $outputFile"
    }
    catch {
        Write-Host "✗ Error fetching $filePath"
        Write-Host "Error: $_"
    }
}

Write-Host "`nSampling completed!"