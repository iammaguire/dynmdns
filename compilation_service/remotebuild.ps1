$projectName = "tdmx"
$codebasePath = "F:\remcomp\codebase"
$buildPath = "F:\remcomp\build"
$outputPath = "F:\remcomp\output"
$tarFilePath = Join-Path -Path $codebasePath -ChildPath "codebase.tar"
$registryHost = "localhost"
$registryPort = "5000"

if (Test-Path -Path $tarFilePath) {
    Write-Host "Found tar archive at $tarFilePath, proceeding with extraction."
    New-Item -ItemType Directory -Force -Path $buildPath
    tar -xvf $tarFilePath -C $buildPath
    Write-Host "Extraction complete."
    Remove-Item -Path $tarFilePath -Force
    Write-Host "Removed tar archive."
    
    Set-Location -Path $buildPath
    Write-Host "Set working directory to $buildPath."
    
    Write-Host "Starting build process using docker-compose."
    docker-compose -f "$buildPath\docker-compose.yml" -p $projectName build
    
    Write-Host "Retrieving service names from the docker-compose configuration."
    $serviceNames = & docker-compose -f "$buildPath\docker-compose.yml" config --services 2>&1
    
    foreach ($service in $serviceNames) {
        $projectNameLower = $projectName.ToLower() 
        $imageName = "${registryHost}:${registryPort}/${projectNameLower}-${service}"
        
        $builtImageName = "${projectNameLower}-${service}"
        
        Write-Host "Tagging built image $builtImageName as $imageName."
        docker tag $builtImageName $imageName
        
        Write-Host "Pushing $imageName to registry."
        docker push $imageName

        if ($?) {
            Write-Host "Pushed $imageName to registry successfully."
        }
        else {
            Write-Error "Failed to push image for service '$service'."
        }
    }

    Write-Host "Marking process completion."
    "" > "$outputPath\done.txt"
}