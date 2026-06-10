/**
 * Rate Limit Service
 * 
 * Tracks rate limit information from API responses and provides
 * observable streams for UI components.
 */

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface RateLimitInfo {
  limit: number;
  remaining: number;
  reset?: number;
  endpoint: string;
  timestamp?: number;
}

@Injectable({
  providedIn: 'root'
})
export class RateLimitService {
  private rateLimitSubject = new BehaviorSubject<RateLimitInfo | null>(null);
  public rateLimit$: Observable<RateLimitInfo | null> = this.rateLimitSubject.asObservable();

  updateRateLimit(info: RateLimitInfo): void {
    this.rateLimitSubject.next({
      ...info,
      timestamp: Date.now()
    });
  }

  getCurrentRateLimit(): RateLimitInfo | null {
    return this.rateLimitSubject.value;
  }

  isApproachingLimit(threshold: number = 20): boolean {
    const current = this.getCurrentRateLimit();
    if (!current) return false;

    const percentage = (current.remaining / current.limit) * 100;
    return percentage < threshold && percentage > 0;
  }

  getRemainingPercentage(): number {
    const current = this.getCurrentRateLimit();
    if (!current) return 100;

    return (current.remaining / current.limit) * 100;
  }
}
