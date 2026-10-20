param([switch]$NoDaemon)
$ErrorActionPreference = 'Stop'
$verificationPrompt = @'
Verify chrome-devtools MCP only. Open https://example.com with new_page in isolatedContext ai-work-skills-verification. Then call take_snapshot with the exact pageId returned. Report the page title and body retrieval result. Wait for user tool approval when requested; never bypass or change approval policies. Do not edit files, run shell commands, use alternate browser tools, or spawn agents. Stop after the two operations and final result.
'@
$cliArgs = @('--ask-for-approval', 'on-request', '--sandbox', 'read-only', '--no-alt-screen', '-C', $PSScriptRoot)
if ($NoDaemon) { $cliArgs = @('--no-daemon') + $cliArgs }
Write-Host 'Review and approve chrome-devtools new_page and take_snapshot in this terminal.'
& codex @cliArgs $verificationPrompt
exit $LASTEXITCODE
