<template>
  <div class="flex flex-col md:flex-row min-h-[500px] md:h-full flex-1 bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <!-- Left Column: Map (Responsive height/width) -->
    <div class="relative h-64 md:h-auto md:min-h-[600px] md:w-1/2 bg-slate-200 dark:bg-slate-800 border-b md:border-b-0 md:border-r border-slate-200 dark:border-slate-800 overflow-hidden shadow-inner">
      <div id="map-step-1" class="w-full h-full min-h-[400px] md:min-h-[600px] z-0"></div>
      
      <!-- Overlays for Map Control -->
      <div class="absolute top-4 right-4 z-10 flex flex-col gap-2">
        <button @click="capturarGPS" class="flex h-12 w-12 items-center justify-center rounded-xl bg-white dark:bg-slate-900 text-primary dark:text-accent-blue shadow-lg border border-slate-200 dark:border-slate-800 active:scale-95 transition-all">
          <span class="material-symbols-outlined">my_location</span>
        </button>
      </div>

      <!-- Precision Indicator Overlay -->
      <div class="absolute bottom-4 left-4 z-10 px-3 py-1.5 bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm rounded-lg border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-2">
        <div class="flex h-2 w-2 rounded-full" :class="coordenadasListas ? 'bg-green-500' : 'bg-amber-500 animate-pulse'"></div>
        <span class="text-[10px] font-black uppercase tracking-widest text-slate-600 dark:text-slate-400">
          {{ coordenadasListas ? `GPS Fix: ±${precisionGPS?.toFixed(1) || '0'}m` : 'GPS: BUSCANDO...' }}
        </span>
      </div>
    </div>

    <!-- Right Column: Form Content (Scrollable on Tablet) -->
    <div class="flex-1 p-6 md:p-10 space-y-8 overflow-y-auto">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Información General</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Registro Técnico de Activos / Referenciación Espacial</p>
      </div>

      <!-- Form Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-8">
        
        <!-- Id Activo -->
        <div class="flex flex-col gap-3">
          <label for="id_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">ID del Activo (Pozo)</label>
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors">badge</span>
            <input 
              id="id_pozo" 
              v-model="inspeccionStore.inspeccionActual.id_pozo"
              type="text" 
              placeholder="P-0000"
              class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
            />
          </div>
        </div>

        <!-- Fecha de Inspección -->
        <div class="flex flex-col gap-3">
          <label for="fecha_inspec" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Fecha de Registro</label>
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors">calendar_today</span>
            <input 
              id="fecha_inspec" 
              v-model="inspeccionStore.inspeccionActual.fecha_inspec"
              type="date" 
              class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
            />
          </div>
        </div>

        <!-- Situación en Vía -->
        <div class="flex flex-col gap-3">
          <label for="situacion" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Situación en Vía</label>
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">traffic</span>
            <select 
              id="situacion" 
              v-model="inspeccionStore.inspeccionActual.situacion"
              required
              class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-10 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none appearance-none"
            >
              <option value="" disabled selected>Seleccione ubicación...</option>
              <option value="Calzada">Calzada</option>
              <option value="Acera">Acera</option>
              <option value="Mediana">Mediana</option>
              <option value="Jardín">Jardín</option>
              <option value="Descampado">Descampado</option>
            </select>
            <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">expand_more</span>
          </div>
        </div>

        <!-- Calle / Localización -->
        <div class="flex flex-col gap-3">
          <div class="flex items-center justify-between">
            <label for="calle_zona" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Calle / Localización</label>
            <span v-if="!isOnline" class="text-[8px] font-black text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-0.5 rounded-full border border-amber-200 dark:border-amber-800 uppercase">Offline</span>
          </div>
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors">location_on</span>
            <input 
              id="calle_zona" 
              v-model="inspeccionStore.inspeccionActual.calle_zona"
              type="text" 
              placeholder="Autodectar con GPS o escribir..."
              class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
            />
          </div>
        </div>

        <!-- Coordenadas UTM Section -->
        <div class="sm:col-span-2 pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
          <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Georreferenciación y Cota (Huso 29N)</label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 lg:gap-6">
            <div class="bg-slate-100 dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-inner">
              <span class="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-2">Coordenada X (Easting)</span>
              <input 
                v-model.number="inspeccionStore.inspeccionActual.coordenadas_utm.x"
                type="number" 
                step="0.01"
                class="w-full bg-transparent border-none p-0 font-mono text-2xl font-black text-slate-900 dark:text-white focus:ring-0"
              />
            </div>
            <div class="bg-slate-100 dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-inner">
              <span class="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-2">Coordenada Y (Northing)</span>
              <input 
                v-model.number="inspeccionStore.inspeccionActual.coordenadas_utm.y"
                type="number" 
                step="0.01"
                class="w-full bg-transparent border-none p-0 font-mono text-2xl font-black text-slate-900 dark:text-white focus:ring-0"
              />
            </div>
            <div class="bg-slate-100 dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-inner">
              <span class="block text-[8px] font-black text-slate-500 uppercase tracking-widest mb-2">Cota Z (Tapa)</span>
              <input 
                v-model.number="inspeccionStore.inspeccionActual.cota_tapa"
                type="number" 
                step="0.01"
                placeholder="0.00"
                class="w-full bg-transparent border-none p-0 font-mono text-2xl font-black text-slate-900 dark:text-white focus:ring-0"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Placeholder spacing for navigation bar -->
      <div class="h-24 md:hidden"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { useInspeccionStore } from '@/store/inspeccion';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import proj4 from 'proj4';

