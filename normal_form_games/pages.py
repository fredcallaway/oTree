from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random
import pickle as pkl
import pandas as pd
import json
import numpy as np
import time

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']


    def vars_for_template(self):
        min_time = self.session.config["min_time"]
        return {"play_rounds":Constants.num_rounds - 1, "min_time":min_time}

    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        else:
            return self.round_number < Constants.num_rounds

    def before_next_page(self):
        self.session.vars["plays_dict"][self.round_number][self.player.player_role].append(self.player.choice)


class ResultsWaitPage(WaitPage):
    group_by_arrival_time = True
    title_text = 'Waiting for another player'
    body_text = '''
        Not enough players have played this game yet, so we can't match you
        with another player. Please wait until more people complete the
        previous round so that we can match you with a new person.
    '''

    def get_choices(self,round, role):
        choices = self.session.vars["plays_dict"][round][role]
        return choices

    def get_players_for_group(self, players):
        round = self.round_number

        if self.session.vars["time_waited"][round] == 0:
            self.session.vars["time_waited"][round] = time.time()

        players_to_return = []

        row_choices = self.get_choices(round - 1, "row")
        col_choices = self.get_choices(round - 1, "col")

        time_diff = time.time() - self.session.vars["time_waited"][round]
        if not self.session.vars['min_plays_dict'][round]:
            if (len(players) >= self.session.config["min_plays"] or time_diff > self.session.config["min_wait_time"]) and len(row_choices) > 0 and len(col_choices) > 0:
                self.session.vars['min_plays_dict'][round] = True
        if self.session.vars['min_plays_dict'][round]:
            random.shuffle(players)
            for player in  players:
                prev_player = player.in_round(round - 1)
                opp_choices = col_choices if prev_player.player_role == "row" else row_choices
                prev_player.other_choice = random.choice(opp_choices)
                prev_player.set_payoff()

                self.session.vars["num_assigned"][round] += 1
                join_num = self.session.vars["num_assigned"][round]
                role = ["row", "col"][join_num % 2]
                player.participant.vars["treatment"] = self.session.config["treatment"]

                player.treatment = player.participant.vars["treatment"]
                player.player_role = role

                game = self.session.vars[round][role]
                player.game = json.dumps(game.tolist())
            players_to_return.extend(players)

        return players_to_return

    def is_displayed(self):
        if self.round_number == 1:
            round = self.round_number
            self.session.vars["num_assigned"][round] += 1
            join_num = self.session.vars["num_assigned"][round]
            role = ["row", "col"][join_num % 2]
            self.player.participant.vars["treatment"] = self.session.config["treatment"]

            self.player.treatment = self.player.participant.vars["treatment"]
            self.player.player_role = role

            game = self.session.vars[round][role]
            self.player.game = json.dumps(game.tolist())

        if self.player.participant.vars['failed']:
            return False
        return self.round_number > 1


class ResultsSummary(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        return self.round_number > 1

    def vars_for_template(self):
        return {
            "prev_player": self.player.in_round(self.round_number - 1),
            "earnings": self.participant.payoff.to_real_world_currency(self.session)
        }



class FinalSummary(Page):
    def is_displayed(self):
        if self.player.participant.vars['failed']:
            return False
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        cumulative_payoff = sum([p.payoff for p in self.player.in_previous_rounds()])

        return {
            "cumulative_payoff": cumulative_payoff,
            "earnings": self.participant.payoff.to_real_world_currency(self.session)
        }

page_sequence = [
    ResultsWaitPage,
    ResultsSummary,
    Choice,
    FinalSummary
]
