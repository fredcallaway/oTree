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
    min_time = 10

class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["minimum_players_passed"] = False
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars["failed"] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    game = models.StringField()
    choice_quiz = models.IntegerField()
    other_choice_quiz = models.IntegerField()
    payoff_quiz = models.IntegerField()
    other_payoff_quiz = models.IntegerField()
    correct = models.BooleanField()
    q_num = models.IntegerField()
