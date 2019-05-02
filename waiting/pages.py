from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for other players to complete the instructions'
    body_text = '''
        The experiment will begin when ten participants have completed the
        instructions. This helps to ensure that we can match you with other
        players quickly, without making you wait throughout the experiment.
    '''

    def get_players_for_group(self, waiting_players):
        print('get players', waiting_players)
        ready = (self.session.vars["min_players_passed"] or
                 len(waiting_players) >= self.session.config['min_players_start'])
        if ready:
            self.session.vars["min_players_passed"] = True
            return waiting_players


page_sequence = [
    ResultsWaitPage,
]
