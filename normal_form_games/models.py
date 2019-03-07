from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np
import json
doc = """
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""

class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 8
    stakes = c(100)
    size = 3
    min_time = 10



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['role'] = ["row", "col"][(p.id_in_group % 2)]
                p.participant.vars['treatment'] = [-0.8, 0.8][(int((1 + p.id_in_group)/2) % 2)]
        for p in self.get_players():
            p.player_role = p.participant.vars['role']
            p.treatment = p.participant.vars['treatment']

    # def creating_session(self):
        # self.group_randomly()
        # for group in self.get_groups():
        #     game = rand_game(Constants.size)
        #     print('players', group.get_players())
        #     p1, p2 = group.get_players()
        #     p1.game = json.dumps(game.tolist())
        #     p2.game = json.dumps(transpose_game(game).tolist())


class Group(BaseGroup):
    def set_payoffs(self):
        p1, p2 = self.get_players()
        p1.other_choice = p2.choice
        p2.other_choice = p1.choice

        game = json.loads(p1.game)
        p1.payoff = c(game[p1.choice][p2.choice][0])
        p2.payoff = c(game[p1.choice][p2.choice][1])


class Player(BasePlayer):
    game = models.StringField()
    choice = models.IntegerField()
    other_choice = models.IntegerField()
    player_role = models.StringField()
    treatment = models.FloatField()

    def set_payoff(self):
        prev_player = self.in_round(self.round_number - 1)
        game = json.loads(prev_player.game)
        prev_player.payoff = c(game[prev_player.choice][prev_player.other_choice][0])
        # game = json.loads(self.game)
        # self.payoff = c(game[self.choice][self.other_choice][0])
