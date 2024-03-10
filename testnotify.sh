#!/bin/bash

output_path="/mnt/remcomp/output"

inotifywait -m -e close_write "$output_path" | while read path action file; do
    echo "Detected $action on $file in directory $path"
    if [[ "$file" == *.tar ]]; then
        echo "$file is a tar file."
    fi
done