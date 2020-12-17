#!/bin/bash

function t() {
    OUTPUT="$($1)"
    if [ "${OUTPUT}" != "$2" ]; then
        echo "Got incorrect output for $1:"
        echo $OUTPUT
        exit 1
    fi
}

t "./examples/hello-world.c" "Hello, world!"

echo "All tests passed."
