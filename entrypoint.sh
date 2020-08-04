#!/bin/bash

mkdir -p data

./entrypoint.py \
--start-id 76561197960265728 \
--end-time-created $(date +'%Y-%m-%d') \
--credentials credentials.json \
--gs-prefix crawl_steam