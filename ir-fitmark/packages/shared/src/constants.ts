// API Constants
export const API_ROUTES = {
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    PROFILE: '/auth/profile',
  },
  USERS: {
    BASE: '/users',
    BY_ID: (id: string) => `/users/${id}`,
  },
  ASSESSMENTS: {
    BASE: '/assessments',
    BY_ID: (id: string) => `/assessments/${id}`,
    BY_USER: (userId: string) => `/assessments/user/${userId}`,
    UPLOAD: '/assessments/upload',
  },
  REPORTS: {
    BASE: '/reports',
    BY_ID: (id: string) => `/reports/${id}`,
    BY_USER: (userId: string) => `/reports/user/${userId}`,
    GENERATE: '/reports/generate',
  },
  QR: {
    BASE: '/qr',
    GENERATE: '/qr/generate',
    BULK_GENERATE: '/qr/bulk-generate',
    VERIFY: '/qr/verify',
  },
  ADMIN: {
    DASHBOARD: '/admin/dashboard',
    USERS: '/admin/users',
    REPORTS: '/admin/reports',
    EXCEPTIONS: '/admin/exceptions',
  },
} as const;

// Fitness Assessment Types
export const ASSESSMENT_TYPES = {
  PUSHUP: 'pushup',
  SITUP: 'situp',
  RUNNING: 'running',
  FLEXIBILITY: 'flexibility',
} as const;

export const ASSESSMENT_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
} as const;

// User Roles
export const USER_ROLES = {
  STUDENT: 'student',
  INSTRUCTOR: 'instructor',
  ADMIN: 'admin',
} as const;

// Report Periods
export const REPORT_PERIODS = {
  WEEKLY: 'weekly',
  MONTHLY: 'monthly',
  QUARTERLY: 'quarterly',
} as const;

// File Upload
export const UPLOAD_LIMITS = {
  MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
  ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/webm', 'video/avi'],
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
} as const;

// Scoring Thresholds
export const SCORING_THRESHOLDS = {
  PUSHUP: {
    EXCELLENT: 90,
    GOOD: 75,
    AVERAGE: 60,
    POOR: 40,
  },
  SITUP: {
    EXCELLENT: 90,
    GOOD: 75,
    AVERAGE: 60,
    POOR: 40,
  },
  RUNNING: {
    EXCELLENT: 90,
    GOOD: 75,
    AVERAGE: 60,
    POOR: 40,
  },
  FLEXIBILITY: {
    EXCELLENT: 90,
    GOOD: 75,
    AVERAGE: 60,
    POOR: 40,
  },
} as const;

// Environment
export const ENVIRONMENTS = {
  DEVELOPMENT: 'development',
  TESTING: 'testing',
  STAGING: 'staging',
  PRODUCTION: 'production',
} as const;