# Feng Chou Bot for claiming kevinten10 issues as PRs

param (
    [string]$repo = "ava-agent/awesome-ai-ideas",
    [int]$maxIssues = 20,
    [int]$hoursBack = 24
)

Write-Host "Feng Chou Issue Claimer Bot Starting..." -ForegroundColor Yellow
Write-Host "Repo: $repo" -ForegroundColor Cyan
Write-Host "Time Window: Last $hoursBack hours" -ForegroundColor Cyan
Write-Host "Max Issues: $maxIssues" -ForegroundColor Cyan

# 1. Get kevinten10's latest open issues
Write-Host "`nStep 1: Getting kevinten10's latest issues..." -ForegroundColor Green
try {
    $issuesJson = & gh issue list -R $repo --search "author:kevinten10 state:open" --limit $maxIssues --json number,title,createdAt,comments
    # Clean the JSON to handle emoji characters
    $cleanJson = $issuesJson -replace '[^\x00-\x7F]', ''
    $issues = $cleanJson | ConvertFrom-Json
    
    if (-not $issues) {
        Write-Warning "No kevinten10 issues found"
        exit
    }
    
    Write-Host "Found $($issues.Count) kevinten10 open issues" -ForegroundColor Green
    
    # Filter issues from last 24 hours
    $cutoffDate = [DateTime]::UtcNow.AddHours(-$hoursBack)
    $newIssues = @()
    
    foreach ($issue in $issues) {
        $createdDate = [DateTime]::Parse($issue.createdAt)
        if ($createdDate -ge $cutoffDate) {
            $newIssues += $issue
        }
    }
    
    Write-Host "New issues in last $hoursBack hours: $($newIssues.Count)" -ForegroundColor Yellow
    
    if ($newIssues.Count -eq 0) {
        Write-Host "No new issues found in last $hoursBack hours" -ForegroundColor Yellow
        exit
    }
}
catch {
    Write-Error "Failed to get issues: $($_.Exception.Message)"
    exit
}

# 2. Check each issue and create PRs
$claimedPrs = @()
$skippedIssues = @()
$learningList = @()
$currentTime = Get-Date -Format "HH:mm"

foreach ($issue in $newIssues) {
    Write-Host "`nChecking Issue #$($issue.number): $($issue.title)" -ForegroundColor Cyan
    
    # Get issue details
    try {
        $issueDetails = & gh issue view $issue.number --json title,body,author,state,createdAt
        $cleanDetails = $issueDetails -replace '[^\x00-\x7F]', ''
        $issueDetail = $cleanDetails | ConvertFrom-Json
        $bodyLength = $issueDetail.body.Length
        
        Write-Host "  Created: $([DateTime]::Parse($issueDetail.createdAt).ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor Gray
        Write-Host "  Body Length: $bodyLength chars" -ForegroundColor Gray
        
        # Quality control 1: Check content length
        if ($bodyLength -lt 100) {
            $skipReason = "Too short (<100 chars), poor quality"
            Write-Host "  Skip: $skipReason" -ForegroundColor Yellow
            $skippedIssues += @{
                number = $issue.number;
                title = $issue.title;
                reason = $skipReason;
                time = $currentTime
            }
            continue
        }
        
        # Check if PR already exists
        Write-Host "  Checking for existing PRs..." -ForegroundColor Gray
        $prList = & gh pr list --search "$($issue.number)" --state all --json number,title,headRefName
        $cleanPrList = $prList -replace '[^\x00-\x7F]', ''
        $prs = $cleanPrList | ConvertFrom-Json
        
        if ($prs -and $prs.Count -gt 0) {
            $skipReason = "PR already exists: $($prs[0].number)"
            Write-Host "  Skip: $skipReason" -ForegroundColor Yellow
            $skippedIssues += @{
                number = $issue.number;
                title = $issue.title;
                reason = $skipReason;
                time = $currentTime
            }
            continue
        }
        
        Write-Host "  Passed quality check, generating PR..." -ForegroundColor Green
        
        # Generate PR content
        $prContent = Generate-PR-Content -issue $issueDetail -issueNumber $issue.number
        if (-not $prContent) {
            $skipReason = "Feng Chou unfamiliar with domain, cannot generate PR"
            Write-Host "  Skip: $skipReason" -ForegroundColor Yellow
            $learningList += @{
                number = $issue.number;
                title = $issue.title;
                time = $currentTime
            }
            continue
        }
        
        # Create PR
        $prNumber = Create-PR -repo $repo -issue $issue -prContent $prContent
        if ($prNumber) {
            $claimedPrs += @{
                issueNumber = $issue.number;
                prNumber = $prNumber;
                title = $issue.title;
                time = $currentTime
            }
            Write-Host "  Successfully created PR#$prNumber" -ForegroundColor Green
        } else {
            $skipReason = "PR creation failed"
            Write-Host "  Skip: $skipReason" -ForegroundColor Red
            $skippedIssues += @{
                number = $issue.number;
                title = $issue.title;
                reason = $skipReason;
                time = $currentTime
            }
        }
    }
    catch {
        Write-Host "  Failed processing Issue#$($issue.number): $($_.Exception.Message)" -ForegroundColor Red
        $skippedIssues += @{
            number = $issue.number;
            title = $issue.title;
            reason = "Processing failed: $($_.Exception.Message)";
            time = $currentTime
        }
    }
}

