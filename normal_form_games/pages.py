from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from .models import Constants, rand_game, transpose_game
from .models import Constants
import random
import pickle as pkl
import pandas as pd
import json
import numpy as np
import time



def rand_game(size):
    return np.random.randint(10, size=(size,size,2))

def transpose_game(game):
    return np.flip(np.swapaxes(game, 0, 1), 2)

# games_df = pd.DataFrame()
# for i in range(50):
#     row_game = rand_game(3)
#     col_game = transpose_game(row_game)
#     row_choices = []
#     col_choices = []
#     corr = 0
#     games_df = games_df.append({"round":i, "row_game":json.dumps(row_game.tolist()), "col_game":json.dumps(col_game.tolist()), "row":row_choices, "col":col_choices, "corr":corr}, ignore_index=True)
#
# games_df.set_index("round")
games_df = pd.read_pickle("games_df.pkl")


class Choice(Page):
    # timeout_seconds = 60
    form_model = 'player'
    form_fields = ['choice']

    def before_next_page(self):
        if not self.timeout_happened:
            games_df.at[self.round_number,self.player.player_role].append(self.player.choice)

    def vars_for_template(self):
        self.player.game = games_df.at[self.round_number, self.player.player_role + "_game"]
        return {"play_rounds":Constants.num_rounds - 1}

    def is_displayed(self):
        return self.round_number < Constants.num_rounds

    # def vars_for_template(self):
    #     prev = self.player.in_previous_rounds()
    #     return {
    #         'last_choice': prev[-1].choice + 1 if prev else False,
    #     }

class GroupWaitPage(WaitPage):
    pass
    # wait_for_all_groups = True
    group_by_arrival_time = True

    def get_players_for_group(self, players):
        # round = self.round_number
        # if len(games_df[games_df[round] == round])
        if len(players) >= 2:
            p1, p2 = random.sample(players, 2)
            game = rand_game(Constants.size)
            p1.game = json.dumps(game.tolist())
            p2.game = json.dumps(transpose_game(game).tolist())
            return [p1, p2]



class ResultsWaitPage(WaitPage):
    # wait_for_all_groups = True
    group_by_arrival_time = True

    def get_players_for_group(self, players):
        round = self.round_number
        if len(games_df.at[round-1, "row"]) > 0 and len(games_df.at[round-1, "col"]) > 0:
            for player in  players:
                prev_player = player.in_round(self.round_number - 1)
                opp_role = "col" if player.player_role == "row" else "row"
                prev_player.other_choice = random.choice(games_df.at[round-1,opp_role])
                # player.other_choice = random.choice(games_df.at[round-1,opp_role])
                player.set_payoff()
            return players

    def is_displayed(self):
        # return self.round_number < Constants.num_rounds
        return self.round_number > 1
    #
    #
    # def after_all_players_arrive(self):
    #     round = self.round_number
    #     while len(games_df.at[round, "row"]) == 0 or len(games_df.at[round, "col"]) == 0:
    #         time.sleep(5)
    #     for player in  self.group.get_players():
    #         opp_role = "col" if player.role == "row" else "row"
    #         player.other_choice = random.choice(games_df[games_df[round] == round][opp_role])
    #         player.set_payoff()

        # self.group.set_payoffs()
        # for group in self.subsession.get_groups():
        #     group.set_payoffs()
        # self.subsession.group_randomly()


class ResultsSummary(Page):
    # timeout_seconds = 5
    def is_displayed(self):
        # return self.round_number < Constants.num_rounds
        return self.round_number > 1

    def vars_for_template(self):

        return {
            "prev_player":self.player.in_round(self.round_number - 1)
        }
class FinalSummary(Page):
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            games_df.to_pickle("games_df.pkl")
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        cumulative_payoff = sum([p.payoff for p in self.player.in_previous_rounds()])
        return {"cumulative_payoff":cumulative_payoff}

page_sequence = [
    ResultsWaitPage,
    ResultsSummary,
    Choice,
    FinalSummary
]
