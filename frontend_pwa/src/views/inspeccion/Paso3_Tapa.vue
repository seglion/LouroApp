<template>
  <div class="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 p-6 md:p-10 space-y-10 max-w-[1024px] mx-auto w-full">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Detalles de la Tapa</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Especificaciones de cierre y acceso superior</p>
      </div>

      <!-- Section: Cota y Morfología -->
      <div class="space-y-8">
        <div class="flex items-center gap-4">
          <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Ubicación y Forma</h3>
          <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Cota de la Tapa -->
          <div class="flex flex-col gap-3">
            <label for="cota_tapa" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Cota de la Tapa (m)</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">height</span>
              <input 
                id="cota_tapa" 
                v-model.number="inspeccionStore.inspeccionActual.cota_tapa"
                type="number" 
                step="0.01"
                placeholder="0.00"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
              />
            </div>
          </div>

          <!-- Forma de la Tapa -->
          <div class="flex flex-col gap-3">
            <label for="tapa_forma" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Forma de la Tapa</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">category</span>
              <select 
                id="tapa_forma" 
                v-model="inspeccionStore.inspeccionActual.tapa_forma"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-10 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none appearance-none"
              >
                <option value="" disabled selected>Seleccione forma...</option>
                <option value="Circular">Circular</option>
                <option value="Cuadrada">Cuadrada</option>
                <option value="Rectangular">Rectangular</option>
                <option value="Triangular">Triangular (Válvulas)</option>
              </select>
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">expand_more</span>
            </div>
          </div>

          <!-- Dimensiones dinámicas de la tapa -->
          <div class="grid grid-cols-2 gap-4 md:col-span-2">
            <div v-if="inspeccionStore.inspeccionActual.tapa_forma === 'Circular'" class="col-span-2">
              <div class="flex flex-col gap-3">
                <label for="tapa_diametro" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Diámetro Tapa (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">adjust</span>
                  <input 
                    id="tapa_diametro" 
                    v-model.number="inspeccionStore.inspeccionActual.tapa_diametro_mm"
                    type="number" 
                    placeholder="600"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
            </div>
            <template v-else-if="inspeccionStore.inspeccionActual.tapa_forma !== ''">
              <div class="flex flex-col gap-3">
                <label for="tapa_largo" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Largo Tapa (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">straighten</span>
                  <input 
                    id="tapa_largo" 
                    v-model.number="inspeccionStore.inspeccionActual.tapa_largo_mm"
                    type="number" 
                    placeholder="600"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <label for="tapa_ancho" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Ancho Tapa (mm)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">straighten</span>
                  <input 
                    id="tapa_ancho" 
                    v-model.number="inspeccionStore.inspeccionActual.tapa_ancho_mm"
                    type="number" 
                    placeholder="600"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none"
                  />
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Section: Material y Tipo -->
      <div class="space-y-8">
        <div class="flex items-center gap-4">
          <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Material y Seguridad</h3>
          <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Material de la Tapa -->
          <div class="flex flex-col gap-3">
            <label for="tapa_material" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Material de la Tapa</label>
            <div class="relative group">
              <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue z-10">layers</span>
              <select 
                id="tapa_material" 
                v-model="inspeccionStore.inspeccionActual.tapa_material"
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-10 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none appearance-none"
              >
                <option value="" disabled selected>Seleccione material...</option>
                <option value="Fundición Dúctil">Fundición Dúctil</option>
                <option value="Fundición Gris">Fundición Gris</option>
                <option value="Acero Galvanizado">Acero Galvanizado</option>
                <option value="PRFV / Composite">PRFV / Composite</option>
                <option value="Hormigón">Hormigón</option>
              </select>
              <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">expand_more</span>
            </div>
          </div>

          <!-- Tipo de Tapa -->
          <div class="flex flex-col gap-4">
            <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Tipo de Cierre</label>
            <div class="flex p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
              <button 
                v-for="opt in ['Estanca', 'Ventilada', 'Ciega', 'Abatible']" 
                :key="opt"
                @click="inspeccionStore.inspeccionActual.tapa_tipo = opt"
                :class="inspeccionStore.inspeccionActual.tapa_tipo === opt 
                  ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg' 
                  : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all"
              >
                {{ opt }}
              </button>
            </div>
          </div>
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

// Limpiar dimensiones cuando se cambia la forma de la tapa
watch(() => inspeccionStore.inspeccionActual.tapa_forma, (newForma) => {
  if (newForma === 'Circular') {
    inspeccionStore.inspeccionActual.tapa_largo_mm = null;
    inspeccionStore.inspeccionActual.tapa_ancho_mm = null;
  } else {
    inspeccionStore.inspeccionActual.tapa_diametro_mm = null;
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
