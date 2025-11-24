import sys
from db import get_session, test_connection, close_session
from queries import run_all_queries

if __name__ == "__main__":
    print("Testing database connection...")

    if not test_connection():
        print("\nCannot connect to database!")
        sys.exit(1)

    session = get_session()

    try:
        run_all_queries(session)
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        close_session(session)