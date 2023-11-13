directory="./benchmarks_out"

# Use a for loop to iterate through the files in the directory
# and add them to an array
file_list=()
for file in "$directory"/*.riscv; do  # /* is for pattern matching
    if [ -f "$file" ]; then
        file_list+=("$file")
    fi
done

echo "[INFO] Start simulation"

for file in "${file_list[@]}"; do
    echo "[INFO] Running ${file}..."
    make CONFIG=LargeBoomConfig run-binary BINARY="$file"
done

