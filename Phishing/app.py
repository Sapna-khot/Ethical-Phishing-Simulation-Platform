"""
Ethical Phishing Simulation Platform
Main Application File

WARNING: For authorized educational use only!
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///phishing_sim.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SMTP Configuration
SMTP_CONFIG = {
    'server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', 587)),
    'username': os.getenv('SMTP_USERNAME', ''),
    'password': os.getenv('SMTP_PASSWORD', ''),
    'from_name': os.getenv('SMTP_FROM_NAME', 'Security Training'),
    'from_email': os.getenv('SMTP_FROM_EMAIL', 'security@example.com')
}

db = SQLAlchemy(app)


# ==================== DATABASE MODELS ====================

class Campaign(db.Model):
    """Campaign model for phishing simulations"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    launched_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='draft')  # draft, active, completed, paused
    targets = db.relationship('Target', backref='campaign', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Campaign {self.name}>'


class Template(db.Model):
    """Email template model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    landing_page = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))  # credential_harvesting, urgent_action, ceo_fraud, etc.
    difficulty = db.Column(db.String(50), default='medium')  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    campaigns = db.relationship('Campaign', backref='template', lazy=True)

    def __repr__(self):
        return f'<Template {self.name}>'


class Target(db.Model):
    """Target/recipient model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200))
    department = db.Column(db.String(100))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)

    # Tracking timestamps
    sent_at = db.Column(db.DateTime)
    opened_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    submitted_at = db.Column(db.DateTime)

    # Data capture (for analysis only - never use maliciously!)
    submitted_data = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))

    def __repr__(self):
        return f'<Target {self.email}>'


class EducationalContent(db.Model):
    """Educational content shown after phishing attempt"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tips = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EducationalContent {self.title}>'


class User(db.Model):
    """Admin user model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='admin')  # admin, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ==================== HELPER FUNCTIONS ====================

def send_phishing_email(target, template, campaign):
    """Send phishing email to target"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = template.subject
        msg['From'] = f"{SMTP_CONFIG['from_name']} <{SMTP_CONFIG['from_email']}>"
        msg['To'] = target.email

        # Generate tracking URLs
        tracking_url = url_for('track_click', token=target.token, _external=True)
        pixel_url = url_for('track_open', token=target.token, _external=True)

        # Replace template variables
        body_html = template.body
        body_html = body_html.replace('{{tracking_url}}', tracking_url)
        body_html = body_html.replace('{{target_email}}', target.email)
        body_html = body_html.replace('{{target_name}}', target.name or target.email)

        # Add tracking pixel at the end
        body_html += f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'

        # Attach HTML body
        msg.attach(MIMEText(body_html, 'html'))

        # Send email
        if SMTP_CONFIG['username'] and SMTP_CONFIG['password']:
            with smtplib.SMTP(SMTP_CONFIG['server'], SMTP_CONFIG['port']) as server:
                server.starttls()
                server.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                server.send_message(msg)

            # Update sent timestamp
            target.sent_at = datetime.utcnow()
            db.session.commit()
            return True
        else:
            # Simulation mode - just mark as sent
            target.sent_at = datetime.utcnow()
            db.session.commit()
            print(f"[SIMULATION] Email would be sent to {target.email}")
            return True

    except Exception as e:
        print(f"Error sending email to {target.email}: {e}")
        return False


def calculate_campaign_stats(campaign):
    """Calculate statistics for a campaign"""
    total = len(campaign.targets)
    sent = sum(1 for t in campaign.targets if t.sent_at)
    opened = sum(1 for t in campaign.targets if t.opened_at)
    clicked = sum(1 for t in campaign.targets if t.clicked_at)
    submitted = sum(1 for t in campaign.targets if t.submitted_at)

    return {
        'total': total,
        'sent': sent,
        'opened': opened,
        'clicked': clicked,
        'submitted': submitted,
        'open_rate': round(opened / sent * 100, 1) if sent > 0 else 0,
        'click_rate': round(clicked / sent * 100, 1) if sent > 0 else 0,
        'submit_rate': round(submitted / sent * 100, 1) if sent > 0 else 0
    }


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Dashboard homepage"""
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).limit(5).all()
    total_campaigns = Campaign.query.count()
    total_templates = Template.query.count()
    total_targets = Target.query.count()

    # Calculate overall stats
    active_campaigns = Campaign.query.filter_by(status='active').all()
    overall_stats = {
        'total_campaigns': total_campaigns,
        'total_templates': total_templates,
        'total_targets': total_targets,
        'active_campaigns': len(active_campaigns)
    }

    return render_template('index.html',
                           campaigns=campaigns,
                           stats=overall_stats)


@app.route('/campaigns')
def campaigns():
    """List all campaigns"""
    all_campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('campaigns.html', campaigns=all_campaigns)


