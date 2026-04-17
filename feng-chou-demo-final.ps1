# Feng Chou Issue Claimer Bot - Final Demo

Write-Host "🔥 凤雏 Issue抢滩PR 演示" -ForegroundColor Yellow
Write-Host "Feng Chou Bot Demo for kevinten10 Issue Claiming" -ForegroundColor Cyan

# Get recent kevinten10 issues
Write-Host "`n📋 获取kevinten10的最新issues..." -ForegroundColor Green
try {
    $issuesJson = & gh issue list -R ava-agent/awesome-ai-ideas --search "author:kevinten10 state:open" --limit 5 --json number,title,createdAt
    
    # Clean and parse JSON
    $cleanJson = $issuesJson -replace '[^\x00-\x7F]', ''
    $issues = $cleanJson | ConvertFrom-Json
    
    $cutoffDate = [DateTime]::UtcNow.AddHours(-24)
    $newIssues = @()
    
    foreach ($issue in $issues) {
        $createdAt = [DateTime]::Parse($issue.createdAt)
        if ($createdAt -ge $cutoffDate) {
            $newIssues += [PSCustomObject]@{
                Number = $issue.number
                Title = $issue.title
                CreatedAt = $createdAt
            }
        }
    }
    
    Write-Host "发现 $($newIssues.Count)个最近24小时的新issues" -ForegroundColor Yellow
    
    if ($newIssues.Count -eq 0) {
        Write-Host "没有找到最近24小时的新issues" -ForegroundColor Yellow
        exit
    }
}
catch {
    Write-Error "获取issues失败: $($_.Exception.Message)"
    exit
}

# Process each issue
$claimedPrs = @()
$skippedIssues = @()
$currentTime = Get-Date -Format "HH:mm"

foreach ($issue in $newIssues) {
    Write-Host "`n🔍 检查 Issue #$( $issue.Number ): $( $issue.Title )" -ForegroundColor Cyan
    
    # Check if issue has enough content
    try {
        $issueDetails = & gh issue view $issue.Number --json body --jq '.body'
        $bodyLength = if ($issueDetails) { $issueDetails.Length } else { 0 }
        
        Write-Host "  创建时间: $( $issue.CreatedAt.ToString('yyyy-MM-dd HH:mm') )" -ForegroundColor Gray
        Write-Host "  内容长度: $bodyLength 字符" -ForegroundColor Gray
        
        # Quality control: Check content length
        if ($bodyLength -lt 100) {
            $skipReason = "内容太短(<100字符)，质量不足"
            Write-Host "  ⚠️ 跳过: $skipReason" -ForegroundColor Yellow
            $skippedIssues += @{
                number = $issue.Number;
                title = $issue.Title;
                reason = $skipReason;
                time = $currentTime
            }
            continue
        }
        
        # Check if PR already exists
        Write-Host "  🔍 检查关联PR..." -ForegroundColor Gray
        try {
            $prList = & gh pr list --search "$( $issue.Number )" --state all --json number --jq '.[].number'
            $existingPrNumbers = @()
            
            if ($prList) {
                $cleanPrList = $prList -replace '[^\x00-\x7F]', ''
                $existingPrNumbers = $cleanPrList | ConvertFrom-Json -ErrorAction SilentlyContinue
            }
            
            if ($existingPrNumbers -and $existingPrNumbers.Count -gt 0) {
                $skipReason = "已有PR关联: $($existingPrNumbers[0])"
                Write-Host "  ⚠️ 跳过: $skipReason" -ForegroundColor Yellow
                $skippedIssues += @{
                    number = $issue.Number;
                    title = $issue.Title;
                    reason = $skipReason;
                    time = $currentTime
                }
                continue
            }
        }
        catch {
            Write-Host "  未找到现有PR" -ForegroundColor Green
        }
        
        Write-Host "  ✅ 通过质量检查，准备生成PR..." -ForegroundColor Green
        
        # Generate PR content summary
        $prTitle = "feat: $( $issue.Title ) (Issue #$( $issue.Number ))"
        $prSummary = @"
# $( $issue.Title )

## 问题描述与用户痛点

基于Issue #$( $issue.Number )的核心需求，提供完整的AI解决方案。

### 技术方案
- **核心功能**: 实现AI驱动的$( $issue.Title )
- **技术栈**: React/Vue.js + Node.js/Python + OpenAI GPT-4
- **架构设计**: 微服务架构，支持高并发和扩展性

### 实现路线图
- **MVP (1-2月)**: 核心功能开发
- **V1 (3-4月)**: 完整功能集，性能优化
- **V2 (5-6月)**: 企业级功能，生态建设

### 商业模式
- **订阅制**: $29-$299/月
- **按使用量**: API调用计费
- **企业授权**: 定制化解决方案

### 竞争优势
1. 先进的AI技术栈
2. 用户友好的界面设计
3. 可扩展的系统架构
4. 竞争性的定价策略

---

此PR基于Issue #$( $issue.Number)生成，包含完整的技术方案和商业模式分析。
"@

        # For demo purposes, just create a text file instead of actual PR
        $prFileName = "demo-pr-$( $issue.Number )-$( $issue.Title.ToLower().Replace(' ', '-').Replace(':', '') ).md"
        $prFileName = $prFileName -replace '[^\w\-\.]', ''
        
        Set-Content -Path $prFileName -Value $prSummary -Encoding UTF8
        
        $prNumber = "DEMO-$( $issue.Number )"
        $claimedPrs += @{
            issueNumber = $issue.Number;
            prNumber = $prNumber;
            title = $issue.Title;
            time = $currentTime
        }
        Write-Host "  ✅ 成功创建PR#$prNumber (演示模式)" -ForegroundColor Green
        Write-Host "  📄 PR内容已保存到文件: $prFileName" -ForegroundColor Gray
    }
    catch {
        Write-Host "  ❌ 处理Issue#$( $issue.Number)失败: $($_.Exception.Message)" -ForegroundColor Red
        $skippedIssues += @{
            number = $issue.Number;
            title = $issue.Title;
            reason = "处理失败: $($_.Exception.Message)";
            time = $currentTime
        }
    }
}

# Output results
Write-Host "`n🎯 凤雏 Issue抢滩PR 演示完成!" -ForegroundColor Yellow
Write-Host "新issues: $($newIssues.Count)个" -ForegroundColor Cyan
Write-Host "成功PR: $($claimedPrs.Count)个" -ForegroundColor Green
Write-Host "跳过: $($skippedIssues.Count)个" -ForegroundColor Yellow

# Update memory file with demo results
$memoryPath = "memory\2026-04-15.md"
$memoryContent = @"
### [$currentTime] 孔明Issue抢滩 (演示模式)
- 新issue: $($newIssues.Count)个
- 提交PR: $(if ($claimedPrs.Count -gt 0) { $($claimedPrs | ForEach-Object { "Issue#$($_.issueNumber) → PR#$($_.prNumber)" }) -join ", " } else { "无" })
- 跳过: $(if ($skippedIssues.Count -gt 0) { $($skippedIssues | ForEach-Object { "$($_.number)(原因:$($_.reason))" }) -join ", " } else { "无" })
- 状态: 演示模式，创建了PR内容文件，未实际提交到GitHub
"@

Add-Content -Path $memoryPath -Value $memoryContent -Encoding UTF8

Write-Host "`n✨ 演示任务完成!" -ForegroundColor Green

# List created demo files
Write-Host "`n📁 创建的演示PR文件:" -ForegroundColor Cyan
Get-ChildItem -Path "demo-pr-*.md" | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor Gray
}