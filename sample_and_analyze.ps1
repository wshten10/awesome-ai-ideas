# PowerShell script to randomly sample files and analyze their content

Write-Host "=== Random Sampling and Content Analysis ==="

# Import previous file lists (simulated - recreate them here)
$prs_files = @(
    "0140-ai-resume-doctor.md", "0146-ai-code-security-auditor-mcp.md", "0153-ai-browser-agent-scheduler.md", 
    "0157-speech-confidence-coach.md", "0178-ai-outfit-advisor.md", "0189-english-speaking-coach.md",
    "0217-ai-file-cabinet-butler.md", "0304-ai-nursing-assistant.md", "0308-ai-neurodiversity-family-ai.md",
    "0353-ai-orchestration-engine.md", "0360-ai-pet-health-guardian.md", "0364-ai-task-orchestrator.md",
    "0388-ai-immersive-language-partner.md", "0391-ai-freelance-life-balance-master.md", "0401-ai-smart-senior-community.md",
    "0421-ai-personal-growth-coach.md", "0676-ai-digital-life-balance-coach.md", "0682-ai-sustainable-living-assistant.md",
    "0819-ai-vision-accessibility-navigator.md", "0868-ai-living-space-design-optimizer.md", "0871-web-knowledge-graph-pipeline.md",
    "0872-ai-learning-path-generator.md", "0873-autonomous-web-testing-framework.md", "0874-ai-multimodal-content-platform.md",
    "0879-formbuddy.md", "0890-nesthunter.md", "0891-lore-master.md", "0893-giftsense.md", "0903-fridgechef.md",
    "0913-menobridge.md", "0914-soundhaven.md", "0919-stylemate.md", "0936-storykeeper.md", "187-viral-title-hunter.md",
    "192-ai-boardgame-rule-translator.md", "196-ai-parking-hunter.md", "199-fitness-form-coach.md", "200-ai-book-digest-assistant.md",
    "204-ai-interview-coach.md", "546-multimodal-reasoning-assistant.md", "660-ai-language-rehabilitation-companion.md",
    "665-emotion-aware-ai-interaction-framework.md", "688-ai-ar-craft-workshop.md", "690-ai-multi-platform-content-adapter.md",
    "692-ai-smart-business-accelerator.md", "697-ai-safety-guardian-for-elderly.md", "713-ai-mental-health-workspace.md",
    "767-ai-decision-coordination.md", "771-ai-community-ecosystem.md", "788-adaptive-prompt-caching-system.md",
    "791-ai-agent-mental-model-framework.md", "792-multi-agent-creative-studio.md", "812-cultural-coordination-platform.md",
    "907-homeworkpeace.md", "909-greenthumb.md", "928-mealforge.md", "934-dreamweave.md", "937-newland-ai.md",
    "941-web-intelligence-agents.md", "AI-File-Cabinet-Manager.md", "ai-browser-agent-orchestrator.md", "ai-procrastination-analyzer.md",
    "ai-rental-guardian.md", "ai-volunteer-management-718.md"
)

