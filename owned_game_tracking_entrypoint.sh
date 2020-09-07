#!/bin/bash

mkdir -p data

./owned_game_tracking_entrypoint.py \
--credentials credentials.json \
--gs-prefix crawl_steam