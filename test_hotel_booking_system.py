"""Functional tests for the cleaned hotel booking module."""

import json

import pytest

import hotel_booking_system as hotel


@pytest.fixture(autouse=True)
def reset_inventory():
    original = {
        key: value.copy() for key, value in hotel.ROOM_INVENTORY.items()
    }
    for room in hotel.ROOM_INVENTORY.values():
        room["is_booked"] = False
    yield
    hotel.ROOM_INVENTORY.clear()
    hotel.ROOM_INVENTORY.update(original)


def test_booking_and_cancel_with_independent_logs():
    log_one = []
    log_two = []
    assert hotel.book_room("101", "Guest One", log_one)
    assert log_one == ["Reserved room 101 for guest Guest One"]
    assert hotel.book_room("102", "Guest Two", log_two)
    assert log_two == ["Reserved room 102 for guest Guest Two"]
    assert hotel.cancel_booking("101")
    assert not hotel.cancel_booking("101")


def test_invalid_booking_inputs_are_rejected():
    assert not hotel.book_room("999", "Guest")
    assert not hotel.book_room("101", "  ")
    assert not hotel.book_room(None, "Guest")


def test_room_status():
    assert hotel.check_room_status("101")
    assert not hotel.check_room_status("999")
    hotel.ROOM_INVENTORY["101"]["is_booked"] = True
    assert not hotel.check_room_status("101")


def test_cancel_unknown_room():
    assert not hotel.cancel_booking("999")


def test_seasonal_rate_and_validation():
    assert hotel.compute_seasonal_rate("101", 1.25) == 187.5
    with pytest.raises(ValueError):
        hotel.compute_seasonal_rate("999", 1.25)
    with pytest.raises(TypeError):
        hotel.compute_seasonal_rate("101", "1.25")
    with pytest.raises(ValueError):
        hotel.compute_seasonal_rate("101", 0)


def test_guest_hash_is_salted_and_verifiable():
    hash_one = hotel.generate_guest_hash("GUEST_991")
    hash_two = hotel.generate_guest_hash("GUEST_991")
    assert hash_one != hash_two
    assert hotel.verify_guest_hash("GUEST_991", hash_one)
    assert not hotel.verify_guest_hash("OTHER", hash_one)
    assert not hotel.verify_guest_hash("GUEST_991", "not-a-valid-hash")


def test_booking_reference_shape():
    reference = hotel.generate_booking_ref()
    assert len(reference) == 8
    assert all(character in "0123456789ABCDEF" for character in reference)


def test_ledger_export(tmp_path):
    destination = hotel.export_room_ledger(str(tmp_path / "ledger.json"))
    assert destination.exists()
    data = json.loads(destination.read_text(encoding="utf-8"))
    assert "101" in data