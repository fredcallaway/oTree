from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    def vars_for_template(self):
        prev = self.player.in_previous_rounds()
        return {
            'last_choice': prev[-1].choice + 1 if prev else False
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        last_round = player_in_all_rounds[-1]

        return {
            'total_payoff': sum(
                [p.payoff for p in player_in_all_rounds]),
            'paying_round': self.session.vars['paying_round'],
            'player_in_all_rounds': player_in_all_rounds,
        }


page_sequence = [
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
