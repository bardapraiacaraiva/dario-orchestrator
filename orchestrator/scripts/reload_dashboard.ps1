$ts = [int][double]::Parse((Get-Date -UFormat %s))
Start-Process "http://localhost:8766/dashboard.html?t=$ts"
Write-Host "Dashboard reloaded with cache-bust t=$ts"
