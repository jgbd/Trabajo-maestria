import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./resultados.component').then(m => m.ResultadosComponent),
    data: {
      title: 'Resultados Detallados'
    }
  }
];
