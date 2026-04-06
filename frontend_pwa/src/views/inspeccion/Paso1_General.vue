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
          {{ coordenadasListas ? `Radar: 100m | GPS: ±${precisionGPS?.toFixed(1) || '0'}m` : 'GPS: BUSCANDO...' }}
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
              @focus="menuSugerenciasAbierto = true"
              @blur="cerrarMenuSugerencias"
              class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
            />
            
            <!-- Menú Desplegable Técnico (Alternativa a Datalist) -->
            <div v-if="menuSugerenciasAbierto && pozosDetectadosIds.length > 0" class="absolute left-0 right-0 top-full mt-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl z-50 max-h-60 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800 animate-in border-t-4 border-t-accent-blue">
              <div 
                v-for="id in pozosDetectadosIds" 
                :key="id"
                @click="inspeccionStore.inspeccionActual.id_pozo = id; menuSugerenciasAbierto = false"
                class="p-4 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between group transition-colors"
                :class="inspeccionStore.inspeccionActual.id_pozo === id ? 'bg-blue-50 dark:bg-blue-900/20' : ''"
              >
                <div class="flex items-center gap-3">
                  <span class="material-symbols-outlined text-slate-400 group-hover:text-accent-blue transition-colors">location_searching</span>
                  <span class="text-sm font-black text-slate-700 dark:text-slate-300 group-hover:text-accent-blue">{{ id }}</span>
                </div>
                <span v-if="inspeccionStore.inspeccionActual.id_pozo === id" class="material-symbols-outlined text-accent-blue text-sm">check_circle</span>
                <span v-else class="text-[8px] font-bold text-slate-400 uppercase tracking-widest">A 100m</span>
              </div>
            </div>
          </div>
          
          <!-- Sugerencias del Radar (Carrusel Lateral) -->
          <div v-if="pozosDetectadosIds.length > 0" class="flex flex-col gap-2 animate-in overflow-hidden">
            <span class="text-[9px] font-black text-slate-400 uppercase tracking-widest pl-1">Sugerencias Radar (100m)</span>
            <div class="flex flex-nowrap gap-2 overflow-x-auto pb-2 px-1 scrollbar-hide snap-x">
              <button 
                v-for="id in pozosDetectadosIds" 
                :key="id"
                @click="inspeccionStore.inspeccionActual.id_pozo = id"
                class="flex-none px-5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs font-black text-slate-600 dark:text-slate-400 hover:bg-accent-blue hover:text-white dark:hover:bg-accent-blue dark:hover:text-white transition-all shadow-sm active:scale-95 snap-start min-w-[80px] text-center"
              >
                {{ id }}
              </button>
            </div>
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
            <div class="flex gap-2 items-center">
              <button 
                type="button"
                @click="simularAsGandaras"
                class="text-[9px] font-black text-white bg-slate-900 dark:bg-accent-blue px-3 py-1 rounded-full uppercase hover:scale-105 active:scale-95 transition-all"
              >
                Simular As Gándaras
              </button>
              <span v-if="!isOnline" class="text-[8px] font-black text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-0.5 rounded-full border border-amber-200 dark:border-amber-800 uppercase">Offline</span>
            </div>
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

        <!-- Estado Especial: No Inspeccionable -->
        <div class="sm:col-span-2 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-6 rounded-3xl transition-all group" :class="{ '!bg-red-50 !border-red-200 dark:!bg-red-900/20 dark:!border-red-900/50 ring-4 ring-red-600/5': inspeccionStore.inspeccionActual.no_inspeccionable }">
          <label class="flex items-center gap-4 cursor-pointer select-none">
            <div class="relative flex items-center">
              <input 
                type="checkbox" 
                v-model="inspeccionStore.inspeccionActual.no_inspeccionable"
                class="peer sr-only"
              />
              <div class="w-14 h-14 bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-700 rounded-2xl flex items-center justify-center transition-all peer-checked:bg-red-600 peer-checked:border-red-600 peer-checked:scale-95 shadow-lg group-active:scale-90">
                <span class="material-symbols-outlined text-slate-300 dark:text-slate-600 peer-checked:text-white transition-all scale-75 peer-checked:scale-110">block</span>
              </div>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-[0.1em]" :class="{ 'text-red-700 dark:text-red-400': inspeccionStore.inspeccionActual.no_inspeccionable }">No se puede inspeccionar</span>
              <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wide opacity-70">Activa si el pozo está asfaltado o la tapa bloqueada</span>
            </div>
          </label>
        </div>

        <!-- Coordenadas UTM Section -->
        <div class="sm:col-span-2 pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
          <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Georreferenciación y Cota (Huso 29N)</label>
          <div class="grid grid-cols-1 gap-4">
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
import { db } from '@/db/db';
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
let gisLayerGroup: L.LayerGroup | null = null;
let gisLayers: { [key: string]: L.Layer } = {};

