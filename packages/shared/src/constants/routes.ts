export const ROUTES = {
  // Public routes
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  ABOUT: '/about',
  CONTACT: '/contact',

  // Dashboard routes
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  SETTINGS: '/settings',

  // Workout routes
  WORKOUTS: '/workouts',
  WORKOUT_DETAILS: '/workouts/[id]',
  WORKOUT_CREATE: '/workouts/create',
  WORKOUT_EDIT: '/workouts/[id]/edit',
  EXERCISES: '/exercises',

  // Assessment routes
  ASSESSMENTS: '/assessments',
  ASSESSMENT_DETAILS: '/assessments/[id]',
  ASSESSMENT_TAKE: '/assessments/[id]/take',
  ASSESSMENT_RESULTS: '/assessments/[id]/results',

  // Admin routes
  ADMIN: {
    DASHBOARD: '/admin',
    USERS: '/admin/users',
    WORKOUTS: '/admin/workouts',
    ASSESSMENTS: '/admin/assessments',
    REPORTS: '/admin/reports',
    UPLOADS: '/admin/uploads',
    QR_CODES: '/admin/qr-codes',
    EXCEPTIONS: '/admin/exceptions',
    SETTINGS: '/admin/settings',
  },

  // API routes
  API: {
    AUTH: '/api/auth',
    USERS: '/api/users',
    WORKOUTS: '/api/workouts',
    ASSESSMENTS: '/api/assessments',
    FILES: '/api/files',
    QR_CODES: '/api/qr-codes',
    REPORTS: '/api/reports',
  },
} as const;

export const PROTECTED_ROUTES = [
  ROUTES.DASHBOARD,
  ROUTES.PROFILE,
  ROUTES.SETTINGS,
  ROUTES.WORKOUTS,
  ROUTES.ASSESSMENTS,
  ...Object.values(ROUTES.ADMIN),
] as const;

export const PUBLIC_ROUTES = [
  ROUTES.HOME,
  ROUTES.LOGIN,
  ROUTES.REGISTER,
  ROUTES.ABOUT,
  ROUTES.CONTACT,
] as const;