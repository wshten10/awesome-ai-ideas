$content = Get-Content "C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\fengchu-checkin.md" -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [System.Convert]::ToBase64String($bytes)
$base64