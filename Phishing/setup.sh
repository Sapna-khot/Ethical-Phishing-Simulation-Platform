"""#!/bin/bash
echo "🎣 Setting up Phishing Simulation Platform..."

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Edit .env with your settings"
fi

python scripts/init_db.py
python scripts/add_sample_templates.py

echo "✅ Setup complete!"
echo "Run: python app.py"
"""