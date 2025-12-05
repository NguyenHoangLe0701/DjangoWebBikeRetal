"""
Automated Database Backup Management
"""
import os
import subprocess
import shutil
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Manages automated database backups
    """
    
    def __init__(self):
        self.backup_dir = getattr(settings, 'BACKUP_DIR', os.path.join(settings.BASE_DIR, 'backups'))
        self.retention_days = getattr(settings, 'BACKUP_RETENTION_DAYS', 30)
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logger.info(f"Created backup directory: {self.backup_dir}")
    
    def create_backup(self, backup_type='full'):
        """
        Create database backup
        
        Args:
            backup_type: Type of backup ('full', 'incremental')
        
        Returns:
            str: Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{backup_type}_{timestamp}.sqlite3"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            # Get database path
            db_path = settings.DATABASES['default']['NAME']
            
            if not os.path.exists(db_path):
                logger.error(f"Database file not found: {db_path}")
                return None
            
            # Copy database file
            shutil.copy2(db_path, backup_path)
            
            # Compress backup
            compressed_path = f"{backup_path}.gz"
            subprocess.run(['gzip', backup_path], check=True)
            
            logger.info(f"Backup created: {compressed_path}")
            
            # Verify backup
            if self.verify_backup(compressed_path):
                logger.info(f"Backup verified: {compressed_path}")
                return compressed_path
            else:
                logger.error(f"Backup verification failed: {compressed_path}")
                os.remove(compressed_path)
                return None
                
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return None
    
    def verify_backup(self, backup_path):
        """
        Verify backup file integrity
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            bool: True if backup is valid
        """
        try:
            if not os.path.exists(backup_path):
                return False
            
            # Check file size
            if os.path.getsize(backup_path) == 0:
                return False
            
            # If compressed, try to decompress and check
            if backup_path.endswith('.gz'):
                import gzip
                with gzip.open(backup_path, 'rb') as f:
                    # Try to read first few bytes
                    f.read(100)
            
            return True
        except Exception as e:
            logger.error(f"Error verifying backup: {str(e)}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            deleted_count = 0
            
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {filename}")
            
            logger.info(f"Cleaned up {deleted_count} old backups")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning up backups: {str(e)}")
            return 0
    
    def list_backups(self):
        """List all backups"""
        backups = []
        
        try:
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                
                if os.path.isfile(file_path) and filename.startswith('backup_'):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    file_size = os.path.getsize(file_path)
                    
                    backups.append({
                        'filename': filename,
                        'path': file_path,
                        'created_at': file_time,
                        'size': file_size,
                        'size_mb': round(file_size / (1024 * 1024), 2)
                    })
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            
            return backups
        except Exception as e:
            logger.error(f"Error listing backups: {str(e)}")
            return []
    
    def restore_backup(self, backup_path):
        """
        Restore database from backup
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            bool: True if restore successful
        """
        try:
            db_path = settings.DATABASES['default']['NAME']
            
            # Decompress if needed
            if backup_path.endswith('.gz'):
                import gzip
                temp_path = backup_path[:-3]  # Remove .gz
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(temp_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path = temp_path
            
            # Backup current database before restore
            current_backup = f"{db_path}.before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if os.path.exists(db_path):
                shutil.copy2(db_path, current_backup)
            
            # Restore backup
            shutil.copy2(backup_path, db_path)
            
            logger.info(f"Database restored from: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            return False


def create_daily_backup():
    """Create daily backup (can be called from cron)"""
    manager = BackupManager()
    backup_path = manager.create_backup('full')
    
    if backup_path:
        # Cleanup old backups
        manager.cleanup_old_backups()
        return backup_path
    return None

