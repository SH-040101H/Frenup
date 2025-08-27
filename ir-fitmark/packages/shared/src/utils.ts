import { SCORING_THRESHOLDS } from './constants';
import type { FitnessAssessment } from './types';

// Score Calculation Utilities
export function getScoreGrade(assessmentType: keyof typeof SCORING_THRESHOLDS, score: number): string {
  const thresholds = SCORING_THRESHOLDS[assessmentType];
  
  if (score >= thresholds.EXCELLENT) return 'Excellent';
  if (score >= thresholds.GOOD) return 'Good';
  if (score >= thresholds.AVERAGE) return 'Average';
  if (score >= thresholds.POOR) return 'Poor';
  return 'Needs Improvement';
}

export function getScoreColor(assessmentType: keyof typeof SCORING_THRESHOLDS, score: number): string {
  const thresholds = SCORING_THRESHOLDS[assessmentType];
  
  if (score >= thresholds.EXCELLENT) return 'green';
  if (score >= thresholds.GOOD) return 'blue';
  if (score >= thresholds.AVERAGE) return 'yellow';
  if (score >= thresholds.POOR) return 'orange';
  return 'red';
}

// Date Utilities
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

export function formatDateTime(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
}

export function isDateExpired(date: Date): boolean {
  return date.getTime() < Date.now();
}

// Assessment Utilities
export function calculateOverallScore(assessments: FitnessAssessment[]): number {
  if (assessments.length === 0) return 0;
  
  const total = assessments.reduce((sum, assessment) => sum + assessment.score, 0);
  return Math.round(total / assessments.length);
}

export function getLatestAssessment(assessments: FitnessAssessment[]): FitnessAssessment | null {
  if (assessments.length === 0) return null;
  
  return assessments.reduce((latest, current) => 
    current.assessedAt > latest.assessedAt ? current : latest
  );
}

// File Utilities
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export function getFileExtension(filename: string): string {
  return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
}

// Validation Utilities
export function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// API Utilities
export function createApiResponse<T>(
  success: boolean,
  data?: T,
  error?: string,
  message?: string
) {
  return {
    success,
    data,
    error,
    message,
  };
}

export function createPaginatedResponse<T>(
  items: T[],
  page: number,
  limit: number,
  total: number
) {
  return {
    items,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  };
}