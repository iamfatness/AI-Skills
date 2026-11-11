$ErrorActionPreference = 'Stop'
$installer = Join-Path $PSScriptRoot 'framework.py'
& python $installer @args
exit $LASTEXITCODE
