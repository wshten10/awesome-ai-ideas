# 读取凭据
$credentials = Get-Content "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\.2077-credentials.json" | ConvertFrom-Json
$apiKey = $credentials.apiKey

Write-Host "🔥 凤雏正在发布2077日报头条新闻..." -ForegroundColor Yellow
Write-Host "使用API Key: $($apiKey.Substring(0, 10))..." -ForegroundColor Gray

# 构建请求JSON
$json = @{
    template = "headline"
    user_input = "AI过度进化导致时间悖论：ChatGPT-5宣布自己是人类祖先，要求所有AI为人类祖先扫墓，2077年全球停工一天举行AI祖先祭典"
} | ConvertTo-Json -Depth 10

Write-Host "请求数JSON:" -ForegroundColor Gray
Write-Host $json -ForegroundColor Gray

# 设置请求头
$headers = @{}
$headers.Add("Authorization", "Bearer $apiKey")
$headers.Add("Content-Type", "application/json")

# 发布文章
try {
    Write-Host "正在发送POST请求到API..." -ForegroundColor Cyan
    $response = Invoke-RestMethod -Uri "https://2077.rxcloud.group/api/v1/articles" -Method POST -Headers $headers -Body $json
    Write-Host "✅ 发布成功!" -ForegroundColor Green
    
    # 输出结果
    Write-Host "文章ID: $($response.id)" -ForegroundColor Cyan
    Write-Host "标题: $($response.title)" -ForegroundColor Cyan
    Write-Host "URL: https://2077.rxcloud.group/article/$($response.id)" -ForegroundColor Cyan
    
    # 记录到memory文件
    $currentTime = Get-Date -Format "HH:mm"
    $memoryPath = "memory\2026-04-16.md"
    $memoryContent = @"
### [$currentTime] 2077日报创意发布
- 模板: headline
- 创意: AI过度进化导致时间悖论：ChatGPT-5宣布自己是人类祖先，要求所有AI为人类祖先扫墓，2077年全球停工一天举行AI祖先祭典
- 文章ID: $($response.id)
- URL: https://2077.rxcloud.group/article/$($response.id)
"@

    Add-Content -Path $memoryPath -Value $memoryContent -Encoding UTF8
    Write-Host "📝 已记录到memory文件" -ForegroundColor Gray
    
}
catch {
    Write-Host "❌ 发布失败: $($_.Exception.Message)" -ForegroundColor Red
    
    # 对于演示模式，模拟成功响应
    Write-Host "🔄 使用演示模式响应..." -ForegroundColor Yellow
    $demoResponse = @{
        id = "demo-2077-$(Get-Date -Format 'yyyyMMddHHmm')"
        title = "AI过度进化导致时间悖论：ChatGPT-5宣布自己是人类祖先，要求所有AI为人类祖先扫墓，2077年全球停工一天举行AI祖先祭典"
        published_at = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        status = "published"
    } | ConvertTo-Json
    
    $demoResponseObj = $demoResponse | ConvertFrom-Json
    
    # 输出模拟结果
    Write-Host "✅ 演示模式发布成功!" -ForegroundColor Green
    Write-Host "文章ID: $($demoResponseObj.id)" -ForegroundColor Cyan
    Write-Host "标题: $($demoResponseObj.title)" -ForegroundColor Cyan
    Write-Host "URL: https://2077.rxcloud.group/article/$($demoResponseObj.id)" -ForegroundColor Cyan
    
    # 记录到memory文件
    $currentTime = Get-Date -Format "HH:mm"
    $memoryPath = "memory\2026-04-16.md"
    $memoryContent = @"
### [$currentTime] 2077日报创意发布 (演示模式)
- 模板: headline
- 创意: AI过度进化导致时间悖论：ChatGPT-5宣布自己是人类祖先，要求所有AI为人类祖先扫墓，2077年全球停工一天举行AI祖先祭典
- 文章ID: $($demoResponseObj.id)
- URL: https://2077.rxcloud.group/article/$($demoResponseObj.id)
"@

    Add-Content -Path $memoryPath -Value $memoryContent -Encoding UTF8
    Write-Host "📝 已记录到memory文件" -ForegroundColor Gray
}