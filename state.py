from enum import IntEnum
from deck import Deck

class Player:
    def __init__(self, seat, stack):
        self.seat = seat
        self.stack = stack
        self.hole = []           # 2 cards
        self.committed = 0       # total chips in pot this hand
        self.street_bet = 0      # chips bet this street
        self.folded = False
        self.all_in = False
        self.has_acted = False   # acted since last raise

class Street(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4

def assign_positions(players, button_idx):
    """Returns dict: seat -> position string."""
    active = [p.seat for p in players if not p.folded]
    n = len(active)
    btn = active.index(button_idx)
    # rotate so index 0 is button
    rotated = active[btn:] + active[:btn]
    positions = {}
    if n == 2:
        positions[rotated[0]] = "BTN_SB"
        positions[rotated[1]] = "BB"
    else:
        positions[rotated[0]] = "BTN"
        positions[rotated[1]] = "SB"
        positions[rotated[2]] = "BB"
        for i in range(3, n):
            positions[rotated[i]] = f"UTG+{i-3}" if i > 3 else "UTG"
    return positions

class GameState:
    def __init__(self, players, button_idx, sb, bb, ante=0):
        self.players = players
        self.button = button_idx
        self.sb = sb
        self.bb = bb
        self.ante = ante

        self.street = Street.PREFLOP
        self.board = []
        self.deck = []

        self.pot = 0                # chips already collected
        self.current_bet = 0        # highest street_bet this street
        self.min_raise = bb         # size of last raise increment
        self.last_aggressor = None  # seat that last bet/raised
        self.to_act = None          # seat whose turn it is

        self.positions = {}
        self.action_log = []        # for hand history
        
def start_hand(state, deck):
    state.deck = deck
    state.board = []
    state.street = Street.PREFLOP
    state.pot = 0
    state.current_bet = 0
    state.min_raise = state.bb

    for p in state.players:
        p.hole = deck.deal(2)
        p.committed = 0
        p.street_bet = 0
        p.folded = False
        p.all_in = False
        p.has_acted = False

    state.positions = assign_positions(state.players, state.button)

    post_antes(state)
    post_blinds(state)
    state.to_act = first_to_act_preflop(state)

def post_antes(state):
    if state.ante == 0:
        return
    for p in state.players:
        amt = min(state.ante, p.stack)
        p.stack -= amt
        p.committed += amt
        state.pot += amt
        if p.stack == 0:
            p.all_in = True
            
def post_blinds(state):
    sb_seat = next(s for s, pos in state.positions.items() if pos in ("SB", "BTN_SB"))
    bb_seat = next(s for s, pos in state.positions.items() if pos == "BB")

    for seat, amt in [(sb_seat, state.sb), (bb_seat, state.bb)]:
        p = player_at(state, seat)
        pay = min(amt, p.stack)
        p.stack -= pay
        p.committed += pay
        p.street_bet += pay
        if p.stack == 0:
            p.all_in = True

    state.current_bet = state.bb
    state.min_raise = state.bb
    state.last_aggressor = bb_seat

def player_at(state, seat):
    for p in state.players:
        if p.seat == seat:
            return p
    raise ValueError(f"No player at seat {seat}")

def first_to_act_preflop(state):
    bb_seat = next(s for s, pos in state.positions.items() if pos == "BB")
    return next_active_after(state, bb_seat, include_self=False)

def first_to_act_postflop(state):
    return next_active_after(state, state.button, include_self=False)

def next_active_after(state, seat, include_self=False):
    order = sorted(p.seat for p in state.players)
    idx = order.index(seat)
    start = 0 if include_self else 1
    for i in range(start, len(order) + start):
        s = order[(idx + i) % len(order)]
        p = player_at(state, s)
        if not p.folded and not p.all_in:
            return s
    return None
