"""Fitness scoring algorithms for IR FitMark."""

import math
from typing import Dict, List, Tuple
from enum import Enum

from .models import AssessmentType, FitnessAssessment


class ScoreGrade(str, Enum):
    """Fitness score grade enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    NEEDS_IMPROVEMENT = "needs_improvement"


# Scoring thresholds for different assessment types
SCORING_THRESHOLDS = {
    AssessmentType.PUSHUP: {
        ScoreGrade.EXCELLENT: 90,
        ScoreGrade.GOOD: 75,
        ScoreGrade.AVERAGE: 60,
        ScoreGrade.POOR: 40,
    },
    AssessmentType.SITUP: {
        ScoreGrade.EXCELLENT: 90,
        ScoreGrade.GOOD: 75,
        ScoreGrade.AVERAGE: 60,
        ScoreGrade.POOR: 40,
    },
    AssessmentType.RUNNING: {
        ScoreGrade.EXCELLENT: 90,
        ScoreGrade.GOOD: 75,
        ScoreGrade.AVERAGE: 60,
        ScoreGrade.POOR: 40,
    },
    AssessmentType.FLEXIBILITY: {
        ScoreGrade.EXCELLENT: 90,
        ScoreGrade.GOOD: 75,
        ScoreGrade.AVERAGE: 60,
        ScoreGrade.POOR: 40,
    },
}

# Age and gender adjustment factors
AGE_ADJUSTMENTS = {
    "18-25": 1.0,
    "26-35": 0.95,
    "36-45": 0.90,
    "46-55": 0.85,
    "56+": 0.80,
}

GENDER_ADJUSTMENTS = {
    "male": 1.0,
    "female": 0.85,  # Adjusted for physiological differences
}


def get_score_grade(assessment_type: AssessmentType, score: float) -> ScoreGrade:
    """Get the grade for a given score and assessment type."""
    thresholds = SCORING_THRESHOLDS[assessment_type]
    
    if score >= thresholds[ScoreGrade.EXCELLENT]:
        return ScoreGrade.EXCELLENT
    elif score >= thresholds[ScoreGrade.GOOD]:
        return ScoreGrade.GOOD
    elif score >= thresholds[ScoreGrade.AVERAGE]:
        return ScoreGrade.AVERAGE
    elif score >= thresholds[ScoreGrade.POOR]:
        return ScoreGrade.POOR
    else:
        return ScoreGrade.NEEDS_IMPROVEMENT


def calculate_pushup_score(
    count: int,
    duration: float,
    age: int,
    gender: str,
    form_score: float = 1.0
) -> float:
    """
    Calculate pushup score based on count, duration, demographics, and form.
    
    Args:
        count: Number of pushups completed
        duration: Duration in seconds
        age: Age of the person
        gender: Gender ("male" or "female")
        form_score: Form quality score (0.0 to 1.0)
    
    Returns:
        Score out of 100
    """
    # Base score calculation (reps per minute)
    if duration <= 0:
        return 0.0
    
    reps_per_minute = (count / duration) * 60
    
    # Age group adjustment
    age_group = get_age_group(age)
    age_factor = AGE_ADJUSTMENTS.get(age_group, 0.8)
    
    # Gender adjustment
    gender_factor = GENDER_ADJUSTMENTS.get(gender.lower(), 1.0)
    
    # Calculate base score (assuming 30 reps/min = 100 points for 18-25 male)
    base_score = (reps_per_minute / 30) * 100
    
    # Apply demographic adjustments
    adjusted_score = base_score / (age_factor * gender_factor)
    
    # Apply form score
    final_score = adjusted_score * form_score
    
    # Cap at 100 and ensure minimum of 0
    return max(0.0, min(100.0, final_score))


def calculate_situp_score(
    count: int,
    duration: float,
    age: int,
    gender: str,
    form_score: float = 1.0
) -> float:
    """
    Calculate situp score based on count, duration, demographics, and form.
    
    Args:
        count: Number of situps completed
        duration: Duration in seconds
        age: Age of the person
        gender: Gender ("male" or "female")
        form_score: Form quality score (0.0 to 1.0)
    
    Returns:
        Score out of 100
    """
    if duration <= 0:
        return 0.0
    
    reps_per_minute = (count / duration) * 60
    
    # Age and gender adjustments
    age_group = get_age_group(age)
    age_factor = AGE_ADJUSTMENTS.get(age_group, 0.8)
    gender_factor = GENDER_ADJUSTMENTS.get(gender.lower(), 1.0)
    
    # Calculate base score (assuming 35 reps/min = 100 points)
    base_score = (reps_per_minute / 35) * 100
    
    # Apply adjustments
    adjusted_score = base_score / (age_factor * gender_factor)
    final_score = adjusted_score * form_score
    
    return max(0.0, min(100.0, final_score))


def calculate_running_score(
    distance: float,
    time: float,
    age: int,
    gender: str
) -> float:
    """
    Calculate running score based on distance, time, and demographics.
    
    Args:
        distance: Distance covered in meters
        time: Time taken in seconds
        age: Age of the person
        gender: Gender ("male" or "female")
    
    Returns:
        Score out of 100
    """
    if time <= 0 or distance <= 0:
        return 0.0
    
    # Calculate speed (m/s)
    speed = distance / time
    
    # Age and gender adjustments
    age_group = get_age_group(age)
    age_factor = AGE_ADJUSTMENTS.get(age_group, 0.8)
    gender_factor = GENDER_ADJUSTMENTS.get(gender.lower(), 1.0)
    
    # Calculate base score (assuming 4 m/s = 100 points for 18-25 male)
    base_score = (speed / 4.0) * 100
    
    # Apply adjustments
    adjusted_score = base_score / (age_factor * gender_factor)
    
    return max(0.0, min(100.0, adjusted_score))


def calculate_flexibility_score(
    reach_distance: float,
    age: int,
    gender: str
) -> float:
    """
    Calculate flexibility score based on reach distance and demographics.
    
    Args:
        reach_distance: Reach distance in centimeters
        age: Age of the person
        gender: Gender ("male" or "female")
    
    Returns:
        Score out of 100
    """
    # Age and gender adjustments
    age_group = get_age_group(age)
    age_factor = AGE_ADJUSTMENTS.get(age_group, 0.8)
    gender_factor = GENDER_ADJUSTMENTS.get(gender.lower(), 1.0)
    
    # Calculate base score (assuming 20cm = 100 points)
    base_score = (reach_distance / 20) * 100
    
    # Apply adjustments
    adjusted_score = base_score / (age_factor * gender_factor)
    
    return max(0.0, min(100.0, adjusted_score))


def get_age_group(age: int) -> str:
    """Get age group for scoring adjustments."""
    if age <= 25:
        return "18-25"
    elif age <= 35:
        return "26-35"
    elif age <= 45:
        return "36-45"
    elif age <= 55:
        return "46-55"
    else:
        return "56+"


def calculate_overall_fitness_score(assessments: List[FitnessAssessment]) -> float:
    """Calculate overall fitness score from multiple assessments."""
    if not assessments:
        return 0.0
    
    # Weight different assessment types
    weights = {
        AssessmentType.PUSHUP: 0.3,
        AssessmentType.SITUP: 0.25,
        AssessmentType.RUNNING: 0.3,
        AssessmentType.FLEXIBILITY: 0.15,
    }
    
    weighted_sum = 0.0
    total_weight = 0.0
    
    for assessment in assessments:
        weight = weights.get(assessment.assessment_type, 0.25)
        weighted_sum += assessment.score * weight
        total_weight += weight
    
    if total_weight == 0:
        return 0.0
    
    return weighted_sum / total_weight


def get_fitness_recommendations(
    assessments: List[FitnessAssessment]
) -> Dict[str, List[str]]:
    """Get fitness recommendations based on assessment scores."""
    recommendations = {
        "strengths": [],
        "improvements": [],
        "exercises": [],
    }
    
    for assessment in assessments:
        grade = get_score_grade(assessment.assessment_type, assessment.score)
        assessment_name = assessment.assessment_type.value.replace("_", " ").title()
        
        if grade in [ScoreGrade.EXCELLENT, ScoreGrade.GOOD]:
            recommendations["strengths"].append(
                f"Excellent {assessment_name.lower()} performance"
            )
        elif grade in [ScoreGrade.POOR, ScoreGrade.NEEDS_IMPROVEMENT]:
            recommendations["improvements"].append(
                f"Focus on improving {assessment_name.lower()}"
            )
            
            # Add specific exercise recommendations
            if assessment.assessment_type == AssessmentType.PUSHUP:
                recommendations["exercises"].extend([
                    "Practice wall push-ups and knee push-ups",
                    "Strengthen chest and arm muscles",
                    "Work on proper form and breathing"
                ])
            elif assessment.assessment_type == AssessmentType.SITUP:
                recommendations["exercises"].extend([
                    "Practice crunches and planks",
                    "Strengthen core muscles",
                    "Work on hip flexor flexibility"
                ])
            elif assessment.assessment_type == AssessmentType.RUNNING:
                recommendations["exercises"].extend([
                    "Start with walking and gradually increase pace",
                    "Focus on cardiovascular endurance",
                    "Practice proper running form"
                ])
            elif assessment.assessment_type == AssessmentType.FLEXIBILITY:
                recommendations["exercises"].extend([
                    "Daily stretching routine",
                    "Yoga or pilates classes",
                    "Focus on hamstring and back flexibility"
                ])
    
    return recommendations


def calculate_improvement_percentage(
    current_score: float,
    previous_score: float
) -> float:
    """Calculate improvement percentage between two scores."""
    if previous_score == 0:
        return 0.0
    
    return ((current_score - previous_score) / previous_score) * 100


def get_fitness_trends(assessments: List[FitnessAssessment]) -> Dict[str, float]:
    """Get fitness trends for each assessment type."""
    trends = {}
    
    # Group assessments by type
    by_type = {}
    for assessment in assessments:
        assessment_type = assessment.assessment_type.value
        if assessment_type not in by_type:
            by_type[assessment_type] = []
        by_type[assessment_type].append(assessment)
    
    # Calculate trends for each type
    for assessment_type, type_assessments in by_type.items():
        if len(type_assessments) < 2:
            trends[assessment_type] = 0.0
            continue
        
        # Sort by date
        sorted_assessments = sorted(
            type_assessments,
            key=lambda x: x.assessed_at
        )
        
        # Calculate trend (simple linear regression slope)
        scores = [a.score for a in sorted_assessments]
        n = len(scores)
        x_values = list(range(n))
        
        sum_x = sum(x_values)
        sum_y = sum(scores)
        sum_xy = sum(x * y for x, y in zip(x_values, scores))
        sum_x_squared = sum(x * x for x in x_values)
        
        if n * sum_x_squared - sum_x * sum_x == 0:
            trends[assessment_type] = 0.0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x * sum_x)
            trends[assessment_type] = slope
    
    return trends