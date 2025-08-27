"""Assessment-related Celery tasks."""

from celery import current_task
from structlog import get_logger

from app.main import celery_app
from app.services.ai_service import AIService
from app.services.assessment_service import AssessmentService

logger = get_logger()


@celery_app.task(bind=True)
def score_assessment(self, assessment_id: str):
    """Score an assessment using AI."""
    try:
        logger.info("Starting assessment scoring", assessment_id=assessment_id)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": 100, "status": "Processing assessment..."}
        )
        
        # Initialize services
        ai_service = AIService()
        assessment_service = AssessmentService()
        
        # Get assessment data
        assessment = assessment_service.get_assessment(assessment_id)
        if not assessment:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 25, "total": 100, "status": "Analyzing responses..."}
        )
        
        # Score assessment using AI
        score_result = ai_service.score_assessment(assessment)
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 75, "total": 100, "status": "Saving results..."}
        )
        
        # Save results
        assessment_service.save_assessment_result(assessment_id, score_result)
        
        logger.info("Assessment scoring completed", assessment_id=assessment_id)
        
        return {
            "status": "SUCCESS",
            "assessment_id": assessment_id,
            "score": score_result.score,
            "category": score_result.category,
        }
        
    except Exception as exc:
        logger.error("Assessment scoring failed", assessment_id=assessment_id, error=str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@celery_app.task(bind=True)
def generate_assessment_report(self, assessment_id: str):
    """Generate a detailed report for an assessment."""
    try:
        logger.info("Starting assessment report generation", assessment_id=assessment_id)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": 100, "status": "Generating report..."}
        )
        
        # Initialize services
        ai_service = AIService()
        assessment_service = AssessmentService()
        
        # Get assessment data
        assessment = assessment_service.get_assessment(assessment_id)
        if not assessment:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 50, "total": 100, "status": "Analyzing data..."}
        )
        
        # Generate report using AI
        report = ai_service.generate_assessment_report(assessment)
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": 90, "total": 100, "status": "Saving report..."}
        )
        
        # Save report
        assessment_service.save_assessment_report(assessment_id, report)
        
        logger.info("Assessment report generation completed", assessment_id=assessment_id)
        
        return {
            "status": "SUCCESS",
            "assessment_id": assessment_id,
            "report_id": report.id,
        }
        
    except Exception as exc:
        logger.error("Assessment report generation failed", assessment_id=assessment_id, error=str(exc))
        raise self.retry(exc=exc, countdown=60, max_retries=3)