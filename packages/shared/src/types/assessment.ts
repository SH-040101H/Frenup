import { z } from 'zod';

export const AssessmentTypeSchema = z.enum(['fitness', 'nutrition', 'mental_health', 'injury_risk']);
export type AssessmentType = z.infer<typeof AssessmentTypeSchema>;

export const AssessmentStatusSchema = z.enum(['pending', 'in_progress', 'completed', 'failed']);
export type AssessmentStatus = z.infer<typeof AssessmentStatusSchema>;

export const AssessmentResultSchema = z.object({
  id: z.string().uuid(),
  assessmentId: z.string().uuid(),
  score: z.number().min(0).max(100),
  category: z.string(),
  details: z.record(z.any()),
  recommendations: z.array(z.string()),
  aiAnalysis: z.string().optional(),
  createdAt: z.date(),
});

export type AssessmentResult = z.infer<typeof AssessmentResultSchema>;

export const AssessmentSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  type: AssessmentTypeSchema,
  status: AssessmentStatusSchema,
  title: z.string().min(1).max(200),
  description: z.string().optional(),
  questions: z.array(z.record(z.any())),
  answers: z.array(z.record(z.any())).optional(),
  result: AssessmentResultSchema.optional(),
  scheduledDate: z.date().optional(),
  completedDate: z.date().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type Assessment = z.infer<typeof AssessmentSchema>;

export const CreateAssessmentSchema = AssessmentSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

export type CreateAssessment = z.infer<typeof CreateAssessmentSchema>;

export const UpdateAssessmentSchema = CreateAssessmentSchema.partial();
export type UpdateAssessment = z.infer<typeof UpdateAssessmentSchema>;