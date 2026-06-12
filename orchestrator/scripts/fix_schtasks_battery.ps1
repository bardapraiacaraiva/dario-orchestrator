# Fix auditoria 2026-06-12: DreamDaily/DreamWeekly/PROMETHEUS falhavam com
# 0x800710E0 porque as tasks tinham "não iniciar se estiver a usar bateria".
# Permite arranque em bateria + StartWhenAvailable (recupera execuções perdidas).

$targets = @(
    @{ Path = '\DARIO\'; Name = 'DreamDaily' },
    @{ Path = '\DARIO\'; Name = 'DreamWeekly' },
    @{ Path = '\';       Name = 'PROMETHEUS Weekly' },
    @{ Path = '\';       Name = 'PROMETHEUS Wave 3 Reminder' }
)

foreach ($x in $targets) {
    $t = Get-ScheduledTask -TaskPath $x.Path -TaskName $x.Name -ErrorAction SilentlyContinue
    if ($t) {
        $t.Settings.DisallowStartIfOnBatteries = $false
        $t.Settings.StopIfGoingOnBatteries = $false
        $t.Settings.StartWhenAvailable = $true
        Set-ScheduledTask -InputObject $t | Out-Null
        Write-Output ("FIXED: " + $x.Path + $x.Name)
    } else {
        Write-Output ("NOT FOUND: " + $x.Name)
    }
}

Write-Output ""
Write-Output "Verificação:"
foreach ($x in $targets) {
    $t = Get-ScheduledTask -TaskPath $x.Path -TaskName $x.Name -ErrorAction SilentlyContinue
    if ($t) {
        Write-Output ("  " + $x.Name + " — DisallowStartIfOnBatteries=" + $t.Settings.DisallowStartIfOnBatteries)
    }
}
