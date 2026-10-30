// Base API URL: Uses environment variable in production, falls back to localhost:8000 in development
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
