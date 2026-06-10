/**
 * Toast Service
 * 
 * Centralized toast notification service for user-critical messages.
 * Uses CoreUI toast component for consistent UI.
 */

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  autohide: boolean;
  delay: number;
  timestamp: number;
}

@Injectable({
  providedIn: 'root'
})
export class ToastService {
  private toastsSubject = new BehaviorSubject<ToastMessage[]>([]);
  public toasts$: Observable<ToastMessage[]> = this.toastsSubject.asObservable();

  private idCounter = 0;

  /**
   * Show error toast (user-critical only)
   */
  showError(message: string, title: string = 'Error'): void {
    this.addToast({
      type: 'error',
      title,
      message,
      autohide: false, // Errors require manual dismissal
      delay: 0
    });
  }

  /**
   * Show success toast
   */
  showSuccess(message: string, title: string = 'Éxito'): void {
    this.addToast({
      type: 'success',
      title,
      message,
      autohide: true,
      delay: 3000
    });
  }

  /**
   * Show warning toast
   */
  showWarning(message: string, title: string = 'Advertencia'): void {
    this.addToast({
      type: 'warning',
      title,
      message,
      autohide: true,
      delay: 5000
    });
  }

  /**
   * Show info toast
   */
  showInfo(message: string, title: string = 'Información'): void {
    this.addToast({
      type: 'info',
      title,
      message,
      autohide: true,
      delay: 3000
    });
  }

  /**
   * Remove toast by ID
   */
  remove(id: string): void {
    const current = this.toastsSubject.value;
    this.toastsSubject.next(current.filter(toast => toast.id !== id));
  }

  /**
   * Clear all toasts
   */
  clear(): void {
    this.toastsSubject.next([]);
  }

  private addToast(toast: Omit<ToastMessage, 'id' | 'timestamp'>): void {
    const id = `toast-${++this.idCounter}`;
    const newToast: ToastMessage = {
      ...toast,
      id,
      timestamp: Date.now()
    };

    const current = this.toastsSubject.value;
    this.toastsSubject.next([...current, newToast]);

    // Auto-remove if autohide is enabled
    if (toast.autohide && toast.delay > 0) {
      setTimeout(() => this.remove(id), toast.delay);
    }
  }

  getCurrentToasts(): ToastMessage[] {
    return this.toastsSubject.value;
  }
}
