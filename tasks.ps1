param([ValidateSet('doctor','init','build','up','ingest','verify','test','analytics','analytics-test','quality','explain','down')][string]$Task = 'doctor')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Invoke-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw "Docker failed (exit $LASTEXITCODE). Review the output above." }
}
switch ($Task) {
    doctor {
        [Environment]::OSVersion.VersionString
        foreach ($tool in @('git','code','docker','gh','python','py')) {
            $found = Get-Command $tool -ErrorAction SilentlyContinue
            if ($found) { Write-Output "$tool : $($found.Source)" }
            else { Write-Output "$tool : not on PATH (Python and gh are optional for Docker execution)" }
        }
        Invoke-Docker version
        Invoke-Docker compose version
        Invoke-Docker info --format '{{.OSType}}'
    }
    init {
        if (Test-Path .env) { Write-Output '.env already exists; preserved.'; break }
        $bytes = New-Object byte[] 32
        $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
        $password = [BitConverter]::ToString($bytes).Replace('-', '').ToLowerInvariant()
        "POSTGRES_DB=energy`nPOSTGRES_USER=energy`nPOSTGRES_PASSWORD=$password" | Set-Content .env -Encoding ascii
        Write-Output 'Created ignored .env with a random local password.'
    }
    build { Invoke-Docker compose build }
    up { Invoke-Docker compose up -d --wait db }
    ingest { Invoke-Docker compose run --rm pipeline energy ingest }
    verify { Invoke-Docker compose run --rm pipeline energy verify }
    test {
        try { Invoke-Docker compose --profile test run --build --rm tests }
        finally { Invoke-Docker compose --profile test stop test-db }
    }
    analytics { Invoke-Docker compose run --build --rm analytics dbt build }
    analytics-test {
        try { Invoke-Docker compose --profile test run --build --rm analytics-tests }
        finally { Invoke-Docker compose --profile test stop test-db }
    }
    quality {
        Invoke-Docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT * FROM analytics.energy_quality_status;"'
    }
    explain {
        Get-Content analytics/queries/explain.sql -Raw | & docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
        if ($LASTEXITCODE -ne 0) { throw 'Query plan inspection failed' }
    }
    down { Invoke-Docker compose --profile test down }
}
