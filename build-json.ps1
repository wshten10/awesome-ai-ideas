$template = "headline"
$user_input = "AI过度进化导致时间悖论：ChatGPT-5宣布自己是人类祖先，要求所有AI为人类祖先扫墓，2077年全球停工一天举行AI祖先祭典"

$json = @{
    template = $template
    user_input = $user_input
} | ConvertTo-Json -Depth 10

$json