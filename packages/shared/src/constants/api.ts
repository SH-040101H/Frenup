export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const API_VERSION = 'v1';

export const API_ENDPOINTS = {
  // Auth
  AUTH: {
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    REGISTER: '/auth/register',
    VERIFY: '/auth/verify',
  },

  // Users
  USERS: {
    BASE: '/users',
    PROFILE: '/users/profile',
    ME: '/users/me',
  },

  // Workouts
  WORKOUTS: {
    BASE: '/workouts',
    EXERCISES: '/workouts/exercises',
    TEMPLATES: '/workouts/templates',
  },

  // Assessments
  ASSESSMENTS: {
    BASE: '/assessments',
    RESULTS: '/assessments/results',
    TEMPLATES: '/assessments/templates',
  },

  // Files
  FILES: {
    BASE: '/files',
    UPLOAD: '/files/upload',
    DOWNLOAD: '/files/download',
  },

  // QR Codes
  QR_CODES: {
    BASE: '/qr-codes',
    GENERATE: '/qr-codes/generate',
    BULK_GENERATE: '/qr-codes/bulk-generate',
  },

  // Reports
  REPORTS: {
    BASE: '/reports',
    GENERATE: '/reports/generate',
    EXPORT: '/reports/export',
  },
} as const;

export const HTTP_METHODS = {
  GET: 'GET',
  POST: 'POST',
  PUT: 'PUT',
  PATCH: 'PATCH',
  DELETE: 'DELETE',
} as const;

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const;