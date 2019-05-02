from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import numpy as np
import json

def rand_game(size):
    return np.random.randint(10, size=(size,size,2))

class MyPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return False
        else:
            return not self.player.participant.vars.get('done', False)
        # return not self.player.participant.vars.get('done', False)

    def before_next_page(self):
        self.player.game = json.dumps(rand_game(Constants.size).tolist())
        self.player.choice_quiz = np.random.randint(Constants.size)
        self.player.other_choice_quiz = np.random.randint(Constants.size)


class Instructions(MyPage):
    def before_next_page(self):
        super().before_next_page()
        self.player.correct = True
        self.player.participant.vars['done'] = False
        self.player.q_num = 1

    def vars_for_template(self):
        return {
            "points_per_dollar": round(1/self.session.config['real_world_currency_per_point']),
        }

class FailPage(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed'] == True:
            return True
        else:
            return False

class Quiz(MyPage):
    form_model = 'player'
    form_fields = ['payoff_quiz', 'other_payoff_quiz']

    def vars_for_template(self):
        row_num = self.player.choice_quiz
        col_num = self.player.other_choice_quiz
        texts = ["first", "second", "third"]
        return {
            'row': texts[row_num],
            'col': texts[col_num]
        }

    def is_displayed(self):
        if self.player.correct == False:
            return False
        else:
            return super().is_displayed()

    def before_next_page(self):
        p = self.player
        p.q_num += 1
        game = json.loads(p.game)
        cell = game[p.choice_quiz][p.other_choice_quiz]
        print(cell)
        print(p.payoff_quiz, p.other_payoff_quiz)
        p.correct = (cell[0] == p.payoff_quiz and cell[1] == p.other_payoff_quiz)

        if not p.correct and self.round_number == Constants.num_rounds:
            p.participant.vars['failed'] = True
        super().before_next_page()


class LastQuiz(Quiz):
    def before_next_page(self):
        super().before_next_page()
        p = self.player
        if p.correct:
            p.participant.vars['done'] = True


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
        ready = (self.session.vars["minimum_players_passed"] or
                 len(waiting_players) >= self.session.config['min_players_start'])
        if ready:
            self.session.vars["minimum_players_passed"] = True
            return waiting_players


page_sequence = [
    Instructions,
    Quiz,
    Quiz,
    LastQuiz,
    FailPage,
    ResultsWaitPage,
]
