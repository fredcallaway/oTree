from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'lobby'
    players_per_group = None
    num_rounds = 10
    size = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    game = models.StringField()
    choice = models.IntegerField()
    other_choice = models.IntegerField()
    payoff = models.IntegerField()
    other_payoff = models.IntegerField()
    correct = models.BooleanField()
    q_num = models.IntegerField()

