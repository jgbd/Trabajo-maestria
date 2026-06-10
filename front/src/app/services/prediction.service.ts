/**
 * Prediction Service
 * 
 * Service for calling the IRCA prediction API endpoint.
 * Uses the trained Random Forest model to predict IRCA values.
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface PredictionRequest {
  color_aparente: number;
  turbiedad: number;
  ph: number;
  cloro_residual_libre: number;
  cloruros: number;
  nitritos: number;
  coliformes_totales: number;
  e_coli: number;
}

export interface PredictionResponse {
  irca_predicted: number;
  nivel_riesgo: string;
  confidence: number;
}

export interface BatchPredictionRequest {
  samples: PredictionRequest[];
}

export interface BatchPredictionResponse {
  predictions: PredictionResponse[];
  total_samples: number;
}

export interface ModelInfo {
  model_class: string;
  parameters: Record<string, any>;
  feature_names: string[];
  metrics: Record<string, number>;
  n_features: number;
}

@Injectable({
  providedIn: 'root',
})
export class PredictionService {
  private apiUrl = `${environment.apiUrl}/prediccion`;

  constructor(private http: HttpClient) {}

  /**
   * Predict IRCA value for a single water quality sample
   * 
   * @param data Water quality parameters
   * @returns Observable<PredictionResponse>
   */
  predictIRCA(data: PredictionRequest): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>(
      `${this.apiUrl}/predict`,
      data
    ).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      catchError((error) => {
        console.error('Error predicting IRCA:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Predict IRCA values for multiple samples at once
   * 
   * @param data Batch prediction request with multiple samples
   * @returns Observable<BatchPredictionResponse>
   */
  predictBatch(data: BatchPredictionRequest): Observable<BatchPredictionResponse> {
    return this.http.post<BatchPredictionResponse>(
      `${this.apiUrl}/batch`,
      data
    ).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      catchError((error) => {
        console.error('Error in batch prediction:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Get information about the loaded prediction model
   * 
   * @returns Observable<ModelInfo>
   */
  getModelInfo(): Observable<ModelInfo> {
    return this.http.get<ModelInfo>(`${this.apiUrl}/model-info`).pipe(
      retry({
        count: 2,
        delay: 1000,
        resetOnSuccess: true
      }),
      catchError((error) => {
        console.error('Error fetching model info:', error);
        return throwError(() => error);
      })
    );
  }

  /**
   * Health check for prediction service
   * 
   * @returns Observable<any>
   */
  healthCheck(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`).pipe(
      catchError((error) => {
        console.error('Prediction service health check failed:', error);
        return throwError(() => error);
      })
    );
  }
}
