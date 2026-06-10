/**
 * Rate Limit Interceptor
 * 
 * Captures rate limit headers from backend responses and provides
 * warnings when approaching limits.
 */

import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { tap } from 'rxjs';
import { RateLimitService } from '../services/rate-limit.service';

export const rateLimitInterceptor: HttpInterceptorFn = (req, next) => {
  const rateLimitService = inject(RateLimitService);

  return next(req).pipe(
    tap((event) => {
      if (event instanceof HttpResponse) {
        const headers = event.headers;
        
        // Extract rate limit headers from response
        const limit = headers.get('X-RateLimit-Limit');
        const remaining = headers.get('X-RateLimit-Remaining');
        const reset = headers.get('X-RateLimit-Reset');

        if (limit && remaining) {
          rateLimitService.updateRateLimit({
            limit: parseInt(limit, 10),
            remaining: parseInt(remaining, 10),
            reset: reset ? parseInt(reset, 10) : undefined,
            endpoint: req.url
          });

          // Warn if approaching limit (< 20% remaining)
          const remainingPercent = (parseInt(remaining, 10) / parseInt(limit, 10)) * 100;
          if (remainingPercent < 20 && remainingPercent > 0) {
            console.warn(
              `⚠️ Rate limit warning: ${remaining}/${limit} requests remaining for ${req.url}`
            );
          }
        }
      }
    })
  );
};
