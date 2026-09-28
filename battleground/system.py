
class Battleground:
    def __init__(self):
        self.teams = {"alliance": [], "horde": []}
        self.scores = {"alliance": 0, "horde": 0}
        self.objectives = {}

    def add_player(self, team, player):
        self.teams[team].append(player)

    def check_balance(self):
        # BUG: 只开场检查
        return abs(len(self.teams["alliance"]) - len(self.teams["horde"])) <= 2

    def capture_point(self, point_id, team, players_count):
        if point_id not in self.objectives:
            self.objectives[point_id] = {"owner": None, "progress": 0}
        obj = self.objectives[point_id]
        # BUG: 不考虑人数差
        obj["progress"] += 1
        if obj["progress"] >= 10:
            obj["owner"] = team
            self.scores[team] += 100
        return obj["progress"]

    def calc_reward(self, team, player):
        # BUG: 只看胜负
        if self.scores[team] > self.scores["other"]:
            return 100
        return 50

    def respawn_time(self, player):
        # BUG: 固定
        return 10
