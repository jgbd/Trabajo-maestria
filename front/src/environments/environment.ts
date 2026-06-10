/**
 * Environment configuration for development
 * 
 * Matches backend Phase 1 implementation:
 * - Public API (no authentication for GET requests)
 * - Rate limiting per endpoint
 * - Admin API key for write operations (future use)
 */
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  apiVersion: '1.0.0',
  
  // Admin API key for protected operations (POST/PUT/DELETE)
  // Only needed when implementing admin features in future phases
  adminApiKey: '', // Leave empty for public read-only access
  
  // Rate limit expectations (informational - limits enforced by backend)
  rateLimits: {
    estadisticas: '30 per minute',
    resultados: '10 per minute', 
    municipios: '100 per hour'
  },

  // Feature flags
  features: {
    showRateLimitInfo: true,
    enableToastNotifications: true,
    enableIRCAColorCoding: true
  }
};
