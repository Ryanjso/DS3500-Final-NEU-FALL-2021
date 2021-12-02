import plotly.graph_objects as go


class Visualizer:

    rounds = ["Flop", "Turn", "River"]

    def __init__(self):
        self.player_probabilities = {}

    def add_player(self, username):
        """ Add current players to the dictionary """
        self.player_probabilities[username] = []

    def add_value(self, username, score):
        """ Append hand rank scores as the game progresses """
        if username in self.player_probabilities.keys():
            self.player_probabilities[username].append(score)

    def probability_plot(self):
        """ Plot the hand percentage ranks """
        # Create traces
        fig = go.Figure()

        colors = ['rgb(177,12,21)', 'rgb(2,57,128)']

        # Add data for each player
        ind = 0
        for player, scores in self.player_probabilities.items():
            fig.add_trace(go.Scatter(x=Visualizer.rounds,
                                     y=scores,
                                     mode='lines+markers',
                                     line=dict(color=colors[ind], width=2),
                                     name=player))
            ind += 1

        # Edit the layout
        fig.update_layout(title='Player Hand Percentage Ranks',
                          xaxis_title='Round Name',
                          yaxis_title='Percentage Rank Among all Hands',
                          template='plotly_white',
                          yaxis_tickformat='%',
                          font=dict(
                              family="Courier New, monospace",
                              size=14,
                              color="black"
                            )
                          )

        fig.show()
