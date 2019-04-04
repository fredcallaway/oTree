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
        min_time = self.session.config["min_time"]
        return {"play_rounds":Constants.num_rounds - 1, "min_time":min_time}

    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        return self.round_number < Constants.num_rounds


class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for another player'
    body_text = '''
        No one else has played this game yet, so we can't match you with
        another player. Please wait until someone else plays this game so that
        we can determine your payoff.
    '''

    def get_choices(self,prev_players, role, treatment):
        prev_players = list(filter(lambda p: p.treatment == treatment and p.player_role == role, prev_players))
        choices = [p.choice for p in prev_players]
        choices = list(filter(lambda x: x in [0,1,2,3], choices))
        return choices

    def get_players_for_group(self, players):
        round = self.round_number

        players_negative = list(filter(lambda p: p.treatment == "negative", players))
        players_positive = list(filter(lambda p: p.treatment == "positive", players))
        players_to_return = []

        prev_players = players[0].in_round(round -1).get_others_in_subsession()
        prev_players.append(players[0].in_round(round -1))
        # prev_players = players[0].in_round(round -1).get_players()

        row_choices = self.get_choices(prev_players, "row", "negative")
        col_choices = self.get_choices(prev_players, "col", "negative")
        if len(row_choices) >= self.session.config["min_plays"] and len(col_choices) >= self.session.config["min_plays"]:
            for player in  players_negative:
                prev_player = player.in_round(self.round_number - 1)
                opp_choices = col_choices if player.player_role == "row" else row_choices
                prev_player.other_choice = random.choice(opp_choices)
                player.set_payoff()
            players_to_return.extend(players_negative)

        row_choices = self.get_choices(prev_players, "row", "positive")
        col_choices = self.get_choices(prev_players, "col", "positive")
        if len(row_choices) >= self.session.config["min_plays"] and len(col_choices) >= self.session.config["min_plays"]:
            for player in  players_positive:
                prev_player = player.in_round(self.round_number - 1)
                opp_choices = col_choices if player.player_role == "row" else row_choices
                prev_player.other_choice = random.choice(opp_choices)
                player.set_payoff()
            players_to_return.extend(players_positive)
        return players_to_return

    def is_displayed(self):
        if self.round_number == 1:
            join_num = self.session.vars["num_assigned"]
            treat, role = self.session.vars["treat_cycle"][join_num % 4]
            self.player.participant.vars["role"] = role
            self.player.participant.vars["treatment"] = treat
            self.session.vars["num_assigned"] = self.session.vars["num_assigned"] + 1

        self.player.treatment = self.player.participant.vars["treatment"]
        self.player.player_role = self.player.participant.vars["role"]

        treat = self.player.treatment
        role = self.player.player_role
        game = self.session.vars[self.round_number][treat][role]
        self.player.game = json.dumps(game.tolist())
        if self.player.participant.vars['failed']:
            return False
        return self.round_number > 1


class ResultsSummary(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        return self.round_number > 1

    def vars_for_template(self):
        return {
            "prev_player": self.player.in_round(self.round_number - 1),
            "earnings": self.participant.payoff.to_real_world_currency(self.session)
        }



class FinalSummary(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        cumulative_payoff = sum([p.payoff for p in self.player.in_previous_rounds()])

        return {
            "cumulative_payoff": cumulative_payoff,
            "earnings": self.participant.payoff.to_real_world_currency(self.session)
        }

page_sequence = [
    ResultsWaitPage,
    ResultsSummary,
    Choice,
    FinalSummary
]
