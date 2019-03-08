from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from .models import Constants, rand_game, transpose_game
from .models import Constants
import random
import pickle as pkl
import pandas as pd
import json
import numpy as np

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']


    def vars_for_template(self):
        return {"play_rounds":Constants.num_rounds - 1}

    def is_displayed(self):
        return self.round_number < Constants.num_rounds


class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = "Waiting for other players"

    def get_choices(self,prev_players, role, treatment):
        choices = [p.choice for p in prev_players]
        choices = list(filter(lambda x: x in [0,1,2,3], choices))
        return choices

    def get_players_for_group(self, players):
        round = self.round_number

        players_negative = list(filter(lambda p: p.treatment == "negative", players))
        players_positive = list(filter(lambda p: p.treatment == "positive", players))
        players_to_return = []

        prev_players = players[0].in_round(round -1).get_others_in_subsession()

        row_choices = self.get_choices(prev_players, "row", "negative")
        col_choices = self.get_choices(prev_players, "col", "negative")
        if len(row_choices) > 0 and len(col_choices) > 0:
            for player in  players_negative:
                prev_player = player.in_round(self.round_number - 1)
                opp_choices = col_choices if player.player_role == "row" else row_choices
                prev_player.other_choice = random.choice(opp_choices)
                player.set_payoff()
            players_to_return.extend(players_negative)

        row_choices = self.get_choices(prev_players, "row", "negative")
        col_choices = self.get_choices(prev_players, "col", "negative")
        if len(row_choices) > 0 and len(col_choices) > 0:
            for player in  players_positive:
                prev_player = player.in_round(self.round_number - 1)
                opp_choices = col_choices if player.player_role == "row" else row_choices
                prev_player.other_choice = random.choice(opp_choices)
                player.set_payoff()
            players_to_return.extend(players_positive)
        return players_to_return

    def is_displayed(self):
        return self.round_number > 1


class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number > 1

    def vars_for_template(self):

        return {
            "prev_player":self.player.in_round(self.round_number - 1)
        }
class FinalSummary(Page):
    def is_displayed(self):
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
