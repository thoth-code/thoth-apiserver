#!/bin/bash

cmd=$1

case "$cmd" in
    ui)
        cd ./ui && npm run dev
        ;;
    mock)
        cd ./mock && npm run dev
        ;;
    *)
        echo "Unknown command '$cmd'"
        exit 1
        ;;

esac