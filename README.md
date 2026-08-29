🎣 Ethical Phishing Simulation Platform

A web-based Ethical Phishing Simulation Platform built with Python, Flask, SQLite, HTML, CSS and JavaScript.
The platform is designed for authorized security-awareness training where administrators can create simulated phishing campaigns, manage email templates, add authorized training targets, track campaign activity, and view analytics.

⚠️ AUTHORIZED SECURITY TRAINING ONLY

Use this project only with explicit authorization and consent from the organization and participants.
Do not use it to collect real credentials, sensitive information, or to target people without permission.

📌 Project Overview

The platform provides a central dashboard for conducting controlled phishing-awareness simulations.

Main workflow

~~~text
Admin
  │
  ├── Create Email Template
  │       ├── Email Subject
  │       ├── Email Body
  │       ├── Landing Page
  │       ├── Category
  │       └── Difficulty
  │
  ├── Create Campaign
  │       ├── Campaign Name
  │       ├── Description
  │       ├── Select Template
  │       └── Add Authorized Targets
  │
  ├── Launch / Track Simulation
  │       ├── Sent
  │       ├── Opened
  │       ├── Clicked
  │       └── Submitted
  │
  └── Analytics
          ├── Campaign Statistics
          ├── Open Rate
          ├── Click Rate
          └── Submit Rate
   ~~~

✨ Features

🎯 Campaign creation and management

📧 Email template management

🗑️ Template deletion with campaign-history protection

👥 Authorized target management

📊 Dashboard statistics

📈 Campaign analytics

🔗 Email open and click tracking

📝 Landing-page submission tracking for training analysis

🎓 Educational content shown after a simulated phishing attempt

🖥️ Cybersecurity/SOC-inspired user interface

📱 Responsive layout

🗄️ SQLite database

🔐 Environment-variable based SMTP configuration

🧪 Simulation mode when SMTP credentials are not configured

🛠️ Technology Stack

Component

Technology

Backend

Python

Web Framework

Flask

Database

SQLite

ORM

Flask-SQLAlchemy

Frontend

HTML5, CSS3, JavaScript

Email

SMTP

Gmail Support

Gmail SMTP + Google App Password

Configuration

python-dotenv

Production Server

Gunicorn

📁 Project Structure
~~~
Ethical-Phishing-Simulation-Platform-main/
│
└── Phishing/
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── setup.sh
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   │
    │   └── js/
    │       └── main.js
    │
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── campaigns.html
    │   ├── campaign_detail.html
    │   ├── create_campaign.html
    │   ├── templates.html
    │   ├── create_template.html
    │   ├── preview_template.html
    │   ├── analytics.html
    │   ├── education.html
    │   ├── landing.html
    │   └── error.html
    │
    ├── scripts/
    │   ├── init_db.py
    │   ├── add_sample_templates.py
    │   ├── create_admin.py
    │   └── reset_database.py
    │
    ├── docs/
    │   ├── SETUP.md
    │   ├── USER_GUIDE.md
    │   ├── DEPLOYMENT.md
    │   └── API.md
    │
    └── instance/
        └── phishing_sim.db

Important folders

app.py
Main Flask application containing database models, routes, email functionality, tracking and analytics.

templates/
Contains the Jinja2 HTML pages used by the application.

static/css/style.css
Contains the main cybersecurity-themed UI and responsive styling.

static/js/main.js
Contains frontend JavaScript functionality.

scripts/
Utility scripts for database initialization, sample templates, admin creation and database reset.

docs/
Additional setup, user, deployment and API documentation.

instance/
Contains the local SQLite database.

💻 Installation

1. Clone the repository

git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Ethical-Phishing-Simulation-Platform-main/Phishing

On Windows, you can also open PowerShell directly in the Phishing folder.

2. Create a virtual environment

Windows

python -m venv venv
.\venv\Scripts\Activate.ps1

Linux / macOS

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

📧 Email Sending Configuration

The application supports SMTP email sending.

The current application is configured by environment variables in a .env file.

Gmail configuration

Your project uses:

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-gmail-address@gmail.com
SMTP_PASSWORD=your-google-app-password
SMTP_FROM_NAME=Security Training Team
SMTP_FROM_EMAIL=your-gmail-address@gmail.com

What you entered when setting up email

There are two different Google/Gmail details involved:

Gmail address / Google account email

This is the email account used as the SMTP username.

Example:

SMTP_USERNAME=yourname@gmail.com

Google App Password

This is not your normal Gmail password.

It is a separate password generated from the Google Account after enabling 2-Step Verification.

Put the generated App Password in:

SMTP_PASSWORD=YOUR_APP_PASSWORD

