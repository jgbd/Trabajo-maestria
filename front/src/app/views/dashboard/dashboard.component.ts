import { CommonModule, NgStyle } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import {
  ChartOptions,
  ChartData,
  ChartType,
  TooltipLabelStyle,
} from 'chart.js';
import {
  ButtonDirective,
  CardBodyComponent,
  CardComponent,
  CardFooterComponent,
  ColComponent,
  RowComponent,
  TextColorDirective,
} from '@coreui/angular';
import { ChartjsComponent } from '@coreui/angular-chartjs';

import { DashboardDataService, MunicipioData } from '../../services/dashboard-data.service';
import { IRCARiskThresholds } from '../../services/irca-constants';
import { RateLimitService } from '../../services/rate-limit.service';
import * as L from 'leaflet';
import 'leaflet.heat';

interface municipio {
  Codigo: number;
  Nombre: string;
}

@Component({
  templateUrl: 'dashboard.component.html',
  styleUrls: ['dashboard.component.scss'],
  imports: [
    CommonModule,
    TextColorDirective,
    CardComponent,
    CardBodyComponent,
    CardFooterComponent,
    RowComponent,
    ColComponent,
    ButtonDirective,
    ReactiveFormsModule,
    ChartjsComponent,
    NgStyle,
  ],
  providers: [DashboardDataService],
})
export class DashboardComponent implements OnInit {
  readonly #dashboardDataService: DashboardDataService =
    inject(DashboardDataService);
  readonly #rateLimitService: RateLimitService = inject(RateLimitService);
  
  chartData!: ChartData;
  chartOptions!: ChartOptions;
  chartType: ChartType = 'line';
  form: FormGroup;
  municipios: municipio[] = [];
  datasource: any[] = [];
  anios: any[] = [];
  Math: any = Math; // Para usar Math en la plantilla
  IRCARiskThresholds = IRCARiskThresholds; // For template access

  currentPage: number = 1; // Página actual
  itemsPerPage: number = 5; // Cantidad de filas por página
  paginatedData: any[] = []; // Datos filtrados para la página actual
  
  // Rate limit display
  rateLimitInfo$ = this.#rateLimitService.rateLimit$;

