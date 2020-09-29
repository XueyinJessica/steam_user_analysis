
# Collecting Steam Data
## Welcome!
This is a project aiming to collect data from steam. I sampled Steamid and collected player information, selected US players, and got their game inventory. I use this data to analyze game similarity and player behavior.

YOU NEED A Steam API TO RUN THE SCRIPT. Check steam doc [here](https://steamcommunity.com/dev).

## Run The Scripts
- To sample steamid: `$bash entrypoint.sh` you may want to change settings in `entrypoint.sh` and the main pipeline. This may take weeks.
- To got player game inventory for the first time, preprocess the script results and output a list of steamids named `selected_steamid.pickle`, run `$bash owned_game_entrypoint.sh`, you may want to change settings in `owned_game_entrypoint.sh` and the main pipeline. This may take days.
- To track players' behavior (current playing game), preprocess the script results and output a list of steamids named `tracking_steamid.pickle`, run `$bash owned_game_tracking_entrypoint.sh`, you may want to change settings in `bash owned_game_tracking_entrypoint.sh` and the main pipeline. This may take days.


## Results

Work Sample: Game Similarity
With the data I got with steam api, I trained a game embedding to find similar games on steam. You can find the result [here](http://www.jessicawangds.com/steam_game_embedding/).Visualization template: tensorflow [embedding project](https://github.com/tensorflow/embedding-projector-standalone)

