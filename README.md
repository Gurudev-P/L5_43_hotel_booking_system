# Lab 5 — Static Code Analysis (Hotel Booking System)

## Submission contents
- `hotel_booking_system_before.py`: exact assigned starter source used for baseline analysis.
- `hotel_booking_system.py`: cleaned and verified implementation.
- `test_hotel_booking_system.py`: eight functional regression tests.
- `issues.md`: static-analysis findings and corresponding fixes.
- `reflection.md`: answers to the four reflection questions.
- `VERIFICATION_RESULTS.md`: measured before/after results.
- `before_reports/` and `after_reports/`: raw Pylint, Bandit, and Flake8 reports.

## Environment used
Python 3.14.7, Pylint 4.1.4, Bandit 1.9.4, Flake8 7.5.0, pytest 9.2.0.

## Reproduce the analysis
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python hotel_booking_system_before.py
pylint hotel_booking_system_before.py > before_reports/pylint_report.txt 2>&1
bandit -r hotel_booking_system_before.py > before_reports/bandit_report.txt 2>&1
flake8 hotel_booking_system_before.py > before_reports/flake8_report.txt 2>&1

python hotel_booking_system.py
python -m pytest -q test_hotel_booking_system.py
pylint hotel_booking_system.py > after_reports/pylint_report.txt 2>&1
bandit -r hotel_booking_system.py > after_reports/bandit_report.txt 2>&1
flake8 hotel_booking_system.py > after_reports/flake8_report.txt 2>&1
```

## Measured results from the submitted terminal run
- Pylint: 5.53/10 before, 10.00/10 after.
- Bandit: 6 findings before (2 high, 1 medium, 3 low), no issues after.
- Flake8: 6 findings before, no findings after. The final Flake8 report is zero bytes because the tool emitted no diagnostics.
- Functional regression tests: 8 passed.

The three commits separate Bandit security remediation, Pylint code-quality remediation, and Flake8 style/report cleanup.