// Inventario de Pozos de Proximidad
const pozosCercanos = ref<any[]>([]);

const pozosDetectadosIds = ref<string[]>([]);
const menuSugerenciasAbierto = ref(false);
const precisionGPS = ref<number | null>(null);

const cerrarMenuSugerencias = () => {
  setTimeout(() => {
    menuSugerenciasAbierto.value = false;
  }, 200);
};

const coordenadasListas = computed(() => {
  return inspeccionStore.inspeccionActual.coordenadas_utm.x !== null 
      && inspeccionStore.inspeccionActual.coordenadas_utm.y !== null;
});

// Inicializar el mapa
onMounted(() => {
  // Convertir centro UTM proporcionado a Lat/Lng para el mapa
  const [lng, lat] = proj4(UTM_29N, WGS84, [523380.97, 4676363.63]);
  
  map = L.map('map-step-1', {
    zoomControl: false,
    attributionControl: false,
    maxZoom: 22,
    preferCanvas: true
  }).setView([lat, lng], 18);


  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri',
    maxZoom: 22,
    maxNativeZoom: 19
  }).addTo(map);

  nearbyWellsLayer = L.layerGroup().addTo(map);
  gisLayerGroup = L.layerGroup().addTo(map);

  // [NUEVO] Capas de Red y Zona
  cargarCapasGIS();

  // Control de visibilidad por zoom
  map.on('zoomend', () => {
    if (!map || !gisLayerGroup) return;
    if (map.getZoom() < 16) {
      if (map.hasLayer(gisLayerGroup)) map.removeLayer(gisLayerGroup);
    } else {
      if (!map.hasLayer(gisLayerGroup)) map.addLayer(gisLayerGroup);
    }
  });

  // Cargar inventario de pozos (GeoJSON)
  cargarInventario();

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

