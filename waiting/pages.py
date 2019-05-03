from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time



class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for other players to complete the instructions'
    body_text = '''
        The experiment will begin when ten participants have completed the
        instructions. This helps to ensure that we can match you with other
        players quickly, without making you wait throughout the experiment. Remember that you are being paid an hourly wage of $7 for the time spent on this wait page. 
    '''

    def get_players_for_group(self, waiting_players):
        print('get players', waiting_players)
        ready = (self.session.vars["min_players_passed"] or
                 len(waiting_players) >= self.session.config['min_players_start'])

        for player in waiting_players:
            if player.join_time == 0:
                player.join_time = time.time()

        if ready:
            self.session.vars["min_players_passed"] = True

            for player in waiting_players:
                player.participant.vars["tot_wait_time"] = time.time() - player.join_time
                print(player.participant.vars["tot_wait_time"])
            return waiting_players


page_sequence = [
    ResultsWaitPage,
]
