# Random File Selection for Quality Audit
Get-ChildItem prs/*.md | Get-Random -Count 5 | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
Get-ChildItem pr/*.md | Get-Random -Count 5 | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
Get-ChildItem ideas/*.md | Get-Random -Count 5 | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize