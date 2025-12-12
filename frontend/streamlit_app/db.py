# import psycopg2
# import streamlit as st
# from passlib.hash import pbkdf2_sha256
# import re

# def get_connection():
#     return psycopg2.connect(
#         host="localhost",
#         database="movies_db",
#         user="postgres",
#         password="navin@2006",
#         port="5432"
#     )

# def create_user_table():
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id SERIAL PRIMARY KEY,
#         username VARCHAR(50) UNIQUE NOT NULL,
#         email VARCHAR(100) UNIQUE NOT NULL,
#         password_hash VARCHAR(255) NOT NULL,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

# def validate_email(email):
#     # Strict email regex with valid TLD check
#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|net|org|edu|gov|io|co)$"
#     return re.match(pattern, email) is not None

# def validate_password(password):
#     # 6-10 chars, at least 1 number, 1 special char
#     pattern = r"^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{6,10}$"
#     return re.match(pattern, password) is not None

# def add_user(username, email, password):
#     if not validate_email(email):
#         st.error("❌ Invalid email format! Example: user@example.com")
#         return False
#     if not validate_password(password):
#         st.error("❌ Password must be 6-10 chars, include at least 1 number & 1 special char.")
#         return False

#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         # Check if email already exists
#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         if cur.fetchone():
#             st.error("❌ Email already exists! Use login or reset password.")
#             return False

#         hashed_password = pbkdf2_sha256.hash(password)
#         cur.execute(
#             "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
#             (username, email, hashed_password)
#         )
#         conn.commit()
#         st.success("✅ Account created successfully!")
#         return True
#     except psycopg2.Error as e:
#         st.error(f"Database error: {e}")
#         return False
#     finally:
#         cur.close()
#         conn.close()

# def validate_user(email, password):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT id, username, email, password_hash FROM users WHERE email=%s", (email,))
#     user = cur.fetchone()
#     cur.close()
#     conn.close()
#     if user and pbkdf2_sha256.verify(password, user[3]):
#         return user
#     return None

# def reset_password(email, new_password):
#     if not validate_password(new_password):
#         st.error("❌ Password must be 6-10 chars, include at least 1 number & 1 special char.")
#         return False
#     conn = get_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         if not cur.fetchone():
#             st.error("❌ Email not found!")
#             return False
#         hashed_password = pbkdf2_sha256.hash(new_password)
#         cur.execute("UPDATE users SET password_hash=%s WHERE email=%s", (hashed_password, email))
#         conn.commit()
#         st.success("✅ Password reset successfully!")
#         return True
#     except psycopg2.Error as e:
#         st.error(f"Database error: {e}")
#         return False
#     finally:
#         cur.close()
#         conn.close()