  private mapa!: L.Map;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      anioInicio: [2020, Validators.required],
      anioFin: [2024, Validators.required],
      municipio: [null, Validators.required],
    });
  }

  ngOnInit(): void {
    // Load dashboard data with error handling (handled by interceptor)
    this.#dashboardDataService.getDashboardData().subscribe({
      next: (data: MunicipioData[]) => {
        if (data && data.length > 0) {
          this.setupChartData(data);
          this.setupChartOptions();
          this.setupTableData(data);
          this.iniciarMapa(data);
        }
      },
      error: (error) => {
        console.error('Failed to load dashboard data:', error);
        // Error toast will be shown by interceptor
      }
    });

    // Load municipalities list
    this.#dashboardDataService
      .getMunicipios()
      .subscribe({
        next: (data: municipio[]) => {
          this.municipios = data;
          if (data.length > 0) {
            this.form.patchValue({ municipio: data[0].Codigo });
          }
        },
        error: (error) => {
          console.error('Failed to load municipalities:', error);
          // Error toast will be shown by interceptor
        }
      });
  }

  setupChartData(municipios: any) {
    // Extrae los años (asumiendo que son iguales para todos los municipios)
    const labels = municipios[0].resultados.map((resultado: any) =>
      resultado.anio.toString()
    );

    // Crea un dataset por cada municipio
    // Use IRCA risk colors based on average IRCA value
    const datasets = municipios.map((municipio: any) => {
      const avgIRCA = municipio.resultados.reduce((sum: number, r: any) => sum + r.irca, 0) / municipio.resultados.length;
      const color = IRCARiskThresholds.getColor(avgIRCA);
      
      return {
        label: municipio.municipio, // Nombre del municipio
        data: municipio.resultados.map((resultado: any) => resultado.irca), // Valores IRCA
        borderColor: color, // Color based on IRCA risk level
        backgroundColor: 'rgba(0, 0, 0, 0)', // Fondo transparente
        borderWidth: 2,
      };
    });

    this.chartData = {
      labels: labels, // Ejes X: los años
      datasets: datasets, // Cada línea representa un municipio
    };
  }

  setupChartOptions() {
    this.chartOptions = {
      responsive: true,
      plugins: {
        legend: {
          display: false,
          position: 'left',
          labels: {
            usePointStyle: true,
            pointStyle: 'star',
            pointStyleWidth: 10,
            boxWidth: 1,
            padding: 10,
            font: {
              size: 9,
              weight: 'bold',
              lineHeight: 1.2,
            },
          },
        },
        title: {
          display: false,
          text: 'Índice de Riesgo de Calidad del Agua (IRCA)',
          font: {
            size: 24,
            weight: 'bold',
            lineHeight: 1.2,
          },
          color: 'rgb(90, 79, 243)',
          padding: {
            top: 10,
            bottom: 20,
          },
        },
        tooltip: {
          enabled: true,
          mode: 'dataset',
          intersect: true,
          callbacks: {
            label: (tooltipItem) => {
              const datasetLabel = tooltipItem.dataset.label;
              const value = tooltipItem.raw;
              return `${datasetLabel}: ${value}`;
            },
            labelColor: (context) =>
              ({
                backgroundColor: context.dataset.borderColor,
              } as TooltipLabelStyle),
            title: (tooltipItems) => {
              if (tooltipItems.length) {
                return `Año: ${tooltipItems[0].label}`; // Solo el título del punto activo
              }
              return '';
            },
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Años',
          },
          ticks: {
            autoSkip: true,
            maxTicksLimit: 20,
            font: {
              size: 10,
              weight: 'bold',
            },
          },
        },
        y: {
          title: {
            display: true,
            text: 'IRCA',
          },
          beginAtZero: true,
        },
      },
      elements: {
        point: {
          radius: 5,
          hoverRadius: 7,
        },
        line: {
          tension: 0.1,
          borderWidth: 2,
        },
      },
    };
  }

  setupTableData(municipios: any) {
    this.anios = [
      ...new Set(
        municipios.flatMap((municipio: any) =>
          municipio.resultados.map((r: any) => r.anio.toString())
        )
      ),
    ];

    this.datasource = municipios.map((municipio: any) => {
      const fila: any = {
        municipio: municipio.municipio,
        color:
          this.chartData?.datasets?.find(
            (d: any) => d.label === municipio.municipio
          )?.borderColor ?? 'rgba(0, 0, 0, 1)',
      };
      this.anios.forEach((anio) => {
        const resultado = municipio.resultados.find(
          (r: any) => r.anio.toString() === anio
        );
        fila[anio] = resultado ? resultado.irca.toFixed(2) : '-';
      });
      return fila;
    });

    this.updatePaginatedData(); // Calcula los datos iniciales
  }

  updatePaginatedData() {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.paginatedData = this.datasource.slice(startIndex, endIndex);
  }

  changePage(page: number) {
    this.currentPage = page;
    this.updatePaginatedData();
  }

  iniciarMapa(municipios: any): void {
    if (this.mapa) {
      this.mapa.eachLayer((layer) => this.mapa.removeLayer(layer)); // Limpiar capas
    } else {
      this.mapa = L.map('map').setView([1.5, -77.5], 8); // Crear nuevo mapa
    }

    // Capa base del mapa
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
    }).addTo(this.mapa);

    // Transformar datos para tomar solo el IRCA del último año
    const datosMapaCalor = municipios.map((municipio: any) => {
      const ultimoResultado = municipio.resultados.reduce(
        (ultimo: any, actual: any) =>
          actual.anio > ultimo.anio ? actual : ultimo
      );

      // Crear tooltip con nombre y valor del IRCA directamente sobre el mapa
      const tooltipContenido = `
        <strong>Municipio:</strong> ${municipio.municipio}<br>
        <strong>IRCA:</strong> ${ultimoResultado.irca.toFixed(2)}
      `;

      // Crear una capa para el tooltip usando circleMarker (invisible pero útil para tooltips)
      const punto = L.circleMarker([municipio.lat, municipio.lng], {
        radius: 0, // El radio se pone en 0 para hacerlo invisible
        opacity: 0, // Sin opacidad visible
      }).addTo(this.mapa);

      punto.bindTooltip(tooltipContenido, {
        direction: 'top',
        permanent: false,
      });
      return [municipio.lat, municipio.lng, ultimoResultado.irca / 100];
    });

    // Crear el mapa de calor
    L.heatLayer(datosMapaCalor, {
      radius: 25,
      blur: 15,
      maxZoom: 8,
    }).addTo(this.mapa);

    const bounds = L.latLngBounds(
      municipios.map((municipio: any) => [municipio.lat, municipio.lng])
    );
    this.mapa.fitBounds(bounds);
  }

  onSubmit() {
    if (this.form.valid) {
      const { anioInicio, anioFin, municipio } = this.form.value;
      this.#dashboardDataService
        .getDashboardData(anioInicio, anioFin, municipio)
        .subscribe({
          next: (data: MunicipioData[]) => {
            if (data && data.length > 0) {
              this.setupChartData(data);
              this.setupChartOptions();
              this.setupTableData(data);
              this.iniciarMapa(data);
            }
          },
          error: (error) => {
            console.error('Failed to filter dashboard data:', error);
            // Error toast will be shown by interceptor
          }
        });
    }
  }
}
