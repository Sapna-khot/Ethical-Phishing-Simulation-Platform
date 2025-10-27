"""# 🎣 Ethical Phishing Simulation Platform

A comprehensive web-based platform for conducting authorized phishing simulation campaigns.

## ⚠️ LEGAL NOTICE
**FOR AUTHORIZED EDUCATIONAL USE ONLY**
- Requires explicit written authorization
- Must comply with all applicable laws
- Focus on education, not punishment

## Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your SMTP settings

# Initialize
python scripts/init_db.py
python scripts/add_sample_templates.py

# Run
python app.py
```

Open: http://127.0.0.1:5000

## Features
✅ Campaign management  
✅ Email tracking  
✅ Real-time analytics  
✅ Educational content  
✅ Multiple templates

## Documentation
See `/docs` for detailed guides.

## Security
- Run in isolated environment
- Use HTTPS in production
- Implement authentication
- Regular audits
""",