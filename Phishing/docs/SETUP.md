"""# Setup Guide

## Prerequisites
- Python 3.8+
- pip
- SMTP server access

## Installation

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your SMTP settings
```

4. **Initialize database:**
```bash
python scripts/init_db.py
python scripts/add_sample_templates.py
```

5. **Run application:**
```bash
python app.py
```

Open: http://127.0.0.1:5000

## Gmail SMTP Setup

1. Enable 2FA on Google Account
2. Generate App Password
3. Use App Password in .env file

## Troubleshooting

**Database errors:** Delete instance/phishing_sim.db and reinitialize
**SMTP errors:** Check credentials and firewall settings
""",