@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    """Create new campaign"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        template_id = request.form.get('template_id')

        if not name or not template_id:
            flash('Campaign name and template are required', 'error')
            return redirect(url_for('create_campaign'))

        campaign = Campaign(
            name=name,
            description=description,
            template_id=template_id,
            status='draft'
        )
        db.session.add(campaign)
        db.session.commit()

        flash(f'Campaign "{name}" created successfully!', 'success')
        return redirect(url_for('campaign_detail', campaign_id=campaign.id))

    templates = Template.query.all()
    return render_template('create_campaign.html', templates=templates)


@app.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    """View campaign details and statistics"""
    campaign = Campaign.query.get_or_404(campaign_id)
    stats = calculate_campaign_stats(campaign)

    return render_template('campaign_detail.html',
                           campaign=campaign,
                           stats=stats)


@app.route('/campaign/<int:campaign_id>/add_targets', methods=['POST'])
def add_targets(campaign_id):
    """Add targets to campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)

    emails_text = request.form.get('emails', '')
    emails = [e.strip() for e in emails_text.split('\n') if e.strip()]

    added = 0
    for email in emails:
        if email and '@' in email:
            # Check if already exists in this campaign
            existing = Target.query.filter_by(
                email=email,
                campaign_id=campaign_id
            ).first()

            if not existing:
                token = secrets.token_urlsafe(32)
                target = Target(
                    email=email,
                    campaign_id=campaign_id,
                    token=token
                )
                db.session.add(target)
                added += 1

    db.session.commit()
    flash(f'Added {added} targets to campaign', 'success')
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))


@app.route('/campaign/<int:campaign_id>/launch', methods=['POST'])
def launch_campaign(campaign_id):
    """Launch a campaign and send emails"""
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.status != 'draft':
        flash('Campaign already launched', 'warning')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))

    template = Template.query.get(campaign.template_id)

    if not template:
        flash('Template not found', 'error')
        return redirect(url_for('campaign_detail', campaign_id=campaign_id))

    # Send emails to all targets
    sent_count = 0
    for target in campaign.targets:
        if not target.sent_at:
            if send_phishing_email(target, template, campaign):
                sent_count += 1

    # Update campaign status
    campaign.status = 'active'
    campaign.launched_at = datetime.utcnow()
    db.session.commit()

    flash(f'Campaign launched! Sent {sent_count} emails.', 'success')
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))


@app.route('/campaign/<int:campaign_id>/pause', methods=['POST'])
def pause_campaign(campaign_id):
    """Pause an active campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.status = 'paused'
    db.session.commit()

    flash('Campaign paused', 'info')
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))


@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    """Delete a campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign_name = campaign.name

    db.session.delete(campaign)
    db.session.commit()

    flash(f'Campaign "{campaign_name}" deleted', 'success')
    return redirect(url_for('campaigns'))


@app.route('/track/open/<token>')
def track_open(token):
    """Track email opens via tracking pixel"""
    target = Target.query.filter_by(token=token).first()

    if target and not target.opened_at:
        target.opened_at = datetime.utcnow()
        target.ip_address = request.remote_addr
        target.user_agent = request.headers.get('User-Agent', '')
        db.session.commit()

    # Return 1x1 transparent GIF
    from flask import Response
    gif_data = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return Response(gif_data, mimetype='image/gif')


@app.route('/track/click/<token>')
def track_click(token):
    """Track link clicks and redirect to landing page"""
    target = Target.query.filter_by(token=token).first()

    if not target:
        return render_template('error.html', message='Invalid link'), 404

    # Track click
    if not target.clicked_at:
        target.clicked_at = datetime.utcnow()
        target.ip_address = request.remote_addr
        target.user_agent = request.headers.get('User-Agent', '')
        db.session.commit()

    # Get landing page
    campaign = Campaign.query.get(target.campaign_id)
    template = Template.query.get(campaign.template_id)

    # Replace token in landing page
    landing_html = template.landing_page.replace('{{token}}', token)

    return render_template('landing.html',
                           content=landing_html,
                           token=token)


@app.route('/submit/<token>', methods=['POST'])
def submit_data(token):
    """Handle form submissions from landing pages"""
    target = Target.query.filter_by(token=token).first()

    if not target:
        return render_template('error.html', message='Invalid submission'), 404

    # Track submission
    if not target.submitted_at:
        target.submitted_at = datetime.utcnow()
        # Store form data (for analysis only!)
        target.submitted_data = str(dict(request.form))
        db.session.commit()

    # Redirect to educational content
    return redirect(url_for('education', token=token))


@app.route('/education/<token>')
def education(token):
    """Show educational content after phishing attempt"""
    target = Target.query.filter_by(token=token).first()

    if not target:
        return render_template('error.html', message='Invalid link'), 404

    # Get or create educational content
    content = EducationalContent.query.first()

    if not content:
        content = create_default_educational_content()

    return render_template('education.html',
                           content=content,
                           target=target)


