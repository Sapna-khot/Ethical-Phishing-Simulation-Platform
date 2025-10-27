#!/usr/bin/env python3
import sys, os, getpass
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db, User

print("Create Admin User")
print("=" * 50)

username = input("Username: ")
email = input("Email: ")
password = getpass.getpass("Password: ")

with app.app_context():
    if User.query.filter_by(username=username).first():
        print("❌ User already exists")
    else:
        user = User(username=username, email=email, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Admin '{username}' created!")

