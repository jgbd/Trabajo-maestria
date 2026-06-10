/**
 * Detailed Results Component
 * 
 * Displays paginated detailed water quality test results.
 * Uses the pagination component for navigation.
 */
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  CardComponent,
  CardBodyComponent,
  CardHeaderComponent,
  ColComponent,
  RowComponent,
  TableDirective,
  SpinnerComponent,
  AlertComponent,
  BadgeComponent,
} from '@coreui/angular';
import { DashboardDataService, ResultadoDetallado } from '../../services/dashboard-data.service';
import { PaginationComponent } from '../../components/pagination/pagination.component';
import { PaginationMeta, createDefaultPagination } from '../../models/pagination.model';
import { IRCARiskThresholds } from '../../services/irca-constants';

@Component({
  selector: 'app-resultados',
  standalone: true,
  imports: [
    CommonModule,
    CardComponent,
    CardBodyComponent,
    CardHeaderComponent,
    ColComponent,
    RowComponent,
    TableDirective,
    SpinnerComponent,
    AlertComponent,
    BadgeComponent,
    PaginationComponent,
  ],
  templateUrl: './resultados.component.html',
  styleUrls: ['./resultados.component.scss'],
})
export class ResultadosComponent implements OnInit {
  private readonly dataService = inject(DashboardDataService);

  resultados: ResultadoDetallado[] = [];
  paginationMeta?: PaginationMeta;
  loading = false;
  error: string | null = null;
  
  // For template access
  IRCARiskThresholds = IRCARiskThresholds;

  ngOnInit(): void {
    this.loadPage(1);
  }

  loadPage(page: number): void {
    this.loading = true;
    this.error = null;

    const pagination = createDefaultPagination(page, 50);

    this.dataService.getResultadosDetallados(pagination).subscribe({
      next: (response) => {
        this.resultados = response.items;
        this.paginationMeta = response.meta;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading results:', error);
        this.error = 'Error al cargar los resultados. Por favor, intente nuevamente.';
        this.loading = false;
      },
    });
  }

  onPageChange(page: number): void {
    this.loadPage(page);
    // Scroll to top of results
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  getRiskBadgeColor(nivel: string | undefined): string {
    if (!nivel) return 'secondary';
    
    switch (nivel.toUpperCase()) {
      case 'SIN RIESGO':
        return 'success';
      case 'BAJO':
        return 'info';
      case 'MEDIO':
        return 'warning';
      case 'ALTO':
        return 'danger';
      case 'INVIABLE':
        return 'dark';
      default:
        return 'secondary';
    }
  }

  formatValue(value: number | string | undefined): string {
    if (value === undefined || value === null) return '-';
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return value;
  }

  formatDate(date: string | undefined): string {
    if (!date) return '-';
    try {
      return new Date(date).toLocaleDateString('es-CO');
    } catch {
      return date;
    }
  }
}
