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
logging.basicConfig(filename='crawl_owned_games_tracking.log',level=logging.INFO)
log_handler = logging.FileHandler('crawl_owned_games_tracking.log')
log_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger('crawl_owned_games_tracking.log')
logger.addHandler(log_handler)


class GetOwnedGames:
    def __init__(self,credentials,gs_prefix):
        #self.steamids = steamids # list of selected steamids
        self.credentials = credentials
        self.gs_prefix = gs_prefix
        self.user_game_info = []
        self.starting_date = datetime.today().strftime("%Y%m%d")
        
    def get_steamids(self):
        with open('tracking_steamid.pickle', 'rb') as f:
            self.steamids = pickle.load(f)


    def get_api(self):
        with open(self.credentials) as outfile:
            f = json.load(outfile)
            self.api_key = f['api_key']     
        
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
        
    def query_till_limit(self,limit:int,steamid:str):
        """
        query player summaries for a batch, max try: limit
        limit: max try
        steamids: list with all sampled steamids
        api_key:
        """
        attempts = 0
        while attempts < limit:
            try:
                owned_game = self.query(steamid)
                return owned_game
            except:
                attempts += 1
                if attempts == (limit-1):
                    logging.info('reach limit at i ={i}'.format(i=limit))
                    time.sleep(600)
                elif attempts == 1:
                    time.sleep(10)
                else:
                    logging.info('{n}th attempt for player {steamid}'.format(n=attempts,steamid=steamid))
                    time.sleep(210)

    
    def run(self):
        self.get_steamids()
        self.get_api()
        print(self.steamids[0])
        #progress
        i = 1
        # no response count
        for steamid in self.steamids:
            self.query_till_limit(5,steamid)
            if self.c % 10 == 0:
                pickle_file_name = 'owned_game_{starting_date}_{batch}.pickle'.format(starting_date=self.starting_date,batch=self.c//10)
                pickle_file_path = 'data/' + pickle_file_name
                with open(pickle_file_path, 'wb') as handle:
                    pickle.dump(self.user_game_info, handle, protocol=pickle.HIGHEST_PROTOCOL)
                upload_blob(self.gs_prefix,pickle_file_path, pickle_file_name)
                self.user_game_info = []
            i += 1
        with open(pickle_file_path, 'wb') as handle:
            pickle_file_name = 'owned_game_{starting_date}_{batch}.pickle'.format(starting_date=self.starting_date,batch=(self.c//10)+1)
            pickle.dump(self.user_game_info, handle, protocol=pickle.HIGHEST_PROTOCOL)
