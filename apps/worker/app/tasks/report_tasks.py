"""Report-related Celery tasks."""

from celery import current_task
from structlog import get_logger

from app.main import celery_app
from app.services.report_service import ReportService

logger = get_logger()


@celery_app.task(bind=True)
def generate_user_report(self, user_id: str, report_type: str = "comprehensive"):
    """Generate a comprehensive report for a user."""
    try:
        logger.info("Starting user report generation", user_id=user_id, report_type=report_type)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": 100, "status": "Gathering user data..."}
        )
        
        # Initialize service
        report_service = ReportService()
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 25, "total": 100, "status": "Analyzing workouts..."}
        )
        
        # Generate report
        report = report_service.generate_user_report(user_id, report_type)
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 75, "total": 100, "status": "Saving report..."}
        )
        
        # Save report
        report_id = report_service.save_report(report)
        
        logger.info("User report generation completed", user_id=user_id, report_id=report_id)
        
        return {
            "status": "SUCCESS",
            "user_id": user_id,
            "report_id": report_id,
            "report_type": report_type,
        }
        
    except Exception as exc:
        logger.error("User report generation failed", user_id=user_id, error=str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@celery_app.task(bind=True)
def generate_bulk_reports(self, user_ids: list[str], report_type: str = "comprehensive"):
    """Generate reports for multiple users."""
    try:
        logger.info("Starting bulk report generation", user_count=len(user_ids), report_type=report_type)
        
        results = []
        total_users = len(user_ids)
        
        for i, user_id in enumerate(user_ids):
            # Update task status
            progress = int((i / total_users) * 100)
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": progress,
                    "total": 100,
                    "status": f"Processing user {i+1} of {total_users}..."
                }
            )
            
            try:
                # Generate individual report
                result = generate_user_report.delay(user_id, report_type)
                results.append({"user_id": user_id, "task_id": result.id})
                
            except Exception as exc:
                logger.error("Failed to generate report for user", user_id=user_id, error=str(exc))
                results.append({"user_id": user_id, "error": str(exc)})
        
        logger.info("Bulk report generation completed", total_users=total_users, successful=len([r for r in results if "error" not in r]))
        
        return {
            "status": "SUCCESS",
            "total_users": total_users,
            "results": results,
        }
        
    except Exception as exc:
        logger.error("Bulk report generation failed", error=str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@celery_app.task(bind=True)
def generate_system_report(self, report_type: str = "daily"):
    """Generate system-wide reports."""
    try:
        logger.info("Starting system report generation", report_type=report_type)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": 100, "status": "Collecting system data..."}
        )
        
        # Initialize service
        report_service = ReportService()
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 50, "total": 100, "status": "Generating system report..."}
        )
        
        # Generate system report
        report = report_service.generate_system_report(report_type)
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 90, "total": 100, "status": "Saving system report..."}
        )
        
        # Save report
        report_id = report_service.save_system_report(report)
        
        logger.info("System report generation completed", report_type=report_type, report_id=report_id)
        
        return {
            "status": "SUCCESS",
            "report_id": report_id,
            "report_type": report_type,
        }
        
    except Exception as exc:
        logger.error("System report generation failed", report_type=report_type, error=str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)