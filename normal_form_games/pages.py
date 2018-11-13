from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    def vars_for_template(self):
        prev = self.player.in_previous_rounds()
        return {
            'last_choice': prev[-1].choice + 1 if prev else False,
            'game': self.group.game
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):
    def is_displayed(self):
        return True

    def vars_for_template(self):
        p1, p2 = self.group.get_players()
        p1.other_choice = p2.choice
        p2.other_choice = p1.choice

        return {
            # 'row_choice': p1.choice,
            # 'col_choice': p2.choice
            # 'paying_round': self.session.vars['paying_round'],
            # 'player_in_all_rounds': player_in_all_rounds,
        }


page_sequence = [
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
