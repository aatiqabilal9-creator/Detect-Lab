# DetectLab - Mandatory Repository Structure Creator (DL-T001)
# Run this from inside your "Detect Lab" project folder

$folders = @(
    "frontend/src/app",
    "frontend/src/features",
    "frontend/src/components",
    "frontend/src/api",
    "frontend/tests",
    "backend/app/api/v1",
    "backend/app/domain",
    "backend/app/services",
    "backend/app/repositories",
    "backend/app/parsers",
    "backend/app/adapters",
    "backend/app/attack",
    "backend/app/validation",
    "backend/app/scoring",
    "backend/app/schemas",
    "backend/app/security",
    "workers/ingestion",
    "workers/normalization",
    "workers/coverage",
    "workers/validation",
    "workers/metrics",
    "workers/deployment",
    "workers/reporting",
    "adapters",
    "validation-fixtures",
    "database/migrations",
    "tests",
    "deployments"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
    New-Item -ItemType File -Force -Path "$folder/.gitkeep" | Out-Null
}

Write-Host "DetectLab mandatory folder structure created successfully." -ForegroundColor Green