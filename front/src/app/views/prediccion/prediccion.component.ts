/**
 * Predicción IRCA Component
 * 
 * Form-based component for predicting IRCA values using water quality parameters.
 * Uses the trained Random Forest model via the prediction API.
 */

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import {
  CardComponent,
  CardBodyComponent,
  CardHeaderComponent,
  ColComponent,
  RowComponent,
  FormModule,
  ButtonDirective,
  SpinnerComponent,
  AlertComponent,
  BadgeComponent,
  ProgressBarComponent,
  ProgressComponent,
} from '@coreui/angular';
import { PredictionService, PredictionRequest, ModelInfo } from '../../services/prediction.service';
import { IRCARiskThresholds } from '../../services/irca-constants';

@Component({
  selector: 'app-prediccion',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    CardComponent,
    CardBodyComponent,
    CardHeaderComponent,
    ColComponent,
    RowComponent,
    FormModule,
    ButtonDirective,
    SpinnerComponent,
    AlertComponent,
    BadgeComponent,
    ProgressBarComponent,
    ProgressComponent,
  ],
  templateUrl: './prediccion.component.html',
  styleUrls: ['./prediccion.component.scss'],
})
export class PrediccionComponent implements OnInit {
  private readonly predictionService = inject(PredictionService);
  private readonly fb = inject(FormBuilder);

  predictionForm!: FormGroup;
  loading = false;
  predictionResult: any = null;
  modelInfo: ModelInfo | null = null;
  error: string | null = null;
  
  // For template access
  IRCARiskThresholds = IRCARiskThresholds;

  ngOnInit(): void {
    this.initForm();
    this.loadModelInfo();
  }

  initForm(): void {
    this.predictionForm = this.fb.group({
      color_aparente: [5.0, [Validators.required, Validators.min(0), Validators.max(1000)]],
      turbiedad: [2.5, [Validators.required, Validators.min(0), Validators.max(1000)]],
      ph: [7.2, [Validators.required, Validators.min(0), Validators.max(14)]],
      cloro_residual_libre: [0.8, [Validators.required, Validators.min(0), Validators.max(100)]],
      cloruros: [15.0, [Validators.required, Validators.min(0), Validators.max(1000)]],
      nitritos: [0.01, [Validators.required, Validators.min(0), Validators.max(100)]],
      coliformes_totales: [0.0, [Validators.required, Validators.min(0), Validators.max(100000)]],
      e_coli: [0.0, [Validators.required, Validators.min(0), Validators.max(100000)]],
    });
  }

  loadModelInfo(): void {
    this.predictionService.getModelInfo().subscribe({
      next: (info) => {
        this.modelInfo = info;
      },
      error: (error) => {
        console.error('Error loading model info:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.predictionForm.invalid) {
      this.error = 'Por favor, complete todos los campos correctamente.';
      return;
    }

    this.loading = true;
    this.error = null;
    this.predictionResult = null;

    const formData: PredictionRequest = this.predictionForm.value;

    this.predictionService.predictIRCA(formData).subscribe({
      next: (result) => {
        this.predictionResult = result;
        this.loading = false;
      },
      error: (error) => {
        console.error('Prediction error:', error);
        this.error = 'Error al realizar la predicción. Por favor, intente nuevamente.';
        this.loading = false;
      },
    });
  }

  onReset(): void {
    this.predictionForm.reset();
    this.predictionResult = null;
    this.error = null;
    this.initForm(); // Reset to default values
  }

  getRiskBadgeColor(nivel: string): string {
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

  getFieldError(fieldName: string): string | null {
    const field = this.predictionForm.get(fieldName);
    if (field?.errors && field.touched) {
      if (field.errors['required']) {
        return 'Este campo es requerido';
      }
      if (field.errors['min']) {
        return `Valor mínimo: ${field.errors['min'].min}`;
      }
      if (field.errors['max']) {
        return `Valor máximo: ${field.errors['max'].max}`;
      }
    }
    return null;
  }
}
