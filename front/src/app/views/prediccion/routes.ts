import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./prediccion.component').then(m => m.PrediccionComponent),
    data: {
      title: 'Predicción IRCA'
    }
  }
];
