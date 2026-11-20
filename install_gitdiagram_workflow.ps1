param(
    [string]$WorkflowPath = (Join-Path $HOME ".gemini\config\global_workflows\auto.md")
)

$ErrorActionPreference = "Stop"
$fragmentPath = Join-Path $PSScriptRoot "AUTO_GITDIAGRAM_WORKFLOW.md"
$marker = "## GitDiagram MCP routing"

if (-not (Test-Path -LiteralPath $WorkflowPath -PathType Leaf)) {
    throw "Global /auto workflow not found: $WorkflowPath. No files were changed."
}
if (-not (Test-Path -LiteralPath $fragmentPath -PathType Leaf)) {
    throw "Workflow fragment not found beside this script: $fragmentPath. No files were changed."
}

$current = [System.IO.File]::ReadAllText($WorkflowPath)
if ($current.Contains($marker)) {
    Write-Host "GitDiagram instructions already exist in the global /auto workflow. No changes made."
    exit 0
}

$fragment = [System.IO.File]::ReadAllText($fragmentPath).Trim()
$backupPath = "$WorkflowPath.bak-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item -LiteralPath $WorkflowPath -Destination $backupPath

$separator = if ($current.EndsWith("`n")) { "`n" } else { "`r`n" }
$updated = $current + $separator + $separator + $fragment + "`r`n"
[System.IO.File]::WriteAllText($WorkflowPath, $updated, [System.Text.UTF8Encoding]::new($false))

$check = [System.IO.File]::ReadAllText($WorkflowPath)
if (-not $check.Contains($marker)) {
    Copy-Item -LiteralPath $backupPath -Destination $WorkflowPath -Force
    throw "Post-write verification failed. Original workflow restored from $backupPath"
}

Write-Host "GitDiagram instructions added to: $WorkflowPath"
Write-Host "Backup created at: $backupPath"
