# PowerShell script to encode file content for GitHub API
$content = Get-Content "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\fengchu-checkin.md" -Raw
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($content))
Write-Output $base64