// Arreglo para que Vite empaquete correctamente los iconos por defecto de Leaflet en producción
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
});

// Definición de proyecciones: ETRS89 Huso 29N (Galicia/Coruña) y WGS84
const UTM_29N = "+proj=utm +zone=29 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs";
const WGS84 = "EPSG:4326";

const inspeccionStore = useInspeccionStore();
const isOnline = ref(navigator.onLine);
let map: L.Map | null = null;
let marker: L.Marker | null = null;
let radarCircle: L.Circle | null = null;
let nearbyWellsLayer: L.LayerGroup | null = null;

// Mock de Inventario de Pozos (Datos de ejemplo)
const pozosInventario = [
  { id: 'P-5001', x: 547242.45, y: 4799842.12 },
  { id: 'P-5002', x: 547192.45, y: 4799792.12 },
  { id: 'P-5003', x: 547262.45, y: 4799762.12 },
  { id: 'P-5004', x: 547152.45, y: 4799862.12 },
  { id: 'P-9999', x: 548212.45, y: 4801812.12 }, // Lejos (fuera de radar)
];

const precisionGPS = ref<number | null>(null);

const coordenadasListas = computed(() => {
  return inspeccionStore.inspeccionActual.coordenadas_utm.x !== null 
      && inspeccionStore.inspeccionActual.coordenadas_utm.y !== null;
});

// Inicializar el mapa
onMounted(() => {
  map = L.map('map-step-1', {
    zoomControl: false,
    attributionControl: false
  }).setView([43.3623, -8.4115], 18); // Default Coruña

  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EBP, and the GIS User Community',
    maxZoom: 19
  }).addTo(map);

  nearbyWellsLayer = L.layerGroup().addTo(map);

  // Si ya hay coordenadas, poner el marcador
  actualizarMarcador();

  // [NUEVO] Si no hay coordenadas, forzamos la captura GPS inmediata al abrir
  if (!coordenadasListas.value) {
    capturarGPS();
  }

  nextTick(() => {
    if (map) map.invalidateSize();
  });

  window.addEventListener('online', () => isOnline.value = true);
  window.addEventListener('offline', () => isOnline.value = false);
});

// Captura GPS Real (si es posible) o Mock
const capturarGPS = () => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const accuracy = position.coords.accuracy;
      
      precisionGPS.value = accuracy;

      // Convertir WGS84 (Lat/Lng) a UTM 29N
      const [utmX, utmY] = proj4(WGS84, UTM_29N, [lng, lat]);
      
      inspeccionStore.inspeccionActual.coordenadas_utm = {
        x: Number(utmX.toFixed(2)),
        y: Number(utmY.toFixed(2))
      };

      // Intentar buscar la dirección si hay conexión
      if (navigator.onLine) {
        buscarDireccion(lat, lng);
      }
    }, (error) => {
      console.error("Error capturando GPS:", error);
      // Fallback a Mock si falla
      mockGPS();
    }, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    });
  } else {
    mockGPS();
  }
};