$pr_files = @(
    "2026-03-25-ai-icebreaker-coach.md", "2026-03-25-ai-shopping-assistant.md", "2026-03-25-ai-story-world-creator.md",
    "2026-03-26-ai-coffee-flavor-explorer.md", "2026-03-26-ai-promotion-navigator.md", "2026-03-29-ai-cross-platform-content-adapter.md",
    "2026-03-29-ai-smart-environmental-assistant.md", "2026-03-30-ai-clinical-decision-partner-456.md", "2026-03-30-ai-life-rhythm-coach-452.md",
    "2026-03-30-ai-personalized-teaching-assistant-448.md", "2026-03-30-ai-personalized-teaching-assistant-454.md",
    "2026-03-30-ai-pet-mental-health-analyst.md", "2026-03-31-ai-nursing-stress-assistant-467.md", "2026-03-31-ai-retail-transformation-coach-497.md",
    "2026-04-02-co-parenting-coordinator-512.md", "2026-04-02-multimodal-reasoning-assistant-546.md", "2026-04-02-prompt-optimization-engine-542.md",
    "2026-04-05-ai-creative-collaboration-playground.md", "2026-04-05-ai-financial-navigation-assistant.md", "2026-04-05-ai-financial-navigator-assistant.md",
    "2026-04-05-ai-mental-therapy-workstation.md", "2026-04-05-ai-multimodal-business-decision-platform.md", "2026-04-05-ai-neurodiversity-life-coach.md",
    "2026-04-05-ai-senior-digital-mentor.md", "2026-04-05-ai-smart-rental-assistant.md", "2026-04-05-ai-social-anxiety-trainer.md",
    "2026-04-05-ai-startup-accelerator.md", "2026-04-05-transparent-ai-criticism-framework.md", "2026-04-06-ai-smart-agricultural-decision-platform.md",
    "PR-329-AI-Personalized-Learning-Path-Planner.md", "PR-336-AI-World-Simulator.md", "PR-577-AI-Global-Financial-Navigator.md",
    "PR-578-AI-Postpartum-Recovery-Companion.md", "PR-579-AI-Emotional-Archive-Analyst.md", "PR-944-JusticeKit-AI.md",
    "PR-956-VoiceRead-AI.md", "ai-agent-orchestration-engine-353.md", "ai-art-creation-optimizer-630.md", "ai-art-growth-companion.md",
    "ai-career-navigation-official.md", "ai-creative-partner-296.md", "ai-creative-workbench-461.md", "ai-digital-legacy-guardian-514.md",
    "ai-dog-trainer.md", "ai-elderly-care-assistant-513.md", "ai-english-speaking-coach.md", "ai-error-diagnostician-pr-125.md",
    "ai-fitness-gaming-coach-629.md", "ai-intergenerational-translator-pr-97.md", "ai-legal-guide-for-everyone-515.md",
    "ai-multimodal-emotion-assistant-352.md", "ai-neurodiversity-family-assistant-308.md", "ai-nursing-assistant-304.md",
    "ai-personalized-growth-companion-354.md", "ai-pet-health-guardian-360.md", "ai-pet-life-wisdom-steward-468.md",
    "ai-secondhand-pricing-agent.md", "ai-seniors-community-platform-401.md", "ai-smart-accessibility-assistant-396.md",
    "ai-smart-business-advisor-399.md", "ai-smart-family-financial-manager.md", "ai-smart-home-butler-299.md", "ai-spatial-eyes-269.md",
    "digital-skills-coach.md", "edge-ai-deployment-framework-278.md", "knowledge-productizer.md", "pr-605-reasoning-multimodal-assistant.md",
    "pr-606-digital-nutritionist.md", "pr-666-ai-lightweight-gateway.md", "pr-667-ai-global-collaboration-partner.md",
    "pr-669-ai-pet-emotional-guardian.md", "pr-670-ai-senior-home-control.md", "pr-673-ai-parenting-wisdom-companion.md",
    "pr-rural-ai-assistant-548.md", "skincare-advisor.md"
)

$ideas_files = @(
    "ai-appointment-manager.md", "ai-career-soft-skills-coach.md", "ai-contract-reader.md", "ai-daily-briefing.md",
    "ai-digital-declutter-assistant.md", "ai-email-manager.md", "ai-emotional-health-companion.md", "ai-error-diagnostician.md",
    "ai-intergenerational-translator.md", "ai-interview-coach.md", "ai-meeting-health-guardian.md", "ai-meeting-organizer.md",
    "ai-music-creation-companion.md", "ai-outfit-decision-advisor.md", "ai-personal-growth-coach.md", "ai-pet-health-analyst.md",
    "ai-photo-story-generator.md", "ai-pr-summary-analyzer.md", "ai-rights-evidence-assistant.md", "ai-running-coach.md",
    "ai-science-explorer.md", "ai-speaking-companion.md", "ai-subscription-manager.md", "ai-tech-meeting-speaking-coach.md",
    "ai-travel-translator.md", "ai-voice-notes-organizer.md", "code-knowledge-map-generator.md", "energy-assistant.md",
    "gift-recommendation-assistant.md", "moving-assistant.md", "reprice-ai.md", "spaced-repetition-system.md", "voice-notes-structure.md"
)

# Randomly sample 4 files (one from each directory + one extra)
Write-Host "`n=== Random Sampling ==="
$random_prs = Get-Random -InputObject $prs_files -Count 1
$random_pr = Get-Random -InputObject $pr_files -Count 1  
$random_ideas = Get-Random -InputObject $ideas_files -Count 1
$random_extra = Get-Random -InputObject ($prs_files + $pr_files + $ideas_files) -Count 1

