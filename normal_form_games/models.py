from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import numpy as np
import json
doc = """
An experiment with normal form games
"""

class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 51
    stakes = c(100)
    size = 3
    min_time = 10
    ρ_pos = 0.8
    ρ_neg = -0.8
    σ = 50.


def sample_cell(ρ=0, max=99.5, min=-0.5, μ=50, σ=3):
    r,c = np.random.multivariate_normal([0,0], [[1, ρ], [ρ, 1]])*σ + μ
    r = round(r)
    c = round(c)
    while r < min or r > max or c < min or c > max:
        r,c = np.random.multivariate_normal([0,0], [[1, ρ], [ρ, 1]])*σ + μ
        r = round(r)
        c = round(c)
    return [int(r),int(c)]


def rand_game(size, ρ=0., σ=3):
    game = np.zeros((size,size,2))
    for i in range(size):
        for j in range(size):
            r,c = sample_cell(ρ=ρ, max=99.5, min=-0.5, μ=50, σ=σ)
            game[i,j,0] = r
            game[i,j,1] = c
    return game



def transpose_game(game):
    return np.flip(np.swapaxes(game, 0, 1), 2)


same_games_dict = dict()
# same_games_dict[1] = np.array([[[4,0],[4,1],[4,4]], [[8,8],[3,5],[0,4]], [[5,3],[5,5],[1,4]]]) # Weak link
# same_games_dict[2] = np.array([[[8,8],[2,9],[1,0]], [[9,2],[3,3],[1,1]], [[1,3],[0,2],[1,1]]]) # Prisoners
# same_games_dict[3] = np.array([[[9,9],[4,6],[0,4]], [[6,4],[6,6],[1,4]], [[4,0],[4,1],[4,4]]]) # Stag-hunt
# same_games_dict[4] = np.array([[[8,8],[7,8],[1,4]], [[8,7],[9,9],[0,5]], [[6,1],[5,0],[6,6]]]) # Sym
# same_games_dict[5] = np.array([[[7,4],[3,5],[4,0]], [[5,3],[3,7],[3,2]], [[0,3],[1,3],[9,9]]]) # Max
## same_games_dict[6] = np.array([[[2,2],[4,0],[4,0]], [[0,4],[3,3],[5,1]], [[0,4],[1,5],[4,4]]]) # Travellers

same_games_dict[31] = np.array([[[4,0],[4,1],[4,4]], [[8,8],[3,5],[0,4]], [[5,3],[5,5],[1,4]]]) # Weak link
same_games_dict[37] = np.array([[[8,8],[2,9],[1,0]], [[9,2],[3,3],[1,1]], [[1,3],[0,2],[1,1]]]) # Prisoners
same_games_dict[41] = np.array([[[9,9],[4,6],[0,4]], [[6,4],[6,6],[1,4]], [[4,0],[4,1],[4,4]]]) # Stag-hunt
same_games_dict[44] = np.array([[[8,8],[7,8],[1,4]], [[8,7],[9,9],[0,5]], [[6,1],[5,0],[6,6]]]) # Sym
same_games_dict[49] = np.array([[[7,4],[3,5],[4,0]], [[5,3],[3,7],[3,2]], [[0,3],[1,3],[9,9]]]) # Max



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars["num_assigned"] = 0
            self.session.vars["treat_cycle"] = [("positive", "row"), ("positive", "col"), ("negative", "row"), ("negative", "col")]
            self.session.vars["plays_dict"] = dict()
            # self.session.vars["treat_cycle"] = [("negative", "row"), ("negative", "col")]
            for p in self.get_players():
                p.participant.vars["failed"] = False
                # p.participant.vars['role'] = ["row", "col"][(p.id_in_group % 2)]
                # p.participant.vars['treatment'] = ["negative", "positive"][(int((1 + p.id_in_group)/2) % 2)]

        round = self.round_number
        games_dict = dict()
        games_dict["positive"] = dict()
        games_dict["negative"] = dict()
        if round in same_games_dict.keys():
            games_dict["positive"]["row"] = same_games_dict[round]
            games_dict["positive"]["col"] = transpose_game(games_dict["positive"]["row"])
            games_dict["negative"]["row"] = same_games_dict[round]
            games_dict["negative"]["col"] = transpose_game(games_dict["negative"]["row"])
        else:
            games_dict["positive"]["row"] = rand_game(Constants.size, ρ=Constants.ρ_pos, σ=Constants.σ)
            games_dict["positive"]["col"] = transpose_game(games_dict["positive"]["row"])
            games_dict["negative"]["row"] = rand_game(Constants.size, ρ=Constants.ρ_neg, σ=Constants.σ)
            games_dict["negative"]["col"] = transpose_game(games_dict["negative"]["row"])

        round_plays_dict = dict()
        round_plays_dict["positive"] = {"row":[], "col":[]}
        round_plays_dict["negative"] = {"row":[], "col":[]}
        self.session.vars["plays_dict"][round] = round_plays_dict

        self.session.vars[round] = games_dict


        # for p in self.get_players():
            # p.player_role = p.participant.vars['role']
            # p.treatment = p.participant.vars['treatment']
            # p.game = json.dumps(games_dict[p.treatment][p.player_role].tolist())



class Group(BaseGroup):
    def set_payoffs(self):
        p1, p2 = self.get_players()
        p1.other_choice = p2.choice
        p2.other_choice = p1.choice

        game = json.loads(p1.game)
        p1.payoff = c(game[p1.choice][p2.choice][0])
        p2.payoff = c(game[p1.choice][p2.choice][1])


class Player(BasePlayer):
    game = models.StringField()
    choice = models.IntegerField()
    other_choice = models.IntegerField()
    player_role = models.StringField()
    treatment = models.StringField()

    def set_payoff(self):
        # prev_player = self.in_round(self.round_number - 1)
        # game = json.loads(prev_player.game)
        # prev_player.payoff = c(game[prev_player.choice][prev_player.other_choice][0])

        game = json.loads(self.game)
        self.payoff = game[self.choice][self.other_choice][0]
