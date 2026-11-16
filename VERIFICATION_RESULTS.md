# Lab 5 — Verification Results

These results were copied from the terminal output supplied after running the tools locally on macOS.

- Python: 3.14.7
- Pylint: 4.1.4
- Bandit: 1.9.4
- Flake8: 7.5.0
- pytest: 9.2.0

## Before analysis (`hotel_booking_system_before.py`)

- Pylint score: **5.53/10**.
- Bandit: **6 total findings** — 2 high, 1 medium, 3 low.
  - B110: try/except/pass (low)
  - B307: eval (medium)
  - B324: weak MD5 hash (high)
  - B311: non-cryptographic random generator (low)
  - B605: shell execution through `os.system()` (high)
  - B105: hard-coded password/token string (low)
- Flake8: **6 findings** — unused import, line too long, bare except, two unused local variables, and comparison to `None` with `==`.

## After analysis (`hotel_booking_system.py`)

- Pylint score: **10.00/10**.
- Bandit: **No issues identified**; zero findings at high, medium, and low severity.
- Flake8: no diagnostic output.
- Functional tests: **8 passed in 0.16 seconds**.

## Commands used

```bash
pylint hotel_booking_system_before.py > before_reports/pylint_report.txt 2>&1
bandit -r hotel_booking_system_before.py > before_reports/bandit_report.txt 2>&1
flake8 hotel_booking_system_before.py > before_reports/flake8_report.txt 2>&1

python hotel_booking_system.py
python -m pytest -q test_hotel_booking_system.py

pylint hotel_booking_system.py > after_reports/pylint_report.txt 2>&1
bandit -r hotel_booking_system.py > after_reports/bandit_report.txt 2>&1
flake8 hotel_booking_system.py > after_reports/flake8_report.txt 2>&1
```

Keep the raw report files produced in the local `before_reports/` and `after_reports/` folders. This summary does not replace those raw reports.