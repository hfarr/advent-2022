
SESSION="Cookie: session=$(cat SESSION)"

fetchone() {

    DAY="$1"
    fname="${DAY}/problem.html"
    fnameinput="${DAY}/input.txt"

    mkdir -p "${DAY}"
    curl "https://adventofcode.com/2022/day/${DAY}" > "${fname}"
    curl "https://adventofcode.com/2022/day/${DAY}/input" -H "${SESSION}" > "${fnameinput}"

    echo "${fname}"
}

fixfile() {
    
    fname="$1"
    sed -i "s/\/static\/style.css?30/..\/style.css/" "${fname}"
}

# ah loops
# sed pattern %s/\/static\/style.css?30/style.css/

doit() {

    for i in $(seq 10 21); do
        # fetchone "${val}" | read -r TEMP
        # fetchone "${val}"
        TEMP="$(fetchone ${i})"
        echo "$TEMP"
        fixfile "$TEMP"
    done
    
}

fixum() {
    for i in $(seq 10 21); do
        fname="${i}/problem.txt"
        newname="${i}/problem.html"
        mv "$fname" "$newname"
    done
}

