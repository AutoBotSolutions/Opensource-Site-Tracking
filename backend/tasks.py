from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PageView, Event, Session
from datetime import datetime, timedelta
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def cleanup_old_data():
    """Delete data older than retention period"""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=settings.DATA_RETENTION_DAYS)
        
        # Delete old pageviews
        pageviews_deleted = db.query(PageView).filter(
            PageView.created_at < cutoff_date
        ).delete()
        
        # Delete old events
        events_deleted = db.query(Event).filter(
            Event.created_at < cutoff_date
        ).delete()
        
        # Delete old sessions
        sessions_deleted = db.query(Session).filter(
            Session.created_at < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(
            f"Data cleanup completed: {pageviews_deleted} pageviews, "
            f"{events_deleted} events, {sessions_deleted} sessions deleted"
        )
    except Exception as e:
        logger.error(f"Data cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    """Start the background task scheduler"""
    # Run cleanup daily at 2 AM
    scheduler.add_job(
        cleanup_old_data,
        'cron',
        hour=2,
        minute=0,
        id='data_cleanup'
    )
    scheduler.start()
    logger.info("Scheduler started")
