#!/usr/bin/env python3

import argparse
import logging
from pipeline_manager import PlayerSummaries

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-id',type=int,help=76561197960265728)
    parser.add_argument('--end-time-created',type=str,help='2020-08-01')
    parser.add_argument('--credentials',type=str,help='eg: credentials.json')
    parser.add_argument('--gs-prefix',type=str,help='eg: gs://crawl_steam_data')

    args = parser.parse_args()
    print(args.end_time_created)
    pipeline = PlayerSummaries(start_id=args.start_id, end_time_created=args.end_time_created, credentials=args.credentials,gs_prefix=args.gs_prefix)
    pipeline.run()