import { z } from 'zod';

export const WorkoutTypeSchema = z.enum(['strength', 'cardio', 'flexibility', 'sports']);
export type WorkoutType = z.infer<typeof WorkoutTypeSchema>;

export const WorkoutStatusSchema = z.enum(['planned', 'in_progress', 'completed', 'cancelled']);
export type WorkoutStatus = z.infer<typeof WorkoutStatusSchema>;

export const ExerciseSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  category: z.string().min(1).max(50),
  muscleGroups: z.array(z.string()),
  equipment: z.array(z.string()).optional(),
  instructions: z.string().optional(),
  videoUrl: z.string().url().optional(),
});

export type Exercise = z.infer<typeof ExerciseSchema>;

export const SetSchema = z.object({
  id: z.string().uuid(),
  exerciseId: z.string().uuid(),
  reps: z.number().positive().optional(),
  weight: z.number().positive().optional(), // in kg
  duration: z.number().positive().optional(), // in seconds
  distance: z.number().positive().optional(), // in meters
  restTime: z.number().positive().optional(), // in seconds
  notes: z.string().optional(),
});

export type Set = z.infer<typeof SetSchema>;

export const WorkoutSchema = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  name: z.string().min(1).max(100),
  description: z.string().optional(),
  type: WorkoutTypeSchema,
  status: WorkoutStatusSchema,
  scheduledDate: z.date(),
  completedDate: z.date().optional(),
  duration: z.number().positive().optional(), // in minutes
  sets: z.array(SetSchema),
  notes: z.string().optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type Workout = z.infer<typeof WorkoutSchema>;

export const CreateWorkoutSchema = WorkoutSchema.omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

export type CreateWorkout = z.infer<typeof CreateWorkoutSchema>;

export const UpdateWorkoutSchema = CreateWorkoutSchema.partial();
export type UpdateWorkout = z.infer<typeof UpdateWorkoutSchema>;