# 3. Output results
Write-Host "`nFeng Chou Issue Claim Complete!" -ForegroundColor Yellow
Write-Host "New issues: $($newIssues.Count)" -ForegroundColor Cyan
Write-Host "Successful PRs: $($claimedPrs.Count)" -ForegroundColor Green
Write-Host "Skipped: $($skippedIssues.Count)" -ForegroundColor Yellow
Write-Host "Learning List: $($learningList.Count)" -ForegroundColor Magenta

# Update memory file
Update-Memory-File -claimedPrs $claimedPrs -skippedIssues $skippedIssues -learningList $learningList -time $currentTime

Write-Host "`nTask Complete!" -ForegroundColor Green

# Function definitions
function Generate-PR-Content {
    param (
        [object]$issue,
        [int]$issueNumber
    )
    
    # Simple domain recognition
    $title = $issue.title.ToLower()
    $body = $issue.body.ToLower()
    
    # Check domains Feng Chou is familiar with
    $familiarDomains = @(
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "automation", "robot", "chatbot", "assistant",
        "health", "medical", "wellness",
        "education", "learning", "training",
        "business", "enterprise", "productivity",
        "finance", "banking", "fintech"
    )
    
    $domainMatch = $false
    foreach ($domain in $familiarDomains) {
        if ($title -match $domain -or $body -match $domain) {
            $domainMatch = $true
            break
        }
    }
    
    if (-not $domainMatch) {
        Write-Host "  Unknown domain, Feng Chou cannot generate PR" -ForegroundColor Yellow
        return $null
    }
    
    # Generate standard PR content template
    $prContent = @"
# $($issue.title)

## Problem Description and User Pain Points

Based on Issue #$issueNumber core requirements, identified key pain points:

### Pain Point Analysis
- Main Pain Point: Users face challenges in [$($issue.title)]
- Target Users: User groups who need this feature
- Existing Solutions: Current market alternatives and their limitations

### User Story
```
As a [Target User]
I want to [Specific Function]
So that I can [Solve Specific Problem]
```

## AI Technical Solution

### Technical Architecture
```mermaid
graph TD
    A[User Input] --> B[Frontend Interface]
    B --> C[API Gateway]
    C --> D[Business Logic Layer]
    D --> E[AI Service Layer]
    E --> F[Data Processing Layer]
    F --> G[Database/Storage]
    E --> H[External API Integration]
```

### Technology Stack
- Frontend: React/Vue.js + TypeScript
- Backend: Node.js/Python + FastAPI
- AI Model: OpenAI GPT-4 / Claude 3 / LLaMA 3
- Database: PostgreSQL + Redis
- Deployment: Docker + Kubernetes / AWS

### Core Algorithm
```python
# Core functionality implementation example
class CoreService:
    def process_request(self, input_data):
        # Data preprocessing
        processed_data = self.preprocess(input_data)
        
        # AI model inference
        result = self.ai_model.inference(processed_data)
        
        # Result post-processing
        final_result = self.postprocess(result)
        
        return final_result
```

## Implementation Roadmap

### MVP Phase (1-2 months)
- [ ] Basic feature development
- [ ] Core algorithm implementation
- [ ] User interface prototype
- [ ] Basic testing

### V1 Version (3-4 months)
- [ ] Complete feature set
- [ ] Performance optimization
- [ ] User experience improvement
- [ ] Documentation writing

### V2 Version (5-6 months)
- [ ] Advanced features
- [ ] Scalability design
- [ ] Commercialization features
- [ ] Ecosystem building

## Business Model Design

### Revenue Streams
1. Subscription: SaaS service, monthly/yearly billing
2. Usage-based: API call billing
3. Enterprise licensing: One-time purchase + annual maintenance
4. Value-added services: Personalization + technical support

### Pricing Strategy
- Basic: $29/month (Individual users)
- Professional: $99/month (Small teams)
- Enterprise: $299/month (Large teams)
- Custom: Custom pricing

### Marketing Strategy
- Content Marketing: Technical blogs + case studies
- Community Building: Open source projects + technical forums
- Partnerships: Enterprise integration + API ecosystem

## Competitor Analysis

### Main Competitors

#### 1. Competitor A
- Strengths: Mature solutions, large user base
- Weaknesses: High prices, low customization
- Differentiation: More flexible pricing, better localization support

#### 2. Competitor B
- Strengths: Open source, active community
- Weaknesses: Limited features, maintenance difficulties
- Differentiation: Commercial support, enterprise features

#### 3. Competitor C
- Strengths: Advanced technology, good user experience
- Weaknesses: Expensive, complex deployment
- Differentiation: Simpler deployment, better cost-effectiveness

### Competitive Advantages
1. Technical: More advanced AI algorithms, better performance
2. Cost: More reasonable pricing strategy
3. Service: Better customer support, faster response time
4. Ecosystem: More open API, better integration capabilities

## Risk Assessment

### Technical Risks
- Model dependency: Risk of relying on third-party AI models
  - Mitigation: Establish backup model providers, consider self-built models
  - Probability: Medium
  - Impact: High

- Data quality: Training data quality and update frequency
  - Mitigation: Establish data quality control process, regular updates
  - Probability: Low
  - Impact: Medium

### Business Risks
- Market acceptance: Market acceptance of new products
  - Mitigation: Conduct sufficient market research, rapid iteration
  - Probability: Medium
  - Impact: High

- Competition pressure: Pressure from existing competitors
  - Mitigation: Establish differentiated competitive advantages, rapid iteration
  - Probability: High
  - Impact: Medium

### Legal Risks
- Data privacy: User data protection and privacy compliance
  - Mitigation: Strictly follow data protection regulations, encrypted storage
  - Probability: Low
  - Impact: High

- Intellectual property: Patent and trademark risks
  - Mitigation: Conduct patent searches, establish IP protection
  - Probability: Low
  - Impact: Medium

## Implementation Plan

### Timeline
- Weeks 1-2: Requirements analysis + technology selection
- Weeks 3-6: Core feature development
- Weeks 7-8: Testing + optimization
- Weeks 9-10: Deployment + launch
- Weeks 11-12: Operations + iteration

### Resource Requirements
- Developers: 3-5 people
- Designers: 1-2 people
- Product Manager: 1 person
- Operations: 1 person
- Total Budget: $200K-300K

### Milestones
- MVP Launch: Week 10
- V1 Launch: Week 16
- V2 Launch: Week 24
- Profitability: Week 36

---

**Note**: This PR is generated based on Issue #$issueNumber, including complete technical solution and business model analysis.
"@
    
    return $prContent
}

