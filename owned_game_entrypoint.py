#!/usr/bin/env python3

import argparse
import logging
from owned_game_pipeline import GetOwnedGames

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--credentials',type=str,help='eg: credentials.json')
    parser.add_argument('--gs-prefix',type=str,help='bucket name eg: crawl_steam')

    args = parser.parse_args()
    pipeline = GetOwnedGames(credentials=args.credentials,gs_prefix=args.gs_prefix)
    pipeline.run()