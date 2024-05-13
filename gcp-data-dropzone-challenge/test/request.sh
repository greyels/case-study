#!/usr/bin/env bash
curl -X POST -F "file_upload=@file.json" https://europe-west3-data-case.cloudfunctions.net/dropzone