const buscarDireccion = async (lat: number, lng: number) => {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`, {
      headers: {
        'Accept-Language': 'es'
      }
    });
    const data = await response.json();
    if (data && data.display_name) {
      // Intentamos extraer algo amigable de la dirección
      const addr = data.address;
      const calle = addr.road || addr.pedestrian || addr.suburb || addr.city || "";
      const numero = addr.house_number ? `, ${addr.house_number}` : "";
      
      if (calle) {
        inspeccionStore.inspeccionActual.calle_zona = `${calle}${numero}`;
      } else {
        inspeccionStore.inspeccionActual.calle_zona = data.display_name.split(',').slice(0, 2).join(',');
      }
    }
  } catch (err) {
    console.warn("No se pudo obtener la dirección automática:", err);
  }
};

const mockGPS = () => {
    precisionGPS.value = 3.5;
    inspeccionStore.inspeccionActual.coordenadas_utm = {
    x: 547212.45,
    y: 4799812.12
  };
  if (navigator.onLine) {
    buscarDireccion(43.3623, -8.4115);
  }
};

const actualizarMarcador = () => {
  if (map && coordenadasListas.value) {
    const x = inspeccionStore.inspeccionActual.coordenadas_utm.x;
    const y = inspeccionStore.inspeccionActual.coordenadas_utm.y;
    
    if (x && y) {
      try {
        // Convertir UTM 29N a WGS84 (Lat/Lng) para Leaflet
        const [lng, lat] = proj4(UTM_29N, WGS84, [x, y]);
        const coords: L.LatLngExpression = [lat, lng];
        
        // 1. Actualizar Marcador Usuario
        if (marker) map.removeLayer(marker);
        marker = L.marker(coords, {
          icon: L.divIcon({
            className: 'custom-user-marker',
            html: `<div class="radar-pulse"></div><div class="inner-dot"></div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
          })
        }).addTo(map);

        // 2. Actualizar Radar (100m)
        if (radarCircle) map.removeLayer(radarCircle);
        radarCircle = L.circle(coords, {
          radius: 100,
          color: '#99CCFF',
          fillColor: '#99CCFF',
          fillOpacity: 0.1,
          weight: 1,
          dashArray: '5, 5',
          interactive: false
        }).addTo(map);

        // 3. Filtrar y Dibujar Pozos cercanos
        actualizarPozosCercanos(x, y);

        map.setView(coords, 19, { animate: false });
      } catch (err) {
        console.error("Error en la conversión de coordenadas:", err);
      }
    }
  }
};

const actualizarPozosCercanos = (userX: number, userY: number) => {
  if (!nearbyWellsLayer || !map) return;
  nearbyWellsLayer.clearLayers();

  pozosInventario.forEach(pozo => {
    const dist = Math.sqrt(Math.pow(pozo.x - userX, 2) + Math.pow(pozo.y - userY, 2));
    
    if (dist <= 100) {
      const [lng, lat] = proj4(UTM_29N, WGS84, [pozo.x, pozo.y]);
      const wellMarker = L.marker([lat, lng], {
        icon: L.divIcon({
          className: 'well-marker-radar',
          html: `<div class="well-dot"></div><span class="well-label">${pozo.id}</span>`,
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        })
      });

      wellMarker.on('click', () => {
        inspeccionStore.inspeccionActual.id_pozo = pozo.id;
        // Efecto haptico visual (glow temporal) puede ir aquí
      });

      wellMarker.addTo(nearbyWellsLayer!);
    }
  });
};

// Observar cambios en coordenadas para mover el marcador
watch(() => inspeccionStore.inspeccionActual.coordenadas_utm, actualizarMarcador, { deep: true });

</script>

<style scoped>
/* Eliminar flechas de inputs numéricos */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

/* Transiciones de entrada */
.animate-in {
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Estilos Radar y Marcadores */
:deep(.custom-user-marker) {
  display: flex;
  align-items: center;
  justify-content: center;
}
:deep(.inner-dot) {
  width: 12px;
  height: 12px;
  background: #3b82f6;
  border: 2px solid white;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
  z-index: 2;
}
:deep(.radar-pulse) {
  position: absolute;
  width: 30px;
  height: 30px;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 50%;
  animation: pulse 2s infinite;
  z-index: 1;
}

@keyframes pulse {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}

:deep(.well-marker-radar) {
  display: flex;
  flex-direction: column;
  align-items: center;
}
:deep(.well-dot) {
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid #363842;
  border-radius: 50%;
  transition: all 0.2s;
}
:deep(.well-marker-radar:hover .well-dot) {
  background: #99CCFF;
  transform: scale(1.5);
}
:deep(.well-label) {
  position: absolute;
  top: 14px;
  background: #363842;
  color: white;
  font-size: 8px;
  font-weight: 900;
  padding: 1px 4px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0.8;
}
</style>
