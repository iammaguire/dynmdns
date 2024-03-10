#!/bin/bash

codebase_path="/mnt/remcomp/codebase"
output_path="/mnt/remcomp/output"
destination_path="/opt/dynmdns/out"

mkdir -p "${destination_path}"
echo "Compressing codebase"
tar --exclude='src/.git' -czf ./codebase.tar -C src .
total_size=$(du -bs ./codebase.tar | cut -f1)
echo "Codebase compressed size: $total_size bytes"
echo "Copying codebase to remote"
rsync -azh --progress ./codebase.tar "$codebase_path"
rm ./codebase.tar
echo "Waiting for build service to detect..."
while [ "$(ls -A "$codebase_path")" ]; do
    sleep 1 
done
echo "Build service has taken codebase"