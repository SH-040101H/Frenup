import { REGEX_PATTERNS, VALIDATION_RULES } from '../constants/validation';

export const validateEmail = (email: string): boolean => {
  return REGEX_PATTERNS.EMAIL.test(email);
};

export const validatePassword = (password: string): boolean => {
  return REGEX_PATTERNS.PASSWORD.test(password);
};

export const validatePhone = (phone: string): boolean => {
  return REGEX_PATTERNS.PHONE.test(phone);
};

export const validateUrl = (url: string): boolean => {
  return REGEX_PATTERNS.URL.test(url);
};

export const validateUuid = (uuid: string): boolean => {
  return REGEX_PATTERNS.UUID.test(uuid);
};

export const validateFileSize = (size: number): boolean => {
  return size <= VALIDATION_RULES.FILE.MAX_SIZE;
};

export const validateFileType = (mimeType: string): boolean => {
  const allowedTypes = [
    ...VALIDATION_RULES.FILE.ALLOWED_IMAGE_TYPES,
    ...VALIDATION_RULES.FILE.ALLOWED_DOCUMENT_TYPES,
    ...VALIDATION_RULES.FILE.ALLOWED_VIDEO_TYPES,
  ];
  return allowedTypes.includes(mimeType);
};

export const validateImageType = (mimeType: string): boolean => {
  return VALIDATION_RULES.FILE.ALLOWED_IMAGE_TYPES.includes(mimeType);
};

export const validateDocumentType = (mimeType: string): boolean => {
  return VALIDATION_RULES.FILE.ALLOWED_DOCUMENT_TYPES.includes(mimeType);
};

export const validateVideoType = (mimeType: string): boolean => {
  return VALIDATION_RULES.FILE.ALLOWED_VIDEO_TYPES.includes(mimeType);
};

export const validateStringLength = (
  value: string,
  minLength: number,
  maxLength: number
): boolean => {
  return value.length >= minLength && value.length <= maxLength;
};

export const validateNumberRange = (
  value: number,
  min: number,
  max: number
): boolean => {
  return value >= min && value <= max;
};

export const validatePagination = (page: number, limit: number): boolean => {
  return (
    page >= VALIDATION_RULES.PAGINATION.MIN_PAGE &&
    limit >= VALIDATION_RULES.PAGINATION.MIN_LIMIT &&
    limit <= VALIDATION_RULES.PAGINATION.MAX_LIMIT
  );
};

export const validateSearchQuery = (query: string): boolean => {
  return (
    query.length >= VALIDATION_RULES.SEARCH.MIN_LENGTH &&
    query.length <= VALIDATION_RULES.SEARCH.MAX_LENGTH
  );
};

export const sanitizeString = (value: string): string => {
  return value.trim().replace(/\s+/g, ' ');
};

export const sanitizeEmail = (email: string): string => {
  return email.trim().toLowerCase();
};

export const generateValidationError = (
  field: string,
  message: string
): { field: string; message: string } => {
  return { field, message };
};