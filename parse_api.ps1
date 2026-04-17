$issues1 = Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\tmp_issues_p1.json' -Raw | ConvertFrom-Json
$issues2 = Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\tmp_issues_p2.json' -Raw | ConvertFrom-Json
$allIssues = @($issues1) + @($issues2)

Write-Output "=== ISSUES (Total: $($allIssues.Count)) ==="
foreach ($item in $allIssues) {
    $labels = ($item.labels | ForEach-Object { $_.name }) -join ','
    Write-Output "$($item.number)|$($item.state)|$($item.title)|$labels"
}

Write-Output ""
Write-Output "=== PULL REQUESTS ==="

$prs1 = Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\tmp_prs_p1.json' -Raw | ConvertFrom-Json
$prs2 = Get-Content 'C:\Users\admin.DESKTOP-L2K21NT\.openclaw\workspace\tmp_prs_p2.json' -Raw | ConvertFrom-Json
$allPrs = @($prs1) + @($prs2)

Write-Output "Total PRs: $($allPrs.Count)"
foreach ($item in $allPrs) {
    $labels = ($item.labels | ForEach-Object { $_.name }) -join ','
    Write-Output "$($item.number)|$($item.state)|$($item.title)|$labels"
}
