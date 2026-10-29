import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- Starter (example) tests ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---------- next_direction: every return line ----------
def test_up_with_request_above():
    assert next_direction(2, "up", [5]) == "up"


def test_up_with_request_only_below():
    assert next_direction(5, "up", [1]) == "down"


def test_up_with_no_requests():
    assert next_direction(4, "up", []) == "idle"


def test_down_with_request_below():
    assert next_direction(6, "down", [2]) == "down"


def test_down_with_request_only_above():
    assert next_direction(1, "down", [7]) == "up"


def test_down_with_no_requests():
    assert next_direction(4, "down", []) == "idle"


def test_idle_with_request_above():
    assert next_direction(0, "idle", [3]) == "up"


def test_idle_with_request_below():
    assert next_direction(8, "idle", [2]) == "down"


# ---------- door_action: every return line ----------
def test_overload():
    assert door_action(700, False, False) == "overload"


def test_blocked_reopens():
    assert door_action(300, True, False) == "reopen"


def test_normal_close():
    assert door_action(300, False, False) == "close"


# ---------- pick_elevator: every line ----------
def test_pick_single_busy_car():
    # busy car -> +5 penalty line runs
    assert pick_elevator([("A", 2, False)], 4) == "A"


def test_pick_closer_idle_car():
    assert pick_elevator([("A", 10, True), ("B", 3, True)], 4) == "B"
