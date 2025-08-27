import { z } from 'zod';

export const PaginationSchema = z.object({
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(20),
  total: z.number().min(0),
  totalPages: z.number().min(0),
});

export type Pagination = z.infer<typeof PaginationSchema>;

export const ApiResponseSchema = z.object({
  success: z.boolean(),
  message: z.string().optional(),
  data: z.any().optional(),
  error: z.string().optional(),
  pagination: PaginationSchema.optional(),
});

export type ApiResponse<T = any> = {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
  pagination?: Pagination;
};

export const SortOrderSchema = z.enum(['asc', 'desc']);
export type SortOrder = z.infer<typeof SortOrderSchema>;

export const FilterSchema = z.object({
  field: z.string(),
  operator: z.enum(['eq', 'ne', 'gt', 'gte', 'lt', 'lte', 'in', 'nin', 'like']),
  value: z.any(),
});

export type Filter = z.infer<typeof FilterSchema>;

export const SortSchema = z.object({
  field: z.string(),
  order: SortOrderSchema,
});

export type Sort = z.infer<typeof SortSchema>;

export const QueryParamsSchema = z.object({
  page: z.number().min(1).optional(),
  limit: z.number().min(1).max(100).optional(),
  sort: z.array(SortSchema).optional(),
  filter: z.array(FilterSchema).optional(),
  search: z.string().optional(),
});

export type QueryParams = z.infer<typeof QueryParamsSchema>;

export const FileUploadSchema = z.object({
  id: z.string().uuid(),
  filename: z.string(),
  originalName: z.string(),
  mimeType: z.string(),
  size: z.number().positive(),
  url: z.string().url(),
  uploadedBy: z.string().uuid(),
  uploadedAt: z.date(),
});

export type FileUpload = z.infer<typeof FileUploadSchema>;

export const QRCodeSchema = z.object({
  id: z.string().uuid(),
  code: z.string(),
  type: z.enum(['workout', 'assessment', 'profile']),
  targetId: z.string().uuid(),
  expiresAt: z.date().optional(),
  isActive: z.boolean(),
  createdAt: z.date(),
});

export type QRCode = z.infer<typeof QRCodeSchema>;