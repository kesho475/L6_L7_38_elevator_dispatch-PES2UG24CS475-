import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- Starter (example) tests ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ================= next_direction =================
# direction == "up": True / False branches
def test_up_with_request_above():
    assert next_direction(2, "up", [5]) == "up"


def test_up_prefers_above_when_both_sides():
    assert next_direction(4, "up", [1, 8]) == "up"


def test_up_with_request_only_below():
    assert next_direction(5, "up", [1]) == "down"


def test_up_with_no_requests():
    assert next_direction(4, "up", []) == "idle"


def test_up_request_at_current_floor_only():
    # request equal to current floor is neither above nor below
    assert next_direction(4, "up", [4]) == "idle"


# direction == "down": True / False branches
def test_down_with_request_below():
    assert next_direction(6, "down", [2]) == "down"


def test_down_prefers_below_when_both_sides():
    assert next_direction(4, "down", [1, 8]) == "down"


def test_down_with_request_only_above():
    assert next_direction(1, "down", [7]) == "up"


def test_down_with_no_requests():
    assert next_direction(4, "down", []) == "idle"


# any other direction (idle) branches
def test_idle_with_request_above():
    assert next_direction(0, "idle", [3]) == "up"


def test_idle_with_request_below():
    assert next_direction(8, "idle", [2]) == "down"


def test_idle_both_sides_goes_up_first():
    assert next_direction(5, "idle", [2, 9]) == "up"


def test_unknown_direction_behaves_like_idle():
    assert next_direction(5, "sideways", [1]) == "down"


# ================= door_action =================
def test_emergency_overrides_overload_and_block():
    assert door_action(900, True, True) == "hold_open"


def test_overload():
    assert door_action(700, False, False) == "overload"


def test_overload_just_above_limit():
    assert door_action(631, False, False) == "overload"


def test_exact_limit_is_not_overload():
    assert door_action(630, False, False) == "close"


def test_overload_checked_before_blocked():
    assert door_action(700, True, False) == "overload"


def test_blocked_reopens():
    assert door_action(300, True, False) == "reopen"


def test_normal_close():
    assert door_action(300, False, False) == "close"


# ================= pick_elevator =================
def test_pick_no_cars_returns_none():
    # loop body never runs
    assert pick_elevator([], 4) is None


def test_pick_single_busy_car():
    assert pick_elevator([("A", 2, False)], 4) == "A"


def test_pick_single_idle_car():
    assert pick_elevator([("A", 2, True)], 4) == "A"


def test_pick_later_closer_car_replaces_best():
    assert pick_elevator([("A", 10, True), ("B", 3, True)], 4) == "B"


def test_pick_later_farther_car_does_not_replace_best():
    # `gap < best_gap` is False
    assert pick_elevator([("A", 4, True), ("B", 9, True)], 4) == "A"


def test_pick_tie_keeps_first_car():
    assert pick_elevator([("A", 2, True), ("B", 6, True)], 4) == "A"


def test_busy_penalty_makes_farther_idle_car_win():
    # A: gap 1 + 5 = 6, B: gap 3 -> B wins
    assert pick_elevator([("A", 5, False), ("B", 7, True)], 4) == "B"
