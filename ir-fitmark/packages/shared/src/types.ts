import { z } from 'zod';

// User & Authentication
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string(),
  role: z.enum(['student', 'instructor', 'admin']),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type User = z.infer<typeof UserSchema>;

// Fitness Assessment
export const FitnessAssessmentSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  assessmentType: z.enum(['pushup', 'situp', 'running', 'flexibility']),
  score: z.number().min(0).max(100),
  videoUrl: z.string().url().optional(),
  assessedAt: z.date(),
  aiConfidence: z.number().min(0).max(1),
  status: z.enum(['pending', 'processing', 'completed', 'failed']),
});

export type FitnessAssessment = z.infer<typeof FitnessAssessmentSchema>;

// Reports
export const ReportSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  period: z.enum(['weekly', 'monthly', 'quarterly']),
  generatedAt: z.date(),
  data: z.record(z.any()),
  pdfUrl: z.string().url().optional(),
});

export type Report = z.infer<typeof ReportSchema>;

// QR Code
export const QRCodeSchema = z.object({
  id: z.string().uuid(),
  code: z.string(),
  userId: z.string().uuid(),
  expiresAt: z.date(),
  usageCount: z.number().default(0),
  maxUsage: z.number().default(1),
  isActive: z.boolean().default(true),
});

export type QRCode = z.infer<typeof QRCodeSchema>;

// API Response Wrapper
export const ApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    data: dataSchema.optional(),
    error: z.string().optional(),
    message: z.string().optional(),
  });

export type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
};

// Pagination
export const PaginationSchema = z.object({
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(10),
  total: z.number().min(0),
  pages: z.number().min(0),
});

export type Pagination = z.infer<typeof PaginationSchema>;

export const PaginatedResponseSchema = <T extends z.ZodTypeAny>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    pagination: PaginationSchema,
  });

export type PaginatedResponse<T> = {
  items: T[];
  pagination: Pagination;
};