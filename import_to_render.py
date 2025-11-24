# import psycopg2
#
# # Add SSL mode to connection string
# DATABASE_URL = "postgresql://caregiver_user:rihnBV3k3cKoI8HuURE7rmGLaKsCZWUh@dpg-d4gtsnhr0fns739sos30-a.oregon-postgres.render.com/caregiver_platform?sslmode=require"
#
# print("Connecting to Render database...")
#
# try:
#     with open('database.sql', 'r', encoding='utf-8') as f:
#         sql = f.read()
#
#     print(f"SQL file loaded ({len(sql)} characters)")
#
#     # Connect with SSL
#     conn = psycopg2.connect(
#         DATABASE_URL,
#         sslmode='require',
#         connect_timeout=10
#     )
#     conn.autocommit = True
#     cur = conn.cursor()
#
#     print("Connected! Importing data...")
#
#     # Split and execute SQL statements
#     statements = [s.strip() for s in sql.split(';') if s.strip()]
#     total = len(statements)
#
#     for i, statement in enumerate(statements):
#         try:
#             cur.execute(statement)
#             if (i + 1) % 10 == 0 or i == total - 1:
#                 print(f"  Progress: {i + 1}/{total} statements")
#         except Exception as e:
#             if "already exists" not in str(e):
#                 print(f"Warning: {e}")
#             continue
#
#     print("Database imported successfully!")
#
#     # Verify import
#     cur.execute("SELECT COUNT(*) FROM users")
#     user_count = cur.fetchone()[0]
#     print(f"Users: {user_count} records")
#
#     cur.close()
#     conn.close()
#
# except psycopg2.OperationalError as e:
#     print(f"Connection Error: {e}")
#     print("\nTroubleshooting:")
#     print("1. Check if Render database is 'Available' (not suspended)")
#     print("2. Render free tier may have connection limits")
#     print("3. Try again in a few minutes")
#
# except Exception as e:
#     print(f"Error: {e}")