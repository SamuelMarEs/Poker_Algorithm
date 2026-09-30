# tests/test_state.py
import pytest
from poker.state import Player, Street, GameState


def test_player_init():
    p = Player(seat=3, stack=1000)
    assert p.seat == 3
    assert p.stack == 1000
    assert p.hole == []
    assert p.committed == 0
    assert p.street_bet == 0
    assert p.folded is False
    assert p.all_in is False
    assert p.has_acted is False


def test_player_mutation():
    p = Player(seat=0, stack=100)
    p.hole = [0, 1]
    p.stack -= 10
    p.committed += 10
    p.street_bet += 10
    assert p.stack == 90
    assert p.committed == 10
    assert p.street_bet == 10


def test_street_values():
    assert Street.PREFLOP == 0
    assert Street.FLOP == 1
    assert Street.TURN == 2
    assert Street.RIVER == 3
    assert Street.SHOWDOWN == 4
    assert Street.FLOP > Street.PREFLOP


def test_gamestate_init():
    players = [Player(seat=i, stack=1000) for i in range(6)]
    state = GameState(players=players, button_idx=0, sb=1, bb=2)

    assert state.players is players
    assert state.button == 0
    assert state.sb == 1
    assert state.bb == 2
    assert state.ante == 0

    assert state.street == Street.PREFLOP
    assert state.board == []
    assert state.deck == []

    assert state.pot == 0
    assert state.current_bet == 0
    assert state.min_raise == 2        # default = bb
    assert state.last_aggressor is None
    assert state.to_act is None

    assert state.positions == {}
    assert state.action_log == []


def test_gamestate_with_ante():
    players = [Player(seat=i, stack=1000) for i in range(3)]
    state = GameState(players=players, button_idx=1, sb=1, bb=2, ante=1)
    assert state.ante == 1
    assert state.button == 1


def test_players_are_independent():
    """Guard against accidentally sharing a mutable default."""
    p1 = Player(seat=0, stack=100)
    p2 = Player(seat=1, stack=100)
    p1.hole.append(5)
    assert p2.hole == []