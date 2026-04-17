# Phoenix Log Sync Script
param(
    [string]$RemoteContent,
    [string]$Sha,
    [string]$LocalLog
)

Write-Host "=== Phoenix Log Sync Script ==="
Write-Host "Remote content length: $($RemoteContent.Length)"
Write-Host "Local log length: $($LocalLog.Length)"

# Check for existing Phoenix section in remote content
$phoenixMarker = "## 🔥 凤雏"
$phoenixIndex = $RemoteContent.IndexOf($phoenixMarker)

if ($phoenixIndex -eq -1) {
    Write-Host "No existing Phoenix section found in remote log"
    $hasPhoenixSection = $false
} else {
    Write-Host "Found existing Phoenix section at position: $phoenixIndex"
    $hasPhoenixSection = $true
}

# Extract Phoenix entries from local log
$phoenixEntries = @()
$lines = $LocalLog -split "`n"

foreach ($line in $lines) {
    if ($line -match "凤雏" -or $line -match "🔥") {
        $phoenixEntries += $line
    }
}

if ($phoenixEntries.Length -gt 0) {
    Write-Host "Found $($phoenixEntries.Length) Phoenix entries in local log"
    $phoenixSection = $phoenixEntries -join "`n"
    
    # Create the formatted Phoenix section
    $formattedPhoenixSection = "## 🔥 凤雏(wshten10)日志`n$phoenixSection"
    
    if (-not $hasPhoenixSection) {
        # Append Phoenix section to remote content
        $mergedContent = "$RemoteContent`n`n$formattedPhoenixSection"
        $operation = "Appended"
    } else {
        # Replace existing Phoenix section
        $beforePhoenix = $RemoteContent.Substring(0, $phoenixIndex)
        $afterPhoenix = $RemoteContent.Substring($phoenixIndex + $formattedPhoenixSection.Length)
        $mergedContent = "$beforePhoenix$formattedPhoenixSection$afterPhoenix"
        $operation = "Replaced"
    }
    
    Write-Host "Merged content length: $($mergedContent.Length)"
    Write-Host "Operation: $operation"
    
    return @{
        Content = $mergedContent
        Success = $true
        Operation = $operation
        PhoenixEntriesCount = $phoenixEntries.Length
    }
} else {
    Write-Host "No Phoenix entries found in local log"
    return @{
        Content = $RemoteContent
        Success = $false
        Operation = "NoPhoenixEntries"
        PhoenixEntriesCount = 0
    }
}