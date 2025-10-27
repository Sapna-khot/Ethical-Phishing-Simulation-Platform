#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db

print("⚠️  WARNING: This will delete ALL data!")
confirm = input("Type 'YES' to confirm: ")

if confirm == 'YES':
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✅ Database reset!")
else:
    print("❌ Cancelled")
