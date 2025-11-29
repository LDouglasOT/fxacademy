# fxAcademy Django Web App

A comprehensive forex trading academy web application built with Django.

## Features

- User authentication and registration
- Email verification
- Dashboard for users
- Course enrollment
- Signal purchases
- Admin panel

## Deployment to VPS

### Prerequisites

- Ubuntu/Debian VPS
- Python 3.8+
- PostgreSQL
- Nginx
- SSL certificate (Let's Encrypt recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd fxAcademy
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r req.txt
   ```

4. **Set up PostgreSQL database:**
   ```bash
   sudo -u postgres createdb fxacademy_db
   sudo -u postgres createuser fxacademy_user
   sudo -u postgres psql -c "ALTER USER fxacademy_user PASSWORD 'your-password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE fxacademy_db TO fxacademy_user;"
   ```

5. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

### Server Configuration

1. **Install and configure Gunicorn:**
   - Copy `gunicorn.service` to `/etc/systemd/system/`
   - Update paths in the service file
   - Enable and start the service:
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl enable gunicorn
     sudo systemctl start gunicorn
     ```

2. **Configure Nginx:**
   - Copy `nginx.conf` to `/etc/nginx/sites-available/fxacademy`
   - Update paths and domain name
   - Create symlink: `sudo ln -s /etc/nginx/sites-available/fxacademy /etc/nginx/sites-enabled/`
   - Test config: `sudo nginx -t`
   - Restart nginx: `sudo systemctl restart nginx`

3. **SSL Certificate (Let's Encrypt):**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

### Deployment Script

Use the provided `scripts/deploy.sh` for updates:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Security Notes

- Change default SECRET_KEY
- Use strong database passwords
- Keep dependencies updated
- Monitor logs regularly
- Set up firewall (ufw)

### Troubleshooting

- Check Gunicorn logs: `sudo journalctl -u gunicorn`
- Check Nginx logs: `/var/log/nginx/error.log`
- Test Gunicorn directly: `gunicorn --config gunicorn.conf.py fxAcademy.wsgi:application`

## Development

For local development:

```bash
python manage.py runserver
```

## License

[Your License Here]