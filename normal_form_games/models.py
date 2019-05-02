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
    ρ_pos = 0.9
    ρ_neg = -0.9
    σ = 5.


def sample_cell(ρ=0, max=9.5, min=-0.5, μ=5, σ=5):
    r,c = np.random.multivariate_normal([0,0], [[1, ρ], [ρ, 1]])*σ + μ
    r = round(r)
    c = round(c)
    while r < min or r > max or c < min or c > max:
        r,c = np.random.multivariate_normal([0,0], [[1, ρ], [ρ, 1]])*σ + μ
        r = round(r)
        c = round(c)
    return [int(r),int(c)]


def rand_game(size, ρ=0., σ=5):
    game = np.zeros((size,size,2))
    for i in range(size):
        for j in range(size):
            r,c = sample_cell(ρ=ρ, max=9.5, min=-0.5, μ=5, σ=σ)
            game[i,j,0] = r
            game[i,j,1] = c
    return game



def transpose_game(game):
    return np.flip(np.swapaxes(game, 0, 1), 2)


same_games_dict = dict()

# same_games_dict[31] = np.array([[[4,0],[4,1],[4,4]], [[8,8],[3,5],[0,4]], [[5,3],[5,5],[1,4]]]) # Weak link
# same_games_dict[37] = np.array([[[8,8],[2,9],[1,0]], [[9,2],[3,3],[1,1]], [[1,3],[0,2],[1,1]]]) # Prisoners
# same_games_dict[41] = np.array([[[9,9],[4,6],[0,4]], [[6,4],[6,6],[1,4]], [[4,0],[4,1],[4,4]]]) # Stag-hunt
# same_games_dict[44] = np.array([[[8,8],[7,8],[1,4]], [[8,7],[9,9],[0,5]], [[6,1],[5,0],[6,6]]]) # Sym
# same_games_dict[49] = np.array([[[7,4],[3,5],[4,0]], [[5,3],[3,7],[3,2]], [[0,3],[1,3],[9,9]]]) # Max

same_games_dict[25] = np.array([[[8,8],[2,5],[0,4]], [[5,2],[5,5],[2,4]], [[4,0],[4,2],[4,4]]]) # Weak link
same_games_dict[29] = np.array([[[8,8],[2,9],[1,0]], [[9,2],[3,3],[1,1]], [[0,1],[1,1],[1,1]]]) # Prisoners
same_games_dict[34] = np.array([[[4,4],[3,7],[5,0]], [[7,3],[3,3],[5,1]], [[0,5],[1,5],[9,9]]]) # Max
# same_games_dict[3] = np.array([[[8,8],[7,5],[2,4]], [[5,7],[9,9],[0,5]], [[4,2],[5,0],[6,6]]]) # Sym
same_games_dict[38] = np.array([[[4,4],[4,5],[8,3]], [[5,4],[8,8],[0,9]], [[3,8],[9,0],[1,1]]]) # No NE
same_games_dict[44] = np.array([[[4,4],[4,1],[4,0]], [[1,4],[6,6],[6,4]], [[0,4],[4,6],[9,9]]]) # Stag-hunt
same_games_dict[50] = np.array([[[5,5],[1,3],[9,0]], [[3,1],[3,3],[9,0]], [[0,9],[0,9],[7,7]]]) # Risky joitnmax with inefficient NE





class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars["num_assigned"] = [0]*(Constants.num_rounds+2) ## Todo: find right value
            self.session.vars["time_waited"] = [0]*(Constants.num_rounds+2) ## Todo: find right value
            # self.session.vars["treat_cycle"] = [("positive", "row"), ("positive", "col"), ("negative", "row"), ("negative", "col")]
            # self.session.vars["role_cycle"] = ['row', 'col']
            self.session.vars["plays_dict"] = dict()
            self.session.vars["min_plays_dict"] = dict()
            for i in range(0, Constants.num_rounds + 1):
                self.session.vars["min_plays_dict"][i] = False
            # self.session.vars["treat_cycle"] = [("negative", "row"), ("negative", "col")]
            for p in self.get_players():
                p.participant.vars["failed"] = False
                # p.participant.vars['role'] = ["row", "col"][(p.id_in_group % 2)]
                # p.participant.vars['treatment'] = ["negative", "positive"][(int((1 + p.id_in_group)/2) % 2)]

        round = self.round_number
        games_dict = dict()
        ρ = Constants.ρ_pos if self.session.config["treatment"] == "positive"  else Constants.ρ_neg
        # games_dict["positive"] = dict()
        # games_dict["negative"] = dict()
        if round in same_games_dict.keys():
            games_dict["row"] = same_games_dict[round]
            games_dict["col"] = transpose_game(games_dict["row"])
        else:
            games_dict["row"] = rand_game(Constants.size, ρ=ρ, σ=Constants.σ)
            games_dict["col"] = transpose_game(games_dict["row"])

        round_plays_dict = dict()
        round_plays_dict = {"row":[], "col":[]}
        self.session.vars["plays_dict"][round] = round_plays_dict

        self.session.vars[round] = games_dict


        # for p in self.get_players():
            # p.player_role = p.participant.vars['role']
            # p.treatment = p.participant.vars['treatment']
            # p.game = json.dumps(games_dict[p.treatment][p.player_role].tolist())



class Group(BaseGroup):
    pass


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
