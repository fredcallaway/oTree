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
    players_per_group = 2
    num_rounds = 4
    stakes = c(100)
    size = 3


def rand_game(size):
    return np.random.randint(10, size=(size,size,2))

def transpose_game(game):
    return np.flip(np.swapaxes(game, 0, 1), 2)

class Subsession(BaseSubsession):
    def creating_session(self):
        # self.group_randomly()
        for group in self.get_groups():
            game = rand_game(Constants.size)
            p1, p2 = group.get_players()
            p1.game = json.dumps(game.tolist())
            p2.game = json.dumps(transpose_game(game).tolist())


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
