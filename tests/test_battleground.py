
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from battleground.system import Battleground


def test_realtime_balance():
    bg = Battleground()
    for i in range(10):
        bg.add_player("alliance", f"a{i}")
    for i in range(3):
        bg.add_player("horde", f"h{i}")
    assert bg.check_balance() == False
    bg.balance_teams()
    assert abs(len(bg.teams["alliance"]) - len(bg.teams["horde"])) <= 2


def test_capture_speed_by_count():
    bg = Battleground()
    bg.capture_point("point1", "alliance", 1)
    p1 = bg.objectives["point1"]["progress"]
    bg.capture_point("point1", "alliance", 5)
    p2 = bg.objectives["point1"]["progress"]
    assert p2 - p1 > 1


def test_reward_by_contribution():
    bg = Battleground()
    bg.scores = {"alliance": 200, "horde": 100, "other": 100}
    mvp = {"damage": 5000, "healing": 0, "kills": 10}
    loser = {"damage": 100, "healing": 0, "kills": 0}
    r1 = bg.calc_reward("alliance", mvp)
    r2 = bg.calc_reward("alliance", loser)
    assert r1 > r2


def test_respawn_increases_with_deaths():
    bg = Battleground()
    p = {"deaths": 0}
    t1 = bg.respawn_time(p)
    p["deaths"] = 5
    t2 = bg.respawn_time(p)
    assert t2 > t1


def test_comeback_event():
    bg = Battleground()
    bg.scores = {"alliance": 500, "horde": 50, "other": 50}
    bg.check_comeback_event()
    assert bg.buffs.get("horde") is not None  # 弱势方有增益


def test_mmr_matchmaking():
    bg = Battleground()
    bg.queue = [{"id": "p1", "mmr": 100}, {"id": "p2", "mmr": 3000}]
    teams = bg.create_teams()
    # 不应把青铜和王者分一队
    assert abs(teams[0]["mmr"] - teams[1]["mmr"]) < 500


def test_objective_contest():
    bg = Battleground()
    bg.capture_point("point1", "alliance", 3)
    bg.capture_point("point1", "horde", 3)  # 双方同时占
    assert bg.objectives["point1"]["owner"] is None  #  contested


def test_leaver_penalty():
    bg = Battleground()
    bg.add_player("alliance", "p1")
    bg.remove_player("alliance", "p1", reason="leave")
    assert bg.penalties.get("p1", 0) > 0


def test_score_tie():
    bg = Battleground()
    bg.scores = {"alliance": 100, "horde": 100, "other": 100}
    assert bg.get_winner() == "tie"
