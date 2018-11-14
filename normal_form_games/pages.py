from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, rand_game, transpose_game
import random

import json

class Choice(Page):
    timeout_seconds = 100
    form_model = 'player'
    form_fields = ['choice']
    # wait_for_all_groups = True

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
        if len(players) >= 4:
            p1, p2 = random.sample(players, 2)
            game = rand_game(Constants.size)
            p1.game = json.dumps(game.tolist())
            p2.game = json.dumps(transpose_game(game).tolist())
            return [p1, p2]
    


class ResultsWaitPage(WaitPage):
    # wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        # for group in self.subsession.get_groups():
        #     group.set_payoffs()
        # self.subsession.group_randomly()


class ResultsSummary(Page):
    timeout_seconds = 5
    def is_displayed(self):
        return True

    def vars_for_template(self):

        return {
            # 'row_choice': p1.choice,
            # 'col_choice': p2.choice
            # 'paying_round': self.session.vars['paying_round'],
            # 'player_in_all_rounds': player_in_all_rounds,
        }


page_sequence = [
    GroupWaitPage,
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
