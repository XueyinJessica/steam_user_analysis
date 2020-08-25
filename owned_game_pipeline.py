import gc
import glob
import json
import requests
import pickle
import time
from datetime import datetime
from utilities import upload_blob


import logging
log_format = "%(asctime)s %(name)s %(funcName)s %(message)s"
logging.basicConfig(filename='crawl_owned_games.log',level=logging.INFO)
log_handler = logging.FileHandler('crawl_owned_games.log')
log_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger('crawl_owned_games.log')
logger.addHandler(log_handler)


class GetOwnedGames:
    def __init__(self,credentials,gs_prefix):
        #self.steamids = steamids # list of selected steamids
        self.credentials = credentials
        self.speed = 12
        self.c = 0  # count seccess
        self.cn = 0 # count no response
        self.gs_prefix = gs_prefix
        self.user_game_info = []
        
    def get_steamids(self):
        summaries = glob.glob("data/summary_*.pickle")
        all_summaries = []
        for summary in summaries:
            with open(summary, 'rb') as f:
                y = pickle.load(f)
            all_summaries.extend(y)
        us_visible = []
        for player in all_summaries:
            if player['communityvisibilitystate'] == 3:
                try:
                    if player['loccountrycode'] == 'US':
                        us_visible.append(player)
                except:
                    pass
        us_id = [player['steamid'] for player in us_visible]
        self.steamids = us_id
        
        logger.info('got steamid, total steamids: {ts}'.format(ts=len(self.steamids)))

    def get_api(self):
        with open(self.credentials) as outfile:
            f = json.load(outfile)
            self.api_key = f['api_key']
        logger.info('set api key')
        
    def query(self,steamid):
        """
        query 1 player and sleep for n seconds
        """
        query_get_game = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid}&include_played_free_games=1&format=json".format(api_key=self.api_key,steamid=steamid)
        r = requests.get(query_get_game)
        data = json.loads(r.text)
        if data['response']:
            self.c += 1
            self.cn = 0
            self.user_game_info.append((steamid,data['response']))
        else:
            self.cn += 1
        time.sleep(self.speed)
    
    def run(self):
        self.get_api()
        self.get_steamids()
        #progress
        i = 0
        # no response count
        for steamid in self.steamids:
            i += 1
            self.query(steamid)
            if self.cn == 30:
                time.sleep(300)
            if self.cn == 50:
                time.sleep(600)
            if self.c % 10 == 0:
                logger.info('got {i} players data'.format(i=self.c))
                pickle_file_name = 'owned_game_{batch}.pickle'.format(batch=self.c//10)
                pickle_file_path = 'data/' + pickle_file_name
                with open(pickle_file_path, 'wb') as handle:
                    pickle.dump(self.user_game_info, handle, protocol=pickle.HIGHEST_PROTOCOL)
                upload_blob(self.gs_prefix,pickle_file_path, pickle_file_name)
                self.user_game_info = []
                gc.collect()