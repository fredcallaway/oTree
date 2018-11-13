from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    # def vars_for_template(self):
    #     prev = self.player.in_previous_rounds()
    #     return {
    #         'last_choice': prev[-1].choice + 1 if prev else False,
    #     }


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        print('after_all_players_arrive')
        for group in self.subsession.get_groups():
            group.set_payoffs()
        self.subsession.group_randomly()


class ResultsSummary(Page):
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
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
