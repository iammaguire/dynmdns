#!/bin/bash

codebase_path="/mnt/remcomp/codebase"
output_path="/mnt/remcomp/output"
destination_path="/opt/dynmdns/out"
wait_time=5
write_wait_time=2
download_marker_path="${output_path}"

mkdir -p "${destination_path}"

wait_until_file_is_stable() {
    local file_path="$1"
    local old_size=-1
    local new_size
    local stable_count=0
    echo "Waiting for $file_path to finish uploading" 
    while (( stable_count < 2 )); do
        new_size=$(stat -c%s "$file_path")
        if [[ "$new_size" == "$old_size" ]]; then
            ((stable_count++))
        else
            stable_count=0
            old_size="$new_size"
        fi
        sleep $write_wait_time
    done
}

download_file() {
    local tar_file="$1"
    local filename=$(basename -- "$tar_file")
    local marker_file="${download_marker_path}/${filename}.downloading"
    if [ -f "$marker_file" ]; then
        return
    fi
    touch "$marker_file"
    echo "Starting download of $tar_file"
    rsync -azhv --progress "$tar_file" "$destination_path/"
    rm "$marker_file"
    # rm "$tar_file"
}

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
echo "Build service has taken codebase. Monitoring $output_path for service images..."
mkdir -p "$destination_path"

while true; do
    for tar_file in "$output_path"/*.tar; do
        if [ ! -e "$tar_file" ]; then
            continue
        fi
        wait_until_file_is_stable "$tar_file" && download_file "$tar_file" &
    done
    sleep $wait_time
done