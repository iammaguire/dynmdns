$projectName = "tdmx"
$codebasePath = "F:\remcomp\codebase"
$buildPath = "F:\remcomp\build"
$outputPath = "F:\remcomp\output"
$tarFilePath = Join-Path -Path $codebasePath -ChildPath "codebase.tar"

if (Test-Path -Path $tarFilePath) {
    New-Item -ItemType Directory -Force -Path $buildPath
    tar -xvf $tarFilePath -C $buildPath
    Remove-Item -Path $tarFilePath -Force
    Set-Location -Path $buildPath
    docker-compose -f "$buildPath\docker-compose.yml" -p $projectName build
    $serviceNames = docker-compose -f "$buildPath\docker-compose.yml" config --services
    foreach ($service in $serviceNames) {
        $projectName = [IO.Path]::GetFileName($buildPath).ToLower() 
        $imageName = "${projectName}-${service}"
        
        $exactImageNameWithTag = docker images --format "{{.Repository}}:{{.Tag}}" | Where-Object { $_ -like "$imageName*" } | Select-Object -First 1

        if ($null -ne $exactImageNameWithTag) {
            $tarOutputPath = Join-Path -Path $outputPath -ChildPath "$service.tar"
            docker save -o $tarOutputPath $exactImageNameWithTag
            Write-Output "Exported $exactImageNameWithTag to $tarOutputPath"
        }
        else {
            Write-Warning "Image for service '$service' not found. Skipping..."
        }
    }

    echo '' > "$outputPath\done.txt"
}