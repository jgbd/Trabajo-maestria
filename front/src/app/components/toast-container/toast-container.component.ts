/**
 * Toast Container Component
 * 
 * Displays toast notifications for user-critical messages.
 * Positioned at top-right corner of the application.
 */
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, ToastMessage } from '../../services/toast.service';
import { ToastModule } from '@coreui/angular';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule, ToastModule],
  template: `
    <c-toaster placement="top-end" class="p-3" position="fixed">
      <c-toast
        *ngFor="let toast of toasts"
        [visible]="true"
        [autohide]="toast.autohide"
        [delay]="toast.delay"
        (visibleChange)="onToastClose(toast.id, $event)"
        [color]="getToastColor(toast.type)"
      >
        <c-toast-header [closeButton]="true">
          <span class="me-auto fw-bold">{{ toast.title }}</span>
        </c-toast-header>
        <c-toast-body>
          {{ toast.message }}
        </c-toast-body>
      </c-toast>
    </c-toaster>
  `,
  styles: [`
    :host {
      position: fixed;
      top: 0;
      right: 0;
      z-index: 9999;
    }
  `]
})
export class ToastContainerComponent implements OnInit {
  toasts: ToastMessage[] = [];

  constructor(private toastService: ToastService) {}

  ngOnInit(): void {
    this.toastService.toasts$.subscribe((toasts) => {
      this.toasts = toasts;
    });
  }

  onToastClose(id: string, visible: boolean): void {
    if (!visible) {
      this.toastService.remove(id);
    }
  }

  getToastColor(type: string): string {
    const colorMap: Record<string, string> = {
      success: 'success',
      error: 'danger',
      warning: 'warning',
      info: 'info'
    };
    return colorMap[type] || 'info';
  }
}
