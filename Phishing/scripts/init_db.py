#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db

print("Initializing database...")
with app.app_context():
    db.create_all()
    print("✅ Database initialized successfully!")