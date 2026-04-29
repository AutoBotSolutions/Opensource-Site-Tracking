# Backup and Recovery Guide

This guide covers backup and recovery procedures for OpenSite Analytics.

## Overview

Regular backups are essential for data protection and disaster recovery. This guide covers:

- Database backups
- File system backups
- Configuration backups
- Automated backup strategies
- Recovery procedures

## Database Backups

### SQLite Backups

#### Manual Backup

```bash
# Copy database file
cp backend/analytics.db backend/analytics.db.backup.$(date +%Y%m%d_%H%M%S)

# Compress backup
gzip backend/analytics.db.backup.$(date +%Y%m%d_%H%M%S)
```

#### Automated Backup Script

Create `backup-sqlite.sh`:

```bash
#!/bin/bash

# Configuration
DB_PATH="/home/robbie/Desktop/opensource-site-tracking/backend/analytics.db"
BACKUP_DIR="/backups/analytics"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/analytics_$TIMESTAMP.db"
cp "$DB_PATH" "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Remove old backups
find "$BACKUP_DIR" -name "analytics_*.db.gz" -mtime +$RETENTION_DAYS -delete

# Log
echo "Backup created: analytics_$TIMESTAMP.db.gz"
```

Make executable:
```bash
chmod +x backup-sqlite.sh
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup-sqlite.sh
```

#### Backup While Database is in Use

```python
# backup_sqlite.py
import sqlite3
import shutil
from datetime import datetime

def backup_sqlite_online(db_path, backup_path):
    """Backup SQLite database while it's in use"""
    conn = sqlite3.connect(db_path)
    
    # Create backup
    backup = sqlite3.connect(backup_path)
    conn.backup(backup)
    
    backup.close()
    conn.close()
    
    print(f"Backup created: {backup_path}")

if __name__ == "__main__":
    db_path = "backend/analytics.db"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backups/analytics_{timestamp}.db"
    backup_sqlite_online(db_path, backup_path)
```

### PostgreSQL Backups

#### Manual Backup

```bash
# Full backup
pg_dump -U opensite_user -d opensite > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -U opensite_user -d opensite | gzip > backup_$(date +%Y%m%d).sql.gz

# Schema only
pg_dump -U opensite_user -d opensite --schema-only > schema_$(date +%Y%m%d).sql

# Data only
pg_dump -U opensite_user -d opensite --data-only > data_$(date +%Y%m%d).sql
```

#### Automated Backup Script

Create `backup-postgres.sh`:

```bash
#!/bin/bash

# Configuration
DB_USER="opensite_user"
DB_NAME="opensite"
BACKUP_DIR="/backups/postgres"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/opensite_$TIMESTAMP.sql.gz"

pg_dump -U $DB_USER -d $DB_NAME | gzip > "$BACKUP_FILE"

# Remove old backups
find "$BACKUP_DIR" -name "opensite_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup created: opensite_$TIMESTAMP.sql.gz"
```

#### Cron Job

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup-postgres.sh
```

### MySQL Backups

#### Manual Backup

```bash
# Full backup
mysqldump -u opensite_user -p opensite > backup_$(date +%Y%m%d).sql

# Compressed backup
mysqldump -u opensite_user -p opensite | gzip > backup_$(date +%Y%m%d).sql.gz
```

#### Automated Backup Script

Create `backup-mysql.sh`:

```bash
#!/bin/bash

# Configuration
DB_USER="opensite_user"
DB_PASS="password"
DB_NAME="opensite"
BACKUP_DIR="/backups/mysql"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/opensite_$TIMESTAMP.sql.gz"

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > "$BACKUP_FILE"

# Remove old backups
find "$BACKUP_DIR" -name "opensite_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup created: opensite_$TIMESTAMP.sql.gz"
```

## File System Backups

### Configuration Files

```bash
#!/bin/bash

# Configuration
PROJECT_DIR="/home/robbie/Desktop/opensource-site-tracking"
BACKUP_DIR="/backups/config"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup configuration files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
  "$PROJECT_DIR/backend/.env" \
  "$PROJECT_DIR/frontend/.env.local"

# Remove old backups
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Config backup created: config_$TIMESTAMP.tar.gz"
```

### Full Application Backup

```bash
#!/bin/bash

# Configuration
PROJECT_DIR="/home/robbie/Desktop/opensource-site-tracking"
BACKUP_DIR="/backups/full"
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Exclude database and node_modules
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/full_$TIMESTAMP.tar.gz" \
  --exclude="$PROJECT_DIR/backend/analytics.db" \
  --exclude="$PROJECT_DIR/backend/venv" \
  --exclude="$PROJECT_DIR/frontend/node_modules" \
  --exclude="$PROJECT_DIR/frontend/.next" \
  "$PROJECT_DIR"

# Remove old backups
find "$BACKUP_DIR" -name "full_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Full backup created: full_$TIMESTAMP.tar.gz"
```

## Cloud Backups

### AWS S3

```bash
#!/bin/bash

# Configuration
BUCKET_NAME="opensite-backups"
BACKUP_DIR="/backups"
AWS_PROFILE="default"

# Upload to S3
aws s3 sync "$BACKUP_DIR" "s3://$BUCKET_NAME" --profile "$AWS_PROFILE"

