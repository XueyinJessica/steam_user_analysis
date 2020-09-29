
# Collecting Steam Data
## Welcome!
This is a project aiming to collect data from steam. I sampled Steamid and collected player information, selected US players, and got their game inventory. I use this data to analyze game similarity and player behavior.

YOU NEED A Steam API KEY TO RUN THE SCRIPT. 
You can check steam doc and get a key [here](https://steamcommunity.com/dev).

## Run The Scripts
### Sample Steamid
- To sample steamid: `$bash entrypoint.sh` 
- You may want to change settings in `entrypoint.sh` and the main pipeline. 
- This may take weeks.

### Got Player Game Inventory For the First Time
- Preprocess the script results and output a list of steamids named `selected_steamid.pickle`, 
- Run `$bash owned_game_entrypoint.sh`
- You may want to change settings in `owned_game_entrypoint.sh` and the main pipeline. 
- This may take days.

### Track Players' Current Playing Game
- To track players' current playing game, preprocess the script results and output a list of steamids named `tracking_steamid.pickle`
- Run `$bash owned_game_tracking_entrypoint.sh` every 2 weeks.
- You may want to change settings in `owned_game_tracking_entrypoint.sh` and the main pipeline. 
- This may take days.


## Results

Work Sample: Game Similarity

With the data I got with steam api, I trained a game embedding to find similar games on steam. 

You can find the result [here](http://www.jessicawangds.com/steam_game_embedding/).

Visualization template: tensorflow [embedding project](https://github.com/tensorflow/embedding-projector-standalone).

