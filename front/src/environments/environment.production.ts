/**
 * Environment configuration for PRODUCTION
 * 
 * Backend serves the frontend from the same origin,
 * so API URL is relative.
 * 
 * This file is used when building with: ng build --configuration production
 */
export const environment = {
  production: true,
  
  // Relative API URL - same origin (backend serves frontend)
  apiUrl: 'https://ircaback-639342137715.northamerica-northeast1.run.app/api',
  apiVersion: '1.0.0',
  
  // Admin API key for protected operations (POST/PUT/DELETE)
  // Configure via environment variable if needed
  adminApiKey: '',
  
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
