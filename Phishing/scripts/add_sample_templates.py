#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, db, Template

TEMPLATES = [
    {
        'name': 'Password Expiration Alert',
        'category': 'credential_harvesting',
        'difficulty': 'easy',
        'subject': 'ACTION REQUIRED: Your password expires today',
        'body': '''<html><body style="font-family: Arial;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
<h2 style="color: #d9534f;">⚠️ Password Expiration</h2>
<p>Your password expires in 2 hours. Reset it immediately:</p>
<div style="text-align: center; margin: 30px 0;">
<a href="{{tracking_url}}" style="background: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">Reset Password</a>
</div>
<p style="color: #d9534f;">Failure to reset will result in account suspension.</p>
</div></body></html>''',
        'landing_page': '''<!DOCTYPE html>
<html><head><title>Reset Password</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;align-items:center;justify-content:center}
.container{background:white;padding:40px;border-radius:10px;max-width:400px}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:5px}
button{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer}</style>
</head><body>
<div class="container">
<h2>🔐 Reset Password</h2>
<form action="/submit/{{token}}" method="POST">
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="old_password" placeholder="Current Password" required>
<input type="password" name="new_password" placeholder="New Password" required>
<button type="submit">Reset Password</button>
</form></div></body></html>'''
    },
    {
        'name': 'Package Delivery',
        'category': 'urgent_action',
        'difficulty': 'medium',
        'subject': 'Failed Delivery - Action Required',
        'body': '''<html><body style="font-family: Arial;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
<h2 style="color: #f0ad4e;">📦 Delivery Failed</h2>
<p>We attempted delivery but were unable to complete it.</p>
<div style="background: #f9f9f9; padding: 15px; margin: 20px 0;">
<strong>Tracking:</strong> 1Z999AA10123456784<br>
<strong>Status:</strong> Failed
</div>
<div style="text-align: center; margin: 30px 0;">
<a href="{{tracking_url}}" style="background: #f0ad4e; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">Reschedule Delivery</a>
</div>
</div></body></html>''',
        'landing_page': '''<!DOCTYPE html>
<html><head><title>Reschedule</title>
<style>body{font-family:Arial;background:#f5f5f5;padding:20px}
.container{max-width:500px;margin:50px auto;background:white;padding:30px;border-radius:8px}
input,select{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:4px}
button{width:100%;padding:12px;background:#f0ad4e;color:white;border:none;border-radius:4px;cursor:pointer}</style>
</head><body>
<div class="container">
<h2>📦 Reschedule Delivery</h2>
<form action="/submit/{{token}}" method="POST">
<input type="text" name="name" placeholder="Full Name" required>
<input type="text" name="address" placeholder="Address" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="email" name="email" placeholder="Email" required>
<select name="time" required>
<option value="">Select Time</option>
<option>Morning</option>
<option>Afternoon</option>
<option>Evening</option>
</select>
<button type="submit">Confirm</button>
</form></div></body></html>'''
    },
    {
        'name': 'Microsoft 365 Security Alert',
        'category': 'credential_harvesting',
        'difficulty': 'medium',
        'subject': 'Microsoft 365: Unusual sign-in activity',
        'body': '''<html><body style="font-family: Segoe UI, Arial;">
<div style="max-width: 600px; margin: 0 auto; background: #f3f2f1; padding: 20px;">
<div style="background: white; padding: 30px; border-top: 4px solid #0078d4;">
<h2 style="color: #0078d4;">🔐 Security Alert</h2>
<p>We detected unusual sign-in activity:</p>
<div style="background: #fff4ce; padding: 15px; margin: 20px 0;">
<strong>Location:</strong> Moscow, Russia<br>
<strong>Status:</strong> Blocked
</div>
<div style="text-align: center; margin: 30px 0;">
<a href="{{tracking_url}}" style="background: #0078d4; color: white; padding: 15px 40px; text-decoration: none;">Verify Account</a>
</div>
</div></div></body></html>''',
        'landing_page': '''<!DOCTYPE html>
<html><head><title>Microsoft Sign In</title>
<style>body{font-family:Segoe UI,sans-serif;background:#f3f2f1;display:flex;align-items:center;justify-content:center;min-height:100vh}
.container{background:white;padding:44px;max-width:440px}
input{width:100%;padding:8px 12px;border:1px solid #8a8886;margin-bottom:24px}
button{width:100%;padding:11px 24px;background:#0078d4;color:white;border:none;cursor:pointer}</style>
</head><body>
<div class="container">
<h1 style="font-size:24px">Verify your account</h1>
<form action="/submit/{{token}}" method="POST">
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form></div></body></html>'''
    }
]

print("Adding sample templates...")
with app.app_context():
    added = 0
    for t in TEMPLATES:
        if not Template.query.filter_by(name=t['name']).first():
            template = Template(**t)
            db.session.add(template)
            added += 1
            print(f"  ✓ {t['name']}")
    db.session.commit()
    print(f"\\n✅ Added {added} templates!")
