import * as L from 'leaflet'; // Importar tipos de Leaflet

declare module 'leaflet' {
  interface HeatLayerOptions {
    radius?: number; // Radio del mapa de calor
    blur?: number;   // Nivel de desenfoque
    maxZoom?: number; // Zoom máximo
  }

  function heatLayer(latLngIntensity: [number, number, number][], options?: HeatLayerOptions): L.Layer;
}
