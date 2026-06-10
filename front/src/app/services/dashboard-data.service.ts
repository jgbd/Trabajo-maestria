/**
 * Dashboard Data Service
 * 
 * Service for fetching water quality data from the IRCA Public API.
 * Integrated with Phase 1 backend security features:
 * - Rate limiting
 * - Error handling
 * - IRCA risk classification
 */
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, retry } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { PaginatedResponse, PaginationParams } from '../models/pagination.model';

export interface MunicipioData {
  municipio: string;
  lat: number;
  lng: number;
  resultados: Array<{
    anio: number;
    irca: number;
    estado: string;
  }>;
}

export interface Municipio {
  Codigo: number;
  Nombre: string;
}

export interface ResultadoDetallado {
  resultado_Color_Aparente?: number;
  diagnostico_Color_Aparente?: string;
  resultado_Turbiedad?: number;
  diagnostico_Turbiedad?: string;
  resultado_pH?: number;
  diagnostico_pH?: string;
  resultado_Cloro_Residual_Libre?: number;
  diagnostico_Cloro_Residual_Libre?: string;
  resultado_Alcalinidad_Total?: number;
  diagnostico_Alcalinidad_Total?: string;
  resultado_Calcio?: number;
  diagnostico_Calcio?: string;
  resultado_Fosfatos?: number;
  diagnostico_Fosfatos?: string;
  resultado_Manganeso?: number;
  diagnostico_Manganeso?: string;
  resultado_Molibdeno?: number;
  diagnostico_Molibdeno?: string;
  resultado_Magnesio?: number;
  diagnostico_Magnesio?: string;
  resultado_Zinc?: number;
  diagnostico_Zinc?: string;
  resultado_Dureza_Total?: number;
  diagnostico_Dureza_Total?: string;
  resultado_Sulfatos?: number;
  diagnostico_Sulfatos?: string;
  resultado_Hierro_Total?: number;
  diagnostico_Hierro_Total?: string;
  resultado_Cloruros?: number;
  diagnostico_Cloruros?: string;
  resultado_Nitratos?: number;
  diagnostico_Nitratos?: string;
  resultado_Nitritos?: number;
  diagnostico_Nitritos?: string;
  resultado_Aluminio?: number;
  diagnostico_Aluminio?: string;
  resultado_Fluoruros?: number;
  diagnostico_Fluoruros?: string;
  resultado_COT?: number;
  diagnostico_COT?: string;
  resultado_Coliformes_Totales?: string;
  diagnostico_Coliformes_Totales?: string;
  resultado_Escherichia_coli?: string;
  diagnostico_Escherichia_coli?: string;
  IRCA?: number;
  nivel_Riesgo?: string;
  fecha_Analisis?: string;
  municipio?: string;
  nombre_Punto?: string;
}

@Injectable({
  providedIn: 'root',
})
export class DashboardDataService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /**
   * Get dashboard IRCA statistics data
   * 
   * Rate limit: 30 requests/minute (configured in backend)
   * 
   * @param anioInicio Start year (default: 2020)
   * @param anioFin End year (default: 2024)
   * @param codigo_municipio Optional municipality filter
   */
  getDashboardData(
    anioInicio?: number, 
    anioFin?: number, 
    codigo_municipio?: number
  ): Observable<MunicipioData[]> {
    let params = new HttpParams();
    
    if (anioInicio !== undefined) {
      params = params.set('anioInicio', anioInicio.toString());
    }
    if (anioFin !== undefined) {
      params = params.set('anioFin', anioFin.toString());
    }
    if (codigo_municipio !== undefined) {
      params = params.set('codigo_municipio', codigo_municipio.toString());
    }

    return this.http.get<MunicipioData[]>(`${this.apiUrl}/estadisticas`, { params }).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      catchError((error) => {
        console.error('Error fetching dashboard data:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get list of all municipalities
   * 
   * Rate limit: 100 requests/hour (configured in backend)
   */
  getMunicipios(): Observable<Municipio[]> {
    return this.http.get<Municipio[]>(`${this.apiUrl}/municipios`).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      map((municipios) => {
        // Sort alphabetically by name
        return municipios.sort((a, b) => a.Nombre.localeCompare(b.Nombre));
      }),
      catchError((error) => {
        console.error('Error fetching municipios:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get detailed results with pagination
   * 
   * Rate limit: 10 requests/minute (configured in backend)
   * 
   * @param pagination Pagination parameters (page, page_size)
   */
  getResultadosDetallados(
    pagination: PaginationParams
  ): Observable<PaginatedResponse<ResultadoDetallado>> {
    let params = new HttpParams()
      .set('page', pagination.page.toString())
      .set('page_size', pagination.page_size.toString());

    return this.http.get<PaginatedResponse<ResultadoDetallado>>(
      `${this.apiUrl}/estadisticas/resultados`,
      { params }
    ).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      catchError((error) => {
        console.error('Error fetching detailed results:', error);
        return throwError(() => error);
      })
    );
  }
}

