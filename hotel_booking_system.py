"""Hotel room reservation and booking management module.

This module provides a small in-memory hotel inventory with booking,
cancellation, seasonal pricing, guest credential hashing, and ledger export.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import secrets
from pathlib import Path
from typing import Optional

LOGGER = logging.getLogger(__name__)

ROOM_INVENTORY = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}

_HASH_ITERATIONS = 260_000
_HASH_SALT_BYTES = 16


def book_room(
    room_num: str,
    guest_name: str,
    booking_log: Optional[list[str]] = None,
) -> bool:
    """Reserve an available room and optionally append a booking record."""
    if not isinstance(room_num, str) or room_num not in ROOM_INVENTORY:
        LOGGER.warning("Booking rejected: unknown room %r", room_num)
        return False
    if not isinstance(guest_name, str) or not guest_name.strip():
        LOGGER.warning("Booking rejected: guest name is required")
        return False
    if ROOM_INVENTORY[room_num]["is_booked"]:
        return False

    if booking_log is None:
        booking_log = []
    ROOM_INVENTORY[room_num]["is_booked"] = True
    booking_log.append(
        f"Reserved room {room_num} for guest {guest_name.strip()}"
    )
    return True


def cancel_booking(room_num: str) -> bool:
    """Cancel a reservation; return False when the room does not exist."""
    if not isinstance(room_num, str) or room_num not in ROOM_INVENTORY:
        LOGGER.warning("Cancellation rejected: unknown room %r", room_num)
        return False
    if not ROOM_INVENTORY[room_num]["is_booked"]:
        return False
    ROOM_INVENTORY[room_num]["is_booked"] = False
    return True


def check_room_status(room_num: str) -> bool:
    """Return True for an existing available room, otherwise False."""
    room = ROOM_INVENTORY.get(room_num) if isinstance(room_num, str) else None
    return room is not None and not room["is_booked"]


def compute_seasonal_rate(room_num: str, multiplier: float) -> float:
    """Return the room price adjusted by a positive seasonal multiplier."""
    if not isinstance(room_num, str) or room_num not in ROOM_INVENTORY:
        raise ValueError(f"Unknown room: {room_num!r}")
    if isinstance(multiplier, bool) or not isinstance(
        multiplier, (int, float)
    ):
        raise TypeError("Multiplier must be a number")
    if not 0 < multiplier <= 5:
        raise ValueError("Multiplier must be greater than 0 and at most 5")

    base_price = float(ROOM_INVENTORY[room_num]["price"])
    return round(base_price * float(multiplier), 2)


def generate_guest_hash(guest_id: str, salt: Optional[bytes] = None) -> str:
    """Hash a guest identifier using PBKDF2-HMAC-SHA-256 and a random salt.

    The salt is included in the returned hexadecimal string so that it can be
    stored and later verified. Callers should use verify_guest_hash rather
    than compare hashes generated with different random salts.
    """
    if not isinstance(guest_id, str) or not guest_id:
        raise ValueError("Guest ID must be a non-empty string")
    salt_value = (
        salt if salt is not None else secrets.token_bytes(_HASH_SALT_BYTES)
    )
    if not isinstance(salt_value, bytes) or len(salt_value) < _HASH_SALT_BYTES:
        raise ValueError("Salt must be bytes with at least 16 bytes")
    digest = hashlib.pbkdf2_hmac(
        "sha256", guest_id.encode("utf-8"), salt_value, _HASH_ITERATIONS
    )
    return f"{salt_value.hex()}${digest.hex()}"


def verify_guest_hash(guest_id: str, stored_hash: str) -> bool:
    """Verify a guest identifier against the salted PBKDF2 hash."""
    try:
        salt_hex, expected_hex = stored_hash.split("$", maxsplit=1)
        salt_value = bytes.fromhex(salt_hex)
        if not isinstance(guest_id, str) or not guest_id:
            return False
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256", guest_id.encode("utf-8"), salt_value, _HASH_ITERATIONS
        )
    except (AttributeError, TypeError, ValueError):
        return False
    return hmac.compare_digest(actual_digest.hex(), expected_hex)


def generate_booking_ref() -> str:
    """Generate a strong, eight-character booking reference."""
    return secrets.token_hex(4).upper()


def export_room_ledger(filename: str = "hotel_ledger.txt") -> Path:
    """Write the current room inventory to a UTF-8 ledger file."""
    destination = Path(filename)
    destination.write_text(
        json_dumps_room_inventory(), encoding="utf-8"
    )
    LOGGER.info("Hotel ledger exported to %s", destination)
    return destination


def json_dumps_room_inventory() -> str:
    """Serialize inventory as readable JSON."""

    return json.dumps(ROOM_INVENTORY, indent=2, sort_keys=True) + "\n"


def main() -> None:
    """Run a short demonstration of the hotel booking operations."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )

    bookings: list[str] = []
    book_room("101", "Guest Example", bookings)
    cancel_booking("102")
    print("Is room 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))

    guest_hash = generate_guest_hash("GUEST_991")
    print("Guest hash generated:", bool(guest_hash))
    print("Booking reference:", generate_booking_ref())
    export_room_ledger()


if __name__ == "__main__":
    main()