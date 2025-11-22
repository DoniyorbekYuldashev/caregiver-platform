# Part 2

import sys
from db import get_session, test_connection, close_session
from queries import run_all_queries


def main():
    print(" CAREGIVER PLATFORM - DATABASE QUERIES")
    print(" CSCI 341 - Assignment 3 - Part 2")
    print(" Student: Doniyor Yuldashev")

    if not test_connection():
        print("\nCannot connect to database!")
        return 1

    session = get_session()

    try:
        run_all_queries(session)
        print("\nAll operations completed successfully!\n")
        return 0
    except Exception as e:
        print(f"\nError: {e}")
        session.rollback()
        return 1
    finally:
        close_session(session)


if __name__ == "__main__":
    sys.exit(main())