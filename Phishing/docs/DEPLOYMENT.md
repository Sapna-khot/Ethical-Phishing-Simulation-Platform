"""# Production Deployment

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure production SMTP
- [ ] Set up database backups
- [ ] Implement authentication
- [ ] Configure firewall

## Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name phishing-sim.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```
""",