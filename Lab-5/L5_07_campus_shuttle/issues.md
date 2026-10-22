\# Lab 5: Static Code Analysis — Issue Log



| Issue | Tool | Description | Fix Applied |

|---|---|---|---|

| Mutable default argument | Pylint | A default empty list could be shared across function calls. | Changed the default to `None` and initialized a list inside the function. |

| Broad exception handling | Pylint, Bandit, Flake8 | A bare `except` could hide unexpected errors. | Caught expected exceptions explicitly. |

| Random selection warning | Bandit | Bandit flagged the use of the standard `random` module. | Replaced `random.choice` with `secrets.choice`. |

| Missing docstrings | Pylint | The module and functions lacked documentation. | Added module and function docstrings. |

| Function naming and unused argument | Pylint | The function name did not follow `snake\_case`, and an argument was unused. | Renamed the function to `assign\_driver` and validated the route argument. |

| File handling | Pylint | Files were opened without explicit encoding or context managers. | Used `with open(...)` and UTF-8 encoding. |

| Formatting errors | Flake8 | Blank lines, line length, and exception syntax violated style rules. | Corrected formatting and exception handling. |

| Missing route handling | Runtime testing | Looking up a removed or unknown route could cause a crash. | Added route validation and safe handling for missing routes. |

| Invalid passenger counts | Runtime testing | Negative and non-integer passenger counts could corrupt trip data. | Added validation for non-negative integer passenger counts. |



\## Final tool results



\- \*\*Pylint:\*\* 10.00/10

\- \*\*Bandit:\*\* No issues identified.

\- \*\*Flake8:\*\* No issues reported.



