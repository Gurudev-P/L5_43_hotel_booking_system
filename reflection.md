# Lab 5 — Reflection

## 1. What is static code analysis, and how do Pylint, Bandit, and Flake8 differ?

Static code analysis examines source code without running the program. Pylint focuses on Python code quality, likely programming mistakes, naming, documentation, and maintainability. Bandit scans Python source for common security weaknesses. Flake8 checks style and formatting conventions, including many PEP 8 violations and pycodestyle/pyflakes findings. The tools complement one another because correctness, security, and readability are different dimensions of quality.

## 2. Which issues were most important, and why?

The highest-priority issues were dynamic `eval()` and the shell command constructed with `os.system()`, because unsafe execution can cross a security boundary. The hard-coded secret and use of MD5 for a credential-like value were also security concerns. The mutable default argument could silently mix booking records between calls, while the bare exception handler concealed invalid-room errors and made debugging difficult.

## 3. How were the issues fixed?

The seasonal-price function now accepts a validated numeric multiplier instead of evaluating source code. Ledger output uses `pathlib` and logging rather than a shell command. The embedded token was removed. Guest IDs are hashed with a random salt and PBKDF2-HMAC-SHA-256, with constant-time comparison during verification. The booking log now uses a `None` default, room operations validate identifiers, and broad exception suppression was removed. Naming, documentation, and import-time behavior were also improved.

## 4. How does static analysis contribute to software quality and maintainability?

Static analysis provides repeatable feedback before deployment and helps detect defects that may not be obvious during normal execution. Using several tools produces a broader view: maintainability and logical concerns, security risks, and style problems. Fixing findings improves clarity and reduces avoidable risk, while rerunning the tools after changes provides evidence that addressed findings have been resolved. Static analysis does not replace runtime tests, code review, or threat modeling.