const simularAsGandaras = () => {
  // Coordenadas aproximadas en el centro del polígono de As Gándaras (Porriño)
  const [lng, lat] = [-8.616, 42.137];
  const [utmX, utmY] = proj4(WGS84, UTM_29N, [lng, lat]);
  
  inspeccionStore.inspeccionActual.coordenadas_utm = {
    x: Number(utmX.toFixed(2)),
    y: Number(utmY.toFixed(2))
  };
  
  inspeccionStore.inspeccionActual.calle_zona = "Polígono As Gándaras (SIMULADO)";
  precisionGPS.value = 5; // Simular alta precisión
  
  console.log("Simulación en As Gándaras activada para pruebas GIS.");
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
    x: 523380.97,
    y: 4676363.63
  };
  if (navigator.onLine) {
    const [lng, lat] = proj4(UTM_29N, WGS84, [523380.97, 4676363.63]);
    buscarDireccion(lat, lng);
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
          interactive: false, // Permite clickear lo que haya debajo
          zIndexOffset: -100, // Lo mantiene por debajo de los pozos en términos de click
          icon: L.divIcon({
            className: 'custom-user-marker',
            html: `<div class="radar-pulse"></div><div class="inner-dot"></div>`,
            iconSize: [50, 50], // Aumentado
            iconAnchor: [25, 25] // Ajustado al centro
          })
        }).addTo(map);

        // 2. Actualizar Radar (100m)
        if (radarCircle) map.removeLayer(radarCircle);
        radarCircle = L.circle(coords, {
            radius: 100,
            color: '#FACC15',
            fillColor: '#FACC15',
            fillOpacity: 0.15,
            weight: 3, // Más visible
            dashArray: '8, 8',
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

const cargarInventario = async () => {
  try {
    // 1. Verificar si ya tenemos datos en IndexedDB
    const totalEnDb = await db.inventario_pozos.count();
    
    if (totalEnDb === 0) {
      console.log("Inventario vacío. Descargando repositorio de pozos...");
      const response = await fetch('/data/pozos.geojson');
      if (!response.ok) throw new Error("No se pudo descargar el inventario inicial.");
      
      const data = await response.json();
      if (data && data.features) {
        console.log("Procesando e indexando pozos para uso offline...");
        const batch = data.features.map((f: any) => ({
          id: String(f.properties.COD_CAMPO || f.properties.ObjectId || f.properties.id),
          x: f.geometry.coordinates[0],
          y: f.geometry.coordinates[1],
          properties: f.properties
        }));
        
        await db.inventario_pozos.bulkAdd(batch);
        console.log(`¡Inventario indexado! ${batch.length} pozos guardados.`);
      }
    } else {
      // Verificar si los datos existentes son antiguos (ObjectId vs COD_CAMPO)
      const primerPozo = await db.inventario_pozos.limit(1).toArray();
      if (primerPozo.length > 0 && primerPozo[0] && !isNaN(Number(primerPozo[0].id))) {
        console.log("Detectado formato antiguo. Limpiando caché de pozos...");
        await db.inventario_pozos.clear();
        return cargarInventario(); // Re-intentar carga con nuevo formato
      }
      console.log(`Usando inventario local offline (${totalEnDb} pozos detectados).`);
    }

    // Calcular pozos cercanos si ya tenemos GPS
    const x = inspeccionStore.inspeccionActual.coordenadas_utm.x;
    const y = inspeccionStore.inspeccionActual.coordenadas_utm.y;
    if (x && y) actualizarPozosCercanos(x, y);

  } catch (err) {
    console.warn("No se pudo cargar el inventario (¿Modo avión inicial?):", err);
  }
};

const cargarCapasGIS = async () => {
  if (!map) return;

  const capas = [
    { url: '/data/principales.geojson', style: { color: '#FF0000', weight: 6, opacity: 1 }, name: 'principales' },
    { url: '/data/secundarios.geojson', style: { color: '#FFFF00', weight: 4, opacity: 1 }, name: 'secundarios' }
  ];

  for (const capa of capas) {
    try {
      const resp = await fetch(capa.url);
      if (!resp.ok) continue;
      const data = await resp.json();
      
      gisLayers[capa.name] = L.geoJSON(data, {
        style: capa.style,
        interactive: false,
        coordsToLatLng: (coords) => {
          // Si las coordenadas son muy grandes, asumimos que son UTM y proyectamos
          if (Math.abs(coords[0]) > 180) {
            const [lng, lat] = proj4(UTM_29N, WGS84, [coords[0], coords[1]]);
            return L.latLng(lat, lng);
          }
          return L.latLng(coords[1], coords[0]);
        }
      }).addTo(gisLayerGroup!);
    } catch (e) {
      console.warn(`No se pudo cargar la capa GIS ${capa.name}:`, e);
    }
  }
};


const actualizarPozosCercanos = async (userX: number, userY: number) => {
  if (!nearbyWellsLayer || !map) return;
  nearbyWellsLayer.clearLayers();
  
  const radioBusqueda = 100;

  // Búsqueda espacial optimizada: Filtramos primero por Bounding Box cuadrado 
  // antes de calcular la distancia euclídea exacta
  const pozosEnRango = await db.inventario_pozos
    .where('x').between(userX - radioBusqueda, userX + radioBusqueda)
    .and(pozo => {
      const dist = Math.sqrt(Math.pow(pozo.x - userX, 2) + Math.pow(pozo.y - userY, 2));
      return dist <= radioBusqueda;
    })
    .toArray();

  const detectados: string[] = [];
  pozosCercanos.value = pozosEnRango;

  pozosEnRango.forEach(pozo => {
    detectados.push(pozo.id);
    const isSelected = pozo.id === inspeccionStore.inspeccionActual.id_pozo;
    const [lng, lat] = proj4(UTM_29N, WGS84, [pozo.x, pozo.y]);
    
    const wellMarker = L.marker([lat, lng], {
      zIndexOffset: isSelected ? 2000 : 500, // Siempre por encima de las redes y del GPS si está seleccionado
      icon: L.divIcon({
        className: `well-marker-radar ${isSelected ? 'is-selected' : ''}`,
        html: `<div class="well-dot"></div><span class="well-label">${pozo.id}</span>`,
iconSize: [30,30],   // <-- Cambia este 60 por el tamaño que quieras
iconAnchor: [15,15]
      })
    });

    wellMarker.on('click', () => {
      inspeccionStore.inspeccionActual.id_pozo = pozo.id;
    });

    wellMarker.addTo(nearbyWellsLayer!);
  });

  pozosDetectadosIds.value = detectados;
};

// Observar cambios en el ID seleccionado para repintar el marcador seleccionado sin mover el radar
watch(() => inspeccionStore.inspeccionActual.id_pozo, () => {
  // Solo repintamos los marcadores existentes para actualizar el estado visual (is-selected)
  // sin volver a filtrar por distancia, para no perder los "compañeros" de la lista
  repintarMarcadores();
});

const repintarMarcadores = () => {
  if (!nearbyWellsLayer || !map) return;
  
  // En lugar de borrar todo, recorremos y actualizamos clases si fuera posible, 
  // pero Leaflet L.LayerGroup es más sencillo de recrear si no hay miles de puntos.
  // Dado que radioBusqueda es 100m, habrá pocos pozos.
  const x = inspeccionStore.inspeccionActual.coordenadas_utm.x;
  const y = inspeccionStore.inspeccionActual.coordenadas_utm.y;
  if (x && y) actualizarPozosCercanos(x, y);
};

// Lógica para Pozo No Inspeccionable
watch(() => inspeccionStore.inspeccionActual.no_inspeccionable, (newVal) => {
  if (newVal) {
    const i = inspeccionStore.inspeccionActual;
    // Poner a 0 diámetros y dimensiones
    i.tapa_diametro_mm = 0;
    i.tapa_largo_mm = 0;
    i.tapa_ancho_mm = 0;
    i.diametro_pozo_mm = 0;
    i.largo_pozo_mm = 0;
    i.ancho_pozo_mm = 0;
    i.colector_diametro_entrada_mm = 0;
    i.colector_diametro_salida_mm = 0;
    i.profundidad_m = 0;
    i.num_pates = 0;
    
    // Comentarios y estados
    i.observaciones = "No se puede Inspeccionar";
    i.estado = "Deficiente";
    i.limpieza = "No procede";
  }
});

// Observar cambios en coordenadas para mover el marcador y buscar dirección
watch(() => inspeccionStore.inspeccionActual.coordenadas_utm, (newCoords) => {
  actualizarMarcador();
  
  if (newCoords.x && newCoords.y && navigator.onLine) {
    const [lng, lat] = proj4(UTM_29N, WGS84, [newCoords.x, newCoords.y]);
    buscarDireccion(lat, lng);
  }
}, { deep: true });

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
  width: 30%; 
  height: 30%;
  background: #3b82f6;
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
  z-index: 2;
}
:deep(.radar-pulse) {
  position: absolute;
  width: 60px; 
  height: 60px;
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
  width: 80%; 
  height: 80%;
  background: white;
  border: 3px solid #363842;
  border-radius: 50%;
  transition: all 0.2s;
}
:deep(.well-marker-radar:hover .well-dot) {
  background: #99CCFF;
  transform: scale(1.5);
}
:deep(.well-label) {
  position: absolute;
  top: 100%;
  margin-top: 8px;
  background: #000000;
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 6px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 1;
  border: 1.5px solid #FFFFFF;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

/* Estado Seleccionado */
:deep(.well-marker-radar.is-selected .well-dot) {
  background: #3b82f6;
  border-color: white;
  transform: scale(1.4);
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.8);
}
:deep(.well-marker-radar.is-selected .well-label) {
  background: #3b82f6;
  opacity: 1;
  transform: translateY(2px) scale(1.1);
}

/* Utilidades para el Carrusel */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
