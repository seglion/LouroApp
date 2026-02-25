<template>
  <div class="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 p-6 md:p-10 space-y-10 max-w-[1024px] mx-auto w-full">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-4">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Detalles del Pozo</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Especificaciones estructurales y sistemas de acceso</p>
      </div>

      <!-- Section: Morfología y Material -->
      <div class="space-y-3">
        <div class="flex items-center gap-4">
          <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Estructura y Dimensiones</h3>
          <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Forma del Pozo Select -->
          <div class="flex flex-col gap-3">
            <label for="forma_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Forma del Pozo</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">hexagon</span>
              <select 
                id="forma_pozo" 
                v-model="inspeccionStore.inspeccionActual.forma_pozo"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-10 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none appearance-none"
              >
                <option value="Circular">Circular</option>
                <option value="Cuadrado">Cuadrado</option>
                <option value="Rectangular">Rectangular</option>
                <option value="Irregular">Irregular</option>
              </select>
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">expand_more</span>
            </div>
          </div>

          <!-- Dimensiones dinámicas -->
          <div class="grid grid-cols-2 gap-4">
            <div v-if="inspeccionStore.inspeccionActual.forma_pozo === 'Circular'" class="col-span-2">
              <div class="flex flex-col gap-3">
                <label for="diametro_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Diámetro (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">adjust</span>
                  <input 
                    id="diametro_pozo" 
                    v-model.number="inspeccionStore.inspeccionActual.diametro_pozo_mm"
                    type="number" 
                    placeholder="1000"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
            </div>
            <template v-else>
              <div class="flex flex-col gap-3">
                <label for="largo_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Largo (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">straighten</span>
                  <input 
                    id="largo_pozo" 
                    v-model.number="inspeccionStore.inspeccionActual.largo_pozo_mm"
                    type="number" 
                    placeholder="1000"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <label for="ancho_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Ancho (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">straighten</span>
                  <input 
                    id="ancho_pozo" 
                    v-model.number="inspeccionStore.inspeccionActual.ancho_pozo_mm"
                    type="number" 
                    placeholder="1000"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
            </template>
          </div>

          <!-- Material del Pozo -->
          <div class="flex flex-col gap-3">
            <label for="material_pozo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Material del Pozo</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">layers</span>
              <select 
                id="material_pozo" 
                v-model="inspeccionStore.inspeccionActual.material_pozo"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-10 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none appearance-none"
              >
                <option value="" disabled selected>Seleccione material...</option>
                <option value="Hormigón">Hormigón</option>
                <option value="Hormigón Prefrabricado">Hormigón Prefrabricado</option>
                <option value="Ladrillo">Ladrillo</option>
                <option value="PVC">PVC</option>
                <option value="Polietileno">Polietileno</option>
              </select>
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">expand_more</span>
            </div>
          </div>

          <!-- Profundidad Total -->
          <div class="flex flex-col gap-3">
            <label for="profundidad" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Profundidad Total (m)</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">straighten</span>
              <input 
                id="profundidad" 
                v-model.number="inspeccionStore.inspeccionActual.profundidad_m"
                type="number" 
                step="0.01"
                placeholder="0.00"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Section: Acceso y Pates -->
      <div class="space-y-8">
        <div class="flex items-center gap-4">
          <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Acceso y Seguridad</h3>
          <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Tipo de Acceso (Pates/Escalones) -->
          <div class="flex flex-col gap-4">
            <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Sistema de Acceso</label>
            <div class="flex p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
              <button 
                v-for="opt in ['Pates', 'Escalones', 'Grapas', 'Ninguno']" 
                :key="opt"
                @click="inspeccionStore.inspeccionActual.tipo_acceso = opt"
                :class="inspeccionStore.inspeccionActual.tipo_acceso === opt 
                  ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg' 
                  : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all"
              >
                {{ opt }}
              </button>
            </div>
          </div>

          <!-- Número de Pates (Solo si hay acceso) -->
          <div v-if="inspeccionStore.inspeccionActual.tipo_acceso !== 'Ninguno' && inspeccionStore.inspeccionActual.tipo_acceso !== ''" class="flex flex-col gap-3">
            <label for="num_pates" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Cantidad de Peldaños</label>
            <div class="flex items-center gap-4">
              <button @click="inspeccionStore.inspeccionActual.num_pates > 0 && inspeccionStore.inspeccionActual.num_pates--" class="h-16 w-16 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center text-primary dark:text-white active:scale-90 transition-transform shadow-sm hover:border-accent-blue transition-colors">
                <span class="material-symbols-outlined">remove</span>
              </button>
              <div class="flex-1 h-16 bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center justify-center border-dashed">
                <span class="text-2xl font-black text-primary dark:text-white font-mono">{{ inspeccionStore.inspeccionActual.num_pates }}</span>
              </div>
              <button @click="inspeccionStore.inspeccionActual.num_pates++" class="h-16 w-16 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center text-primary dark:text-white active:scale-90 transition-transform shadow-sm hover:border-accent-blue transition-colors">
                <span class="material-symbols-outlined">add</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Section: Estado y Anomalías -->
      <div class="space-y-8">
        <div class="flex items-center gap-4">
          <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Anomalías Estructurales</h3>
          <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Switches / Toggles para Anomalías -->
          <template v-for="anom in [
            { key: 'resalto', label: 'Resalto', icon: 'keyboard_tab' },
            { key: 'filtraciones', label: 'Filtraciones', icon: 'water_drop' },
            { key: 'pluviales', label: 'Pluviales', icon: 'rainy' },
            { key: 'biofilm', label: 'Biofilm', icon: 'vape_free' }
          ]" :key="anom.key">
            <div @click="(inspeccionStore.inspeccionActual as any)[anom.key] = ((inspeccionStore.inspeccionActual as any)[anom.key] === 'Sí' ? 'No' : 'Sí')" 
                 class="group flex flex-col items-center justify-center gap-3 p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl cursor-pointer active:scale-[0.98] transition-all shadow-sm hover:border-accent-blue/50">
              <span class="material-symbols-outlined text-3xl transition-colors" :class="(inspeccionStore.inspeccionActual as any)[anom.key] === 'Sí' ? 'text-accent-blue' : 'text-slate-400 group-hover:text-slate-600'">{{ anom.icon }}</span>
              <span class="text-[10px] font-black text-slate-700 dark:text-slate-200 uppercase tracking-widest">{{ anom.label }}</span>
              <div class="w-10 h-5 rounded-full relative transition-colors duration-200" :class="(inspeccionStore.inspeccionActual as any)[anom.key] === 'Sí' ? 'bg-accent-blue' : 'bg-slate-200 dark:bg-slate-700'">
                <div class="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full transition-transform duration-200" :class="(inspeccionStore.inspeccionActual as any)[anom.key] === 'Sí' ? 'translate-x-5' : 'translate-x-0'"></div>
              </div>
            </div>
          </template>
        </div>
      </div>
      
      <!-- Placeholder spacing for navigation bar (Mobile only) -->
      <div class="h-24 md:hidden"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue';
import { useInspeccionStore } from '@/store/inspeccion';

const inspeccionStore = useInspeccionStore();

// Limpiar dimensiones cuando se cambia la forma del pozo
watch(() => inspeccionStore.inspeccionActual.forma_pozo, (newForma) => {
  if (newForma === 'Circular') {
    inspeccionStore.inspeccionActual.largo_pozo_mm = null;
    inspeccionStore.inspeccionActual.ancho_pozo_mm = null;
  } else {
    inspeccionStore.inspeccionActual.diametro_pozo_mm = null;
  }
});
</script>

<style scoped>
/* Eliminar flechas de inputs numéricos */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  appearance: none;
  margin: 0;
}
input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
}

select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}
</style>