def create_default_educational_content():
    """Create default educational content"""
    content = EducationalContent(
        title="You've Been Phished! (In a Safe Training Environment)",
        content="""
        <h2>This was a simulated phishing attack</h2>
        <p>Don't worry - this was a training exercise conducted by your organization's 
        security team. No real harm was done, but this demonstrates how easy it is to 
        fall for phishing attacks.</p>
        <p>Cybercriminals use similar techniques to steal credentials, install malware, 
        and compromise organizations every day.</p>
        """,
        tips="""
        <ul>
            <li><strong>Check the sender:</strong> Verify email addresses carefully, not just display names</li>
            <li><strong>Hover before clicking:</strong> See the real URL destination before clicking links</li>
            <li><strong>Look for urgency:</strong> Be suspicious of urgent requests for personal information</li>
            <li><strong>Check for mistakes:</strong> Look for spelling and grammar errors</li>
            <li><strong>Verify requests:</strong> Contact the sender through a different channel to confirm</li>
            <li><strong>Use 2FA:</strong> Enable two-factor authentication whenever possible</li>
            <li><strong>Report suspicious emails:</strong> Forward to your IT security team</li>
        </ul>
        """
    )
    db.session.add(content)
    db.session.commit()
    return content


@app.route('/templates')
def templates():
    """List all templates"""
    all_templates = Template.query.order_by(Template.created_at.desc()).all()
    return render_template('templates.html', templates=all_templates)


@app.route('/template/create', methods=['GET', 'POST'])
def create_template():
    """Create new email template"""
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        body = request.form.get('body')
        landing_page = request.form.get('landing_page')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty', 'medium')

        if not all([name, subject, body, landing_page, category]):
            flash('All fields are required', 'error')
            return redirect(url_for('create_template'))

        template = Template(
            name=name,
            subject=subject,
            body=body,
            landing_page=landing_page,
            category=category,
            difficulty=difficulty
        )
        db.session.add(template)
        db.session.commit()

        flash(f'Template "{name}" created successfully!', 'success')
        return redirect(url_for('templates'))

    return render_template('create_template.html')


@app.route('/template/<int:template_id>/preview')
def preview_template(template_id):
    """Preview a template"""
    template = Template.query.get_or_404(template_id)

    # Replace placeholders with sample data
    preview_body = template.body
    preview_body = preview_body.replace('{{tracking_url}}', '#')
    preview_body = preview_body.replace('{{target_email}}', 'user@example.com')
    preview_body = preview_body.replace('{{target_name}}', 'John Doe')

    return render_template('preview_template.html',
                           template=template,
                           preview_body=preview_body)


@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    campaigns = Campaign.query.filter(
        Campaign.status.in_(['active', 'completed'])
    ).all()

    # Overall statistics
    all_targets = Target.query.all()
    overall_stats = {
        'total_campaigns': Campaign.query.count(),
        'total_targets': len(all_targets),
        'total_sent': sum(1 for t in all_targets if t.sent_at),
        'total_opened': sum(1 for t in all_targets if t.opened_at),
        'total_clicked': sum(1 for t in all_targets if t.clicked_at),
        'total_submitted': sum(1 for t in all_targets if t.submitted_at)
    }

    # Calculate rates
    if overall_stats['total_sent'] > 0:
        overall_stats['overall_open_rate'] = round(
            overall_stats['total_opened'] / overall_stats['total_sent'] * 100, 1
        )
        overall_stats['overall_click_rate'] = round(
            overall_stats['total_clicked'] / overall_stats['total_sent'] * 100, 1
        )
        overall_stats['overall_submit_rate'] = round(
            overall_stats['total_submitted'] / overall_stats['total_sent'] * 100, 1
        )
    else:
        overall_stats['overall_open_rate'] = 0
        overall_stats['overall_click_rate'] = 0
        overall_stats['overall_submit_rate'] = 0

    return render_template('analytics.html',
                           campaigns=campaigns,
                           stats=overall_stats)


@app.route('/api/campaign/<int:campaign_id>/stats')
def api_campaign_stats(campaign_id):
    """API endpoint for campaign statistics"""
    campaign = Campaign.query.get_or_404(campaign_id)
    stats = calculate_campaign_stats(campaign)
    stats['name'] = campaign.name
    stats['status'] = campaign.status
    return jsonify(stats)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', message='Internal server error'), 500


# ==================== CLI COMMANDS ====================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def create_admin():
    """Create an admin user"""
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')

    user = User(username=username, email=email, role='admin')
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print(f'Admin user "{username}" created!')


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('✅ Database initialized')

    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    host = os.getenv('APP_HOST', '127.0.0.1')
    port = int(os.getenv('APP_PORT', 5000))

    print(f'\n🎣 Phishing Simulation Platform')
    print(f'   Running on http://{host}:{port}')
    print(f'   Press CTRL+C to quit\n')

    app.run(debug=debug_mode, host=host, port=port)