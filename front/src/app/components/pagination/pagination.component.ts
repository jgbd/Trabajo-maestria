/**
 * Reusable Pagination Component
 * 
 * Displays pagination controls for navigating through paginated data.
 * Uses CoreUI components for consistent styling.
 */

import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationMeta, calculatePageNumbers } from '../../models/pagination.model';
import { 
  PaginationModule,
  PageLinkDirective,
  PageItemDirective 
} from '@coreui/angular';

@Component({
  selector: 'app-pagination',
  standalone: true,
  imports: [CommonModule, PaginationModule, PageLinkDirective, PageItemDirective],
  template: `
    <nav *ngIf="meta && meta.total_pages > 1" aria-label="Page navigation">
      <c-pagination aria-label="Page navigation" class="justify-content-center">
        <!-- Previous button -->
        <li
          cPageItem
          [disabled]="!meta.has_previous"
          (click)="onPageChange(meta.page - 1)"
          [attr.aria-label]="'Previous'"
        >
          <a cPageLink>
            <span aria-hidden="true">«</span>
          </a>
        </li>

        <!-- First page if not visible -->
        <li
          cPageItem
          *ngIf="pageNumbers[0] > 1"
          (click)="onPageChange(1)"
        >
          <a cPageLink>1</a>
        </li>
        
        <li cPageItem *ngIf="pageNumbers[0] > 2" [disabled]="true">
          <a cPageLink>...</a>
        </li>

        <!-- Page numbers -->
        <li
          cPageItem
          *ngFor="let pageNum of pageNumbers"
          [active]="pageNum === meta.page"
          (click)="onPageChange(pageNum)"
        >
          <a cPageLink>{{ pageNum }}</a>
        </li>

        <!-- Last page if not visible -->
        <li
          cPageItem
          *ngIf="pageNumbers[pageNumbers.length - 1] < meta.total_pages - 1"
          [disabled]="true"
        >
          <a cPageLink>...</a>
        </li>
        
        <li
          cPageItem
          *ngIf="pageNumbers[pageNumbers.length - 1] < meta.total_pages"
          (click)="onPageChange(meta.total_pages)"
        >
          <a cPageLink>{{ meta.total_pages }}</a>
        </li>

        <!-- Next button -->
        <li
          cPageItem
          [disabled]="!meta.has_next"
          (click)="onPageChange(meta.page + 1)"
          [attr.aria-label]="'Next'"
        >
          <a cPageLink>
            <span aria-hidden="true">»</span>
          </a>
        </li>
      </c-pagination>

      <!-- Page info -->
      <div class="text-center text-muted mt-2" *ngIf="showInfo">
        <small>
          Mostrando 
          {{ ((meta.page - 1) * meta.page_size) + 1 }} - 
          {{ Math.min(meta.page * meta.page_size, meta.total_items) }} 
          de {{ meta.total_items }} registros
        </small>
      </div>
    </nav>
  `,
  styles: [`
    li[cPageItem]:not([disabled]) {
      cursor: pointer;
    }
    
    li[cPageItem][disabled] {
      cursor: not-allowed;
    }
  `]
})
export class PaginationComponent implements OnChanges {
  @Input() meta!: PaginationMeta;
  @Input() maxVisible: number = 5;
  @Input() showInfo: boolean = true;
  @Output() pageChange = new EventEmitter<number>();

  pageNumbers: number[] = [];
  Math = Math; // For template access

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['meta'] && this.meta) {
      this.pageNumbers = calculatePageNumbers(
        this.meta.page,
        this.meta.total_pages,
        this.maxVisible
      );
    }
  }

  onPageChange(page: number): void {
    if (page >= 1 && page <= this.meta.total_pages && page !== this.meta.page) {
      this.pageChange.emit(page);
    }
  }
}
