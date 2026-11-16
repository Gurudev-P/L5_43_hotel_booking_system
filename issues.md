# Lab 5 — Static Code Analysis Findings

**Target:** `hotel_booking_system.py`  
**Original baseline:** `hotel_booking_system_before.py`  
**Analysis environment:** Python 3.14.7, Pylint 4.1.4, Bandit 1.9.4, Flake8 7.5.0

Line numbers below refer to the original `hotel_booking_system_before.py`.

| Issue | Type / Tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Weak MD5 hashing | High — Bandit B324 | 47 | MD5 is unsuitable for security-sensitive credential/identifier hashing. | Replaced MD5 with salted PBKDF2-HMAC-SHA-256 and added verification with constant-time comparison. |
| Shell command constructed from filename | High — Bandit B605 | 58 | `os.system()` invokes a shell using concatenated input, creating command-injection risk. | Removed shell invocation; used `pathlib.Path` for file writing and `logging` for status output. |
| Dynamic `eval()` in seasonal pricing | Medium — Bandit B307; Pylint W0123 | 42 | Evaluates a string as Python code, potentially executing arbitrary expressions. | Replaced expression input with a validated numeric multiplier and direct arithmetic. |
| Bare `except` with `pass` | Low — Bandit B110; Pylint W0702; Flake8 E722 | 26–27 | Suppresses all exceptions and hides invalid room inputs or programming errors. | Added explicit room validation and clear success/failure return behavior; removed broad exception suppression. |
| Non-cryptographic random booking reference | Low — Bandit B311 | 51 | `random.randint()` is not suitable for security-sensitive tokens or references that need unpredictability. | Replaced it with `secrets.token_hex()` to generate a random booking reference. |
| Hard-coded secret | Low — Bandit B105 | 62 (printed at 70) | A token-like secret is embedded in source code and printed to output. | Removed the hard-coded secret and its output. No credential is needed for the demo. |
| Mutable default argument | Bug — Pylint W0102 | 15 | `booking_log=[]` is shared between calls, which can leak booking records across invocations. | Changed the default to `None` and create a fresh list when no list is supplied. |
| Missing function docstrings | Maintainability — Pylint C0116 | Several functions | Functions lack documentation describing their behavior and input/output contracts. | Added concise docstrings to functions. |
| Non-snake-case function name | Style — Pylint C0103 | 15 | `bookRoom` does not follow Python's snake_case naming convention. | Renamed it to `book_room`. |
| Old-style string formatting | Style — Pylint C0209 | 19 | `%` formatting is less readable than an f-string in this case. | Replaced it with an f-string. |
| `== None` comparison and redundant branch | Quality — Pylint C0121, R1703, R1705; Flake8 E711 | 32–36 | Uses an equality comparison with `None` and an unnecessary `else` after a return. | Used an identity-safe `is None` check / direct boolean return. |
| Unused import and variables | Quality — Pylint W0611/W0612; Flake8 F401/F841 | 6, 31, 41 | `math`, `cleaning_deposit`, and the original `base_price` assignment were unused. | Removed unused import and variables; the new pricing implementation uses the base price directly. |
| File writing without encoding/context manager | Quality — Pylint W1514/R1732 | 55–56 | `open()` does not specify encoding and the file is manually closed. | Used `Path.write_text(..., encoding="utf-8")`, which manages the file operation. |
| Long line | Style — Flake8 E501 | 19 | A line exceeded Flake8's 79-character default. | Wrapped the line across multiple lines. |
| Import-time program execution | Testability / design | final `main()` call | Importing the module immediately ran the demo, making it harder to test functions independently. | Added an `if __name__ == "__main__":` guard. |

## Actual before/after tool results

| Tool | Before | After |
|---|---|---|
| Pylint | **5.53/10** | **10.00/10** |
| Bandit | **6 findings**: 2 high, 1 medium, 3 low | **No issues identified**; 0 high, 0 medium, 0 low |
| Flake8 | **6 findings** | **No output / no findings** |
| Functional pytest suite | Not run against the original in this transcript | **8 passed** (`8 passed in 0.16s`) |

## Verification notes

The after-analysis commands were run against `hotel_booking_system.py`. Pylint returned a score of 10.00/10. Bandit reported “No issues identified” and zero findings in every severity category. Flake8 produced no diagnostic output, indicating no style findings. The functional regression suite passed all eight tests.

The original reports were generated against `hotel_booking_system_before.py`. The before/after report files should be kept in `before_reports/` and `after_reports/` respectively.