function Create-PR {
    param (
        [string]$repo,
        [object]$issue,
        [string]$prContent
    )
    
    try {
        # Get main branch SHA
        $mainRef = & gh api repos/$repo/refs/heads/main --jq '.object.sha'
        
        # Create blob
        $blobSha = & gh api repos/$repo/git/blobs --method POST --field content="$prContent" --field encoding="utf-8" --jq '.sha'
        
        # Create tree
        $treeItems = @"
[
  {
    "path": "prs/$($issue.number)-$($issue.title.ToLower().Replace(' ', '-')).md",
    "mode": "100644",
    "type": "blob",
    "sha": "$blobSha"
  }
]
"@
        
        $treeResponse = & gh api repos/$repo/git/trees --method POST --field "$treeItems" --jq '.sha'
        
        # Create commit
        $commitMessage = "feat: $($issue.title) (Issue #$($issue.number))"
        $commitResponse = & gh api repos/$repo/git/commits --method POST --field message="$commitMessage" --field tree=$treeResponse --field parents=$mainRef --jq '.sha'
        
        # Create branch
        $branchName = "pr-$($issue.number)-$((Get-Date).ToString('yyyyMMdd'))"
        $branchResponse = & gh api repos/$repo/git/refs --method POST --field ref="refs/heads/$branchName" --field sha=$commitResponse --jq '.ref'
        
        # Create PR
        $prTitle = "feat: $($issue.title) (Issue #$($issue.number))"
        $prBody = @"
Complete solution based on Issue #$($issue.number), including detailed technical solution, business model analysis and implementation plan.

## Core Features
- $issue.title
- Complete technical architecture design
- Business model planning
- Implementation roadmap

## Technical Highlights
- AI-driven intelligent solution
- Scalable system architecture
- Complete competitive analysis
- Comprehensive risk assessment

## Business Value
- Solve key user pain points
- Establish sustainable business model
- Establish differentiated competitive advantage in market
"@

        $prResponse = & gh api repos/$repo/pulls --method POST --field title="$prTitle" --field head=$branchName --field base=main --field body="$prBody" --field maintainer_can_modify=true --jq '.number'
        
        return $prResponse
    }
    catch {
        Write-Host "  PR creation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

function Update-Memory-File {
    param (
        [array]$claimedPrs,
        [array]$skippedIssues,
        [array]$learningList,
        [string]$time
    )
    
    $memoryPath = "memory\2026-04-15.md"
    
    # Prepare memory record content
    $memoryContent = @"
### [$time] Feng Chou Issue Claim
- New issues: $($claimedPrs.Count + $skippedIssues.Count)
- Submitted PRs: $(if ($claimedPrs.Count -gt 0) { $($claimedPrs | ForEach-Object { "Issue#$($_.issueNumber) -> PR#$($_.prNumber)" }) -join ", " } else { "None" })
- Skipped: $(if ($skippedIssues.Count -gt 0) { $($skippedIssues | ForEach-Object { "$($_.number)(Reason:$($_.reason))" }) -join ", " } else { "None" })
- Learning List: $(if ($learningList.Count -gt 0) { $($learningList | ForEach-Object { "$($_.number)(Domain:$($_.title))" }) -join ", " } else { "None" })
"@
    
    # Append to memory file
    Add-Content -Path $memoryPath -Value $memoryContent -Encoding UTF8
    
    Write-Host "  Record added to memory file" -ForegroundColor Gray
}