The application then uses these values to authenticate to Gmail SMTP.

Example .env

Create a file named:

.env

inside the Phishing folder:

FLASK_ENV=development

SECRET_KEY=replace-with-a-random-secret-key

DATABASE_URL=sqlite:///phishing_sim.db

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-google-app-password

SMTP_FROM_NAME=Security Training Team
SMTP_FROM_EMAIL=your-email@gmail.com

APP_NAME=Phishing Simulation Platform
APP_HOST=127.0.0.1
APP_PORT=5000

DEBUG=True

⚠️ Never commit .env

Your .env file can contain your email account information and SMTP App Password.

Do not upload it to GitHub.

Add this to .gitignore:

.env
venv/
__pycache__/
*.pyc

It is also recommended to avoid committing a production/local database containing real target information.

🧪 Simulation Mode

If SMTP credentials are not configured, the application can operate in simulation mode.

Instead of actually sending an email, it records the message as sent and prints a message similar to:

[SIMULATION] Email would be sent to user@example.com

This is useful for development and UI testing.

🗄️ Database Setup

Initialize the database:

python scripts/init_db.py

Add sample templates:

python scripts/add_sample_templates.py

The application also creates the database tables when it starts.

👤 Create an Admin User

Use:

python scripts/create_admin.py

Follow the prompts for:

Username
Email
Password

The application stores the password as a hash rather than plain text.

▶️ Run the Application

From the Phishing directory:

python app.py

The application normally runs at:

http://127.0.0.1:5000

Open that address in your browser.

🖥️ Application Pages

Page

Purpose

/

Main dashboard

/campaigns

View all campaigns

/campaign/create

Create a campaign

/templates

View and manage email templates

/template/create

Create a new template

/analytics

View campaign analytics

/campaign/<id>

View campaign details

📊 Dashboard

The dashboard provides an overview of:

Total campaigns

Total email templates

Total authorized targets

Active campaigns

Recent campaign activity

The interface uses a cybersecurity/SOC-inspired dark theme with cyan, blue, purple and green accent colors.

📧 Email Templates

Templates contain:

Template name

Category

Difficulty

Email subject

HTML email body

HTML landing page

Templates can be previewed before being used in a campaign.

A template that is already associated with a campaign is protected from deletion so that campaign history is not accidentally broken.

🎯 Campaigns

A campaign contains:

Campaign name

Description

Selected email template

Authorized targets

Campaign status

Tracking statistics

Campaign activity can be monitored from the campaign details page and analytics dashboard.

📈 Analytics

The analytics dashboard provides:

Total campaigns

Total targets

Total sent emails

Total opened emails

Total clicked links

Total submissions

Overall open rate

Overall click rate

Overall submit rate

Campaign-level performance

🎓 Security Awareness Training

After a simulated phishing interaction, the platform can display educational content explaining:

How phishing attacks work

How to identify suspicious messages

How to inspect links

Why urgent requests should be verified

The importance of multi-factor authentication

How to report suspicious emails

The goal is education and awareness, not punishment.

🔐 Security Considerations

For a real deployment:

Use explicit written authorization.

Do not collect real passwords.

Do not store unnecessary sensitive information.

Keep SMTP credentials outside source control.

Use HTTPS.

Add proper authentication and authorization.

Restrict access to administrators.

Run the platform in an isolated environment.

Protect the database.

Review logs regularly.

Perform security audits.

Use a dedicated training email account rather than a personal email account.

⚠️ Responsible Use

This project is intended for:

Authorized security-awareness training
        +
Controlled phishing simulations
        +
Education
        +
Security improvement

It must not be used for:

Unauthorized phishing
Credential theft
Real-world social engineering
Malware distribution
Impersonation without authorization
Collecting real passwords or sensitive credentials

📚 Documentation

Additional documentation is available in:

docs/
├── SETUP.md
├── USER_GUIDE.md
├── DEPLOYMENT.md
└── API.md

🧹 Before Publishing to GitHub

Before pushing the project, check:

git status

Make sure you do not see:

.env
venv/
__pycache__/

If necessary, create/update .gitignore:

.env
venv/
__pycache__/
*.pyc

Also inspect your Git history if a secret was ever committed previously. Simply deleting .env from the current folder does not remove an already-committed secret from Git history.

🚀 Future Improvements

Possible future enhancements include:

Admin authentication UI

Role-based access control

Campaign scheduling

More detailed charts

Exportable analytics reports

Audit logging

Email delivery status

Campaign pause/resume controls

Improved target management

Production deployment configuration

👩‍💻 Project

Ethical Phishing Simulation Platform

Built for authorized cybersecurity awareness and training.