
import plotly.express as px
import pandas as pd

game_tracker = pd.read_csv('game-tracker.csv')

game_tracker = pd.melt(game_tracker, id_vars =['guesses'], 
                        value_vars =['round1', 'round2', 'round3', 'round4', 
                        'round5', 'round6'])
game_tracker = game_tracker.rename({'variable':'round', 'value':'n_words_left'}, axis=1)

fig = px.line(game_tracker, x="round", y="n_words_left", color='guesses', log_y=True)
fig.update_layout(showlegend=False)
fig.show()

