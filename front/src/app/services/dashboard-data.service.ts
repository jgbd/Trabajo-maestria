// serivio para obtener los datos desde una api
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class DashboardDataService {
  private apiUrl = environment.apiUrl; // Replace with your API URL

  constructor(private http: HttpClient) {}

  getDashboardData(anioInicio?: number, anioFin?: number, codigo_municipio?: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/estadisticas`, {
      params: {
        ...(anioInicio !== undefined && { anioInicio }),
        ...(anioFin !== undefined && { anioFin }),
        ...(codigo_municipio !== undefined && { codigo_municipio }),
      },
    });
  }

  getMunicipios(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/municipios`);
  }
}
