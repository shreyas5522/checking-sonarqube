# main.py
"""
A small, clean Python script to test your Jenkins → SonarQube setup.
- Pure standard library (no external dependencies)
- Contains type hints, docstrings, basic logging, and simple unit-like self-check
- Can be executed directly: `python3 main.py --task fib --n 10`

You can commit this as the only file in your GitHub repo and point Jenkins at it.
Later, you can add real unit tests (e.g., with pytest/unittest) and coverage.
"""

from __future__ import annotations
import argparse
import logging
import os
import sys
from typing import List


# --- Logging setup ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


# --- Core functionality ---
def fibonacci(n: int) -> List[int]:
    """
    Return the first n Fibonacci numbers as a list.
    Examples:
        fibonacci(1) -> [0]
        fibonacci(5) -> [0, 1, 1, 2, 3]
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    if n == 1:
        return [0]

    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq


def is_prime(x: int) -> bool:
    """
    Simple primality test for positive integers.
    Returns True if x is prime, False otherwise.
    """
    if x <= 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    i = 5
    while i * i <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return False
        i += 6
    return True


def primes_up_to(n: int) -> List[int]:
    """
    Return a list of prime numbers up to and including n.
    """
    if n < 2:
        return []
    return [x for x in range(2, n + 1) if is_prime(x)]


# --- CLI handling ---
def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tiny Python app to test Jenkins + SonarQube pipeline."
    )
    subparsers = parser.add_subparsers(dest="task", required=True)

    # fibonacci
    fib_p = subparsers.add_parser("fib", help="Generate first n Fibonacci numbers.")
    fib_p.add_argument("--n", type=int, required=True, help="How many numbers.")

    # primes
    primes_p = subparsers.add_parser("primes", help="List primes up to n.")
    primes_p.add_argument("--n", type=int, required=True, help="Upper bound (inclusive).")

    # env
    subparsers.add_parser(
        "env",
        help="Print a few environment variables useful in CI (e.g., Jenkins, Sonar).",
    )

    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if args.task == "fib":
        logger.info("Generating Fibonacci sequence...")
        seq = fibonacci(args.n)
        print(seq)
        return 0

    if args.task == "primes":
        logger.info("Listing primes up to n...")
        seq = primes_up_to(args.n)
        print(seq)
        return 0

    if args.task == "env":
        # Print a subset of environment variables that are often present in CI
        # Safe to print; avoids secrets.
        vars_to_show = [
            "JENKINS_URL",
            "JOB_NAME",
            "BUILD_NUMBER",
            "GIT_URL",
            "BRANCH_NAME",
            "SONAR_HOST_URL",
        ]
        for k in vars_to_show:
            print(f"{k}={os.getenv(k, '')}")
        return 0

    logger.error("Unknown task.")
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        logger.exception("Unhandled error: %s", exc)
        sys.exit(1)
