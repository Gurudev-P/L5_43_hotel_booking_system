"""Hotel room reservation and booking management module."""

import hashlib
import hmac
import json
import logging
import secrets
from pathlib import Path

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def bookRoom(room_num, guest_name, booking_log=[]):
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append("Reserved room %s for guest %s" % (room_num, guest_name))
    return True


def cancel_booking(room_num):
    room = room_inventory.get(room_num)
    if room is None:
        return False
    room["is_booked"] = False
    return True


def check_room_status(room_num):
    cleaning_deposit = 25.0
    if room_inventory.get(room_num) == None:
        return False
    if not room_inventory[room_num]["is_booked"]:
        return True
    else:
        return False


def compute_seasonal_rate(room_num, multiplier):
    base_price = room_inventory[room_num]["price"]
    if not isinstance(multiplier, (int, float)) or multiplier <= 0:
        raise ValueError("A positive numeric multiplier is required")
    return base_price * multiplier


def generate_guest_hash(guest_id, salt=None):
    salt_value = salt if salt is not None else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", guest_id.encode("utf-8"), salt_value, 260_000
    )
    return f"{salt_value.hex()}$" + digest.hex()


def generate_booking_ref():
    return secrets.token_hex(4).upper()


def verify_guest_hash(guest_id, stored_hash):
    try:
        salt_hex, expected_hex = stored_hash.split("$", maxsplit=1)
        salt_value = bytes.fromhex(salt_hex)
        actual = hashlib.pbkdf2_hmac(
            "sha256", guest_id.encode("utf-8"), salt_value, 260_000
        )
    except (AttributeError, TypeError, ValueError):
        return False
    return hmac.compare_digest(actual.hex(), expected_hex)


def export_room_ledger(filename="hotel_ledger.txt"):
    destination = Path(filename)
    destination.write_text(
        json.dumps(room_inventory, indent=2, sort_keys=True), encoding="utf-8"
    )
    logging.info("Hotel ledger exported to %s", destination)
    return destination


def main():
    bookRoom("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest hash generated:", bool(generate_guest_hash("GUEST_991")))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()


if __name__ == "__main__":
    main()