# Set lifecycle policy for old backups
aws s3api put-bucket-lifecycle-configuration \
  --bucket "$BUCKET_NAME" \
  --lifecycle-configuration file://lifecycle.json
```

### Google Cloud Storage

```bash
#!/bin/bash

# Configuration
BUCKET_NAME="opensite-backups"
BACKUP_DIR="/backups"

# Upload to GCS
gsutil -m rsync -r "$BACKUP_DIR" "gs://$BUCKET_NAME"
```

## Recovery Procedures

### SQLite Recovery

#### Restore from Backup

```bash
# Stop backend
sudo systemctl stop opensite-backend

# Restore database
cp backups/analytics_20260429_020000.db.gz .
gunzip analytics_20260429_020000.db.gz
cp analytics_20260429_020000.db backend/analytics.db

# Start backend
sudo systemctl start opensite-backend
```

#### Recover from Corruption

```bash
# Try to recover using SQLite
sqlite3 corrupted.db ".recover" | sqlite3 recovered.db

# Check integrity
sqlite3 recovered.db "PRAGMA integrity_check;"

# If successful, replace original
cp recovered.db backend/analytics.db
```

### PostgreSQL Recovery

#### Restore from Backup

```bash
# Drop existing database
dropdb -U opensite_user opensite

# Create new database
createdb -U opensite_user opensite

# Restore from backup
gunzip backup_20260429.sql.gz
psql -U opensite_user -d opensite < backup_20260429.sql

# Or use pg_restore for custom format backups
pg_restore -U opensite_user -d opensite backup.dump
```

#### Point-in-Time Recovery

```bash
# Configure recovery in postgresql.conf
restore_command = 'cp /backups/wal/%f %p'
recovery_target_time = '2026-04-29 14:00:00'

# Start PostgreSQL
pg_ctl start -D /var/lib/postgresql/data
```

### MySQL Recovery

#### Restore from Backup

```bash
# Create database if not exists
mysql -u opensite_user -p -e "CREATE DATABASE IF NOT EXISTS opensite"

# Restore from backup
gunzip backup_20260429.sql.gz
mysql -u opensite_user -p opensite < backup_20260429.sql
```

## Disaster Recovery

### Complete System Recovery

1. **Restore Operating System**
   - Reinstall OS
   - Apply security updates
   - Configure network

2. **Install Dependencies**
   ```bash
   # Python
   apt install python3 python3-pip python3-venv
   
   # Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
   apt install -y nodejs
   
   # Database
   apt install postgresql
   ```

3. **Restore Application**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/opensource-site-tracking.git
   cd opensource-site-tracking
   
   # Restore configuration
   tar -xzf /backups/config/config_latest.tar.gz
   ```

4. **Restore Database**
   ```bash
   # Follow database-specific recovery procedures
   ```

5. **Start Services**
   ```bash
   # Backend
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   
   # Frontend
   cd frontend
   npm install
   npm run build
   npm start
   ```

6. **Verify Recovery**
   - Check backend health endpoint
   - Verify frontend loads
   - Test login functionality
   - Verify analytics data

## Monitoring

### Backup Monitoring

```python
# monitor_backups.py
import os
import smtplib
from datetime import datetime, timedelta

def check_backups(backup_dir, max_age_hours=24):
    """Check if backups are recent enough"""
    now = datetime.now()
    threshold = now - timedelta(hours=max_age_hours)
    
    backups = os.listdir(backup_dir)
    if not backups:
        send_alert("No backups found!")
        return False
    
    latest_backup = max(backups)
    backup_time = datetime.strptime(latest_backup.split('_')[1], "%Y%m%d")
    
    if backup_time < threshold:
        send_alert(f"Backup is too old: {latest_backup}")
        return False
    
    return True

def send_alert(message):
    """Send email alert"""
    # Implement email sending
    print(f"ALERT: {message}")
```

### Backup Verification

```bash
#!/bin/bash

# Test backup integrity
for backup in /backups/analytics/*.db.gz; do
    echo "Testing: $backup"
    gunzip -t "$backup"
    if [ $? -eq 0 ]; then
        echo "✓ Backup is valid"
    else
        echo "✗ Backup is corrupted"
        send_alert "Corrupted backup: $backup"
    fi
done
```

## Best Practices

1. **Automate backups** - Use cron jobs or scheduled tasks
2. **Test restores regularly** - Verify backups can be restored
3. **Offsite storage** - Store backups in different physical location
4. **Encryption** - Encrypt sensitive backup data
5. **Retention policy** - Define and enforce backup retention
6. **Monitor backups** - Alert on backup failures
7. **Document procedures** - Maintain recovery documentation
8. **Version control** - Track configuration changes
9. **Incremental backups** - For large databases, consider incremental backups
10. **Access control** - Restrict backup access to authorized personnel

## Backup Checklist

### Daily
- [ ] Automated database backup completed
- [ ] Backup integrity verified
- [ ] Backup stored in offsite location
- [ ] Backup monitoring alerts checked

### Weekly
- [ ] Full application backup
- [ ] Restore test performed
- [ ] Backup size reviewed
- [ ] Retention policy enforced

### Monthly
- [ ] Disaster recovery drill
- [ ] Backup procedures reviewed
- [ ] Storage capacity checked
- [ ] Recovery documentation updated
