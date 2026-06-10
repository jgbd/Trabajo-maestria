/**
 * Error Handling Interceptor
 * 
 * Centralized error handling for HTTP requests.
 * Handles rate limiting (429), server errors (5xx), and client errors (4xx).
 */

import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { ToastService } from '../services/toast.service';

export const errorHandlingInterceptor: HttpInterceptorFn = (req, next) => {
  const toastService = inject(ToastService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'Ha ocurrido un error inesperado';
      let showToast = true;

      if (error.error instanceof ErrorEvent) {
        // Client-side error
        errorMessage = `Error: ${error.error.message}`;
        console.error('Client-side error:', error.error.message);
      } else {
        // Server-side error
        switch (error.status) {
          case 429:
            // Rate limit exceeded
            errorMessage = 'Límite de solicitudes excedido. Por favor, espera un momento e intenta nuevamente.';
            const retryAfter = error.headers.get('Retry-After');
            if (retryAfter) {
              errorMessage += ` Intenta nuevamente en ${retryAfter} segundos.`;
            }
            console.warn('Rate limit exceeded:', error);
            break;

          case 404:
            errorMessage = 'Recurso no encontrado';
            showToast = false; // Don't show toast for 404s (might be intentional)
            console.warn('Resource not found:', req.url);
            break;

          case 500:
          case 502:
          case 503:
          case 504:
            errorMessage = 'Error del servidor. Por favor, intenta más tarde.';
            console.error('Server error:', error);
            break;

          case 0:
            // Network error (no response from server)
            errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
            console.error('Network error - server not reachable');
            break;

          default:
            if (error.error?.error) {
              errorMessage = error.error.error;
            } else if (error.error?.message) {
              errorMessage = error.error.message;
            }
            console.error('HTTP error:', error);
        }
      }

      // Show toast notification for critical errors only
      if (showToast && (error.status === 429 || error.status >= 500 || error.status === 0)) {
        toastService.showError(errorMessage);
      }

      return throwError(() => ({
        status: error.status,
        message: errorMessage,
        originalError: error
      }));
    })
  );
};
