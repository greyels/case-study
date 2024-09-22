#!/usr/bin/env bash
curl -X POST -H "Content-Type: text/plain" --data "text to be moderated" $MODERATE_TEXT_URL