$sampled_files = @(
    @{name = $random_prs[0]; dir = "prs"; path = "prs/$($random_prs[0])"},
    @{name = $random_pr[0]; dir = "pr"; path = "pr/$($random_pr[0])"},
    @{name = $random_ideas[0]; dir = "ideas"; path = "ideas/$($random_ideas[0])"},
    @{name = $random_extra[0]; dir = if ($prs_files -contains $random_extra[0]) { "prs" } elseif ($pr_files -contains $random_extra[0]) { "pr" } else { "ideas" }; path = "$($random_extra[0].Split('/')[0])/$($random_extra[0])"}
)

Write-Host "Sampled files:"
$sampled_files | ForEach-Object { Write-Host "   - $($_.dir)/$($_.name)" }

# Function to fetch and analyze file content
function Analyze-GithubFile {
    param (
        [string]$File,
        [string]$Dir
    )
    
    Write-Host "`n=== Analyzing $Dir/$File ==="
    
    try {
        # Fetch file content
        $raw_url = "https://raw.githubusercontent.com/ava-agent/awesome-ai-ideas/main/$Dir/$File"
        $response = Invoke-WebRequest -Uri $raw_url -UseBasicParsing
        $content = $response.Content
        
        # Basic analysis
        $lines = $content.Split([Environment]::NewLine).Count
        $has_description = $content -match "description|Description|DESCRIPTION"
        $has_features = $content -match "features|Features|FEATURES|capabilities|Capabilities|CAPABILITIES"
        $has_tech_stack = $content -match "technology|Technology|TECHNOLOGY|tech stack|Tech Stack|TECH STACK"
        $has_use_cases = $content -match "use cases|Use Cases|USE CASES|examples|Examples|EXAMPLES"
        $has_implementation = $content -match "implementation|Implementation|IMPLEMENTATION|how to|How to|HOW TO"
        
        # Check for technical debt indicators
        $has_hardcoded_dates = $content -match "\d{4}-\d{2}-\d{2}"
        $has_placeholders = $content -match "TODO|FIXME|HACK|XXX|placeholder|Placeholder|PLACEHOLDER"
        $has_duplicate_content = ($content -split '\r?\n' | Group-Object | Where-Object { $_.Count -gt 1 }).Count -gt 0
        
        # Check format consistency
        $has_proper_headers = $content -match "^# "
        $has_markdown_format = $content -match "^\s*[-*+] \s|^\s*\d+\. \s|^\s*\*\*.*\*\*|^\s*__.*__"
        
        # Rating logic (simplified)
        $rating = 0
        $issues = @()
        
        if ($lines -lt 50) { $rating += 1; $issues += "Content appears short (< 50 lines)" }
        if (!$has_description) { $rating += 1; $issues += "Missing description section" }
        if (!$has_features) { $rating += 1; $issues += "Missing features/capabilities section" }
        if (!$has_use_cases) { $rating += 2; $issues += "Missing use cases/examples section" }
        if ($has_hardcoded_dates) { $rating += 1; $issues += "Contains hardcoded dates" }
        if ($has_placeholders) { $rating += 1; $issues += "Contains TODO/FIXME placeholders" }
        if ($lines -gt 200) { $rating += 1; $issues += "Content may be too verbose (> 200 lines)" }
        
        # Ensure rating is between 1-5
        $rating = [Math]::Max(1, [Math]::Min(5, 5 - $rating))
        
        $analysis = @{
            name = $File
            directory = $Dir
            lines = $lines
            rating = $rating
            issues = $issues
            has_description = $has_description
            has_features = $has_features
            has_tech_stack = $has_tech_stack
            has_use_cases = $has_use_cases
            has_implementation = $has_implementation
            has_hardcoded_dates = $has_hardcoded_dates
            has_placeholders = $has_placeholders
            has_duplicate_content = $has_duplicate_content
            has_proper_headers = $has_proper_headers
            has_markdown_format = $has_markdown_format
        }
        
        Write-Host "Rating: $rating/5"
        Write-Host "Lines: $lines"
        Write-Host "Issues: $($issues.Count) found"
        if ($issues.Count -gt 0) {
            $issues | ForEach-Object { Write-Host "   - $_" }
        }
        
        return $analysis
        
    }
    catch {
        Write-Host "Error analyzing $Dir/$File: $($_.Exception.Message)"
        return @{
            name = $File
            directory = $Dir
            error = $_.Exception.Message
        }
    }
}

# Analyze sampled files
$analysis_results = @()
$sampled_files | ForEach-Object {
    $result = Analyze-GithubFile -File $_.name -Dir $_.dir
    $analysis_results += $result
}

# Output results for script processing
[PSCustomObject]@{
    sampled_files = $sampled_files
    analysis_results = $analysis_results
}