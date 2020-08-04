import collections
import json
import pickle
import pandas as pd
import requests
import sys
import time
import collections
import json
import pickle
import pandas as pd
import requests
import sys
import time
import random
import datetime
from utilities import upload_blob
import gc


class PlayerSummaries:
    def __init__(self,start_id:int,end_time_created:str,credentials:str,gs_prefix:str):
        """
        end_time_created: last account create day
        credentials: path for api key
        gs_prefix: bucket name eg:crawl_steam_data
        """
        #self.start_id=76561197960265728 #first steamid
        
        self.start_id = start_id
        self.end_time_created = datetime.datetime.strptime(end_time_created, "%Y-%m-%d").timestamp()
        self.credentials = credentials
        self.gs_prefix = gs_prefix
        self.i = None
        self.end_time = 0
        self.api_key = None
        self.failure = []
        
        
    def get_api(self):
        with open(self.credentials) as outfile:
            f = json.load(outfile)
            self.api_key = f['api_key']
    def query_summaries(self,steamids:list,api_key):
        query = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamids}'\
            .format(api_key=api_key, steamids=steamids)
        r = requests.get(query)
        data = json.loads(r.text)
        player_summary_batch = data['response']['players']
        return player_summary_batch    
        

    def query_till_limit(self,limit:int,steamids:list,api_key:str):
        """
        query player summaries for a batch, max try: limit
        limit: max try
        steamids: list with all sampled steamids
        api_key:
        """
        attempts = 0
        while attempts < limit:
            try:
                player_summaries = self.query_summaries(steamids,api_key)
                return player_summaries
            except:
                attempts += 1
                if attempts == (limit-1):
                    print('reach limit')
                    time.sleep(600)
                elif attempts == 1:
                    time.sleep(5)
                else:
                    time.sleep(300)
                if attempts == limit:
                    self.failure.append(steamids)
                    with open('data/failure.pickle', 'wb') as handle:
                        pickle.dump(self.failure, handle, protocol=pickle.HIGHEST_PROTOCOL)                    

    def get_last_timecreated(self,player_summaries,prev_timecreated):
        if player_summaries:
            for i in range(len(player_summaries) - 1, -1, -1) :
                try:
                    timecreated = player_summaries[i]['timecreated']
                    if timecreated:
                        return timecreated
                except:
                    pass
        return prev_timecreated                    
                    
                    
    def run(self):
        self.get_api()

        
        sample_ratio=0.004
        batch = int(100/sample_ratio)
        i = 0
        player_summary = []
        
        while self.end_time < self.end_time_created:
            i += 1
            self.i = i
            self.end_id = self.start_id + batch
            steamids = random.sample(range(self.start_id, self.end_id), 100)
            steamids.sort()
            player_summary_batch = self.query_till_limit(limit=5,steamids=steamids,api_key=self.api_key)
            if player_summary_batch:
                self.end_time = self.get_last_timecreated(player_summary_batch,self.end_time)

            else:
                print("reach limit at batch {i}".format(i=i))
            self.start_id = self.end_id
            if player_summary_batch:
                player_summary.extend(player_summary_batch)
                self.player_summary_batch = player_summary_batch

                if i % 100 == 0:
                    pickle_file_name = 'summary_{batch}.pickle'.format(batch=i//100)
                    pickle_file_path = 'data/' + pickle_file_name
                    with open(pickle_file_path, 'wb') as handle:
                        pickle.dump(player_summary, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    
                    player_summary = []
                    upload_blob(self.gs_prefix,pickle_file_path, pickle_file_name)
                    gc.collect()
            time.sleep(10)

        with open('data/summary_{batch}.pickle'.format(batch=(i//100)+1), 'wb') as handle:
            pickle.dump(player_summary, handle, protocol=pickle.HIGHEST_PROTOCOL)
        upload_blob(self.gs_prefix,'data/summary_{batch}.pickle'.format(batch=(i//100)+1),
                    'summary_{batch}.pickle'.format(batch=(i//100)+1))

        try:
            upload_blob(gs_prefix,'data/failure.pickle','failure.pickle')
        except:
            pass