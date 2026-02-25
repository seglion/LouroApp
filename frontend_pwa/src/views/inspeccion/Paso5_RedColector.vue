<template>
  <div class="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 p-6 md:p-10 space-y-10 max-w-[1024px] mx-auto w-full">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Red y Colector</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Configuración de conectividad y características técnicas</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
        <!-- Left Column: Conectividad de Red -->
        <div class="space-y-10">
          <div class="space-y-8">
            <div class="flex items-center gap-4">
              <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Conectividad de Red</h3>
              <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
            </div>
            
            <!-- Origen y Destino -->
            <div class="grid grid-cols-2 gap-6">
              <div class="flex flex-col gap-3">
                <label for="red_viene_de" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Viene de Pozo (ID)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">login</span>
                  <input 
                    id="red_viene_de" 
                    v-model="inspeccionStore.inspeccionActual.red_viene_de_pozo"
                    type="text" 
                    placeholder="P-XXXX"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none uppercase"
                  />
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <label for="red_va_a" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Va a Pozo (ID)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">logout</span>
                  <input 
                    id="red_va_a" 
                    v-model="inspeccionStore.inspeccionActual.red_va_a_pozo"
                    type="text" 
                    placeholder="P-YYYY"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none uppercase"
                  />
                </div>
              </div>
            </div>

            <!-- Tipo de Red -->
            <div class="flex flex-col gap-4">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Tipo de Red</label>
              <div class="flex p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                <button 
                  v-for="opt in ['Unitario', 'Pluvial', 'Residual']" 
                  :key="opt"
                  @click="inspeccionStore.inspeccionActual.red_tipo = opt"
                  :class="inspeccionStore.inspeccionActual.red_tipo === opt 
                    ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg' 
                    : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                  class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all"
                >
                  {{ opt }}
                </button>
              </div>
            </div>

            <!-- Carga de Red -->
            <div class="flex flex-col gap-4">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Nivel de Carga</label>
              <div class="flex p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                <button 
                  v-for="opt in ['Baja', 'Media', 'Alta']" 
                  :key="opt"
                  @click="inspeccionStore.inspeccionActual.red_carga = opt"
                  :class="inspeccionStore.inspeccionActual.red_carga === opt 
                    ? (opt === 'Alta' ? 'bg-red-500 text-white shadow-lg' : (opt === 'Media' ? 'bg-amber-500 text-white shadow-lg' : 'bg-green-500 text-white shadow-lg'))
                    : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                  class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all"
                >
                  {{ opt }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Detalles de los Colectores -->
        <div class="space-y-10">
          <div class="flex items-center gap-4">
            <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Características de los Colectores</h3>
            <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
          </div>
          
          <div class="space-y-8">
            <!-- Colector Entrada -->
            <div class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
              <div class="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-xl bg-green-500/10 flex items-center justify-center">
                  <span class="material-symbols-outlined text-green-600">login</span>
                </div>
                <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Entrada</span>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="flex flex-col gap-3">
                  <label for="mat_entrada" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Material</label>
                  <select 
                    id="mat_entrada" 
                    v-model="inspeccionStore.inspeccionActual.colector_mat_entrada"
                    class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none appearance-none"
                  >
                    <option value="" disabled>Seleccione...</option>
                    <option v-for="m in ['Hormigón', 'Gres', 'PVC', 'PEAD', 'Fundición', 'Fibrocemento']" :key="m" :value="m">{{ m }}</option>
                  </select>
                </div>
                <div class="flex flex-col gap-3">
                  <label for="diam_entrada" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Diámetro (mm)</label>
                  <input 
                    id="diam_entrada" 
                    v-model.number="inspeccionStore.inspeccionActual.colector_diametro_entrada_mm"
                    type="number" 
                    placeholder="DN"
                    class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none"
                  />
                </div>
              </div>
            </div>

            <!-- Colector Salida -->
            <div class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
              <div class="absolute top-0 left-0 w-1 h-full bg-accent-blue"></div>
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
                  <span class="material-symbols-outlined text-accent-blue">logout</span>
                </div>
                <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Salida</span>
              </div>

              <div class="grid grid-cols-2 gap-6">
                <div class="flex flex-col gap-3">
                  <label for="mat_salida" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Material</label>
                  <select 
                    id="mat_salida" 
                    v-model="inspeccionStore.inspeccionActual.colector_mat_salida"
                    class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none appearance-none"
                  >
                    <option value="" disabled>Seleccione...</option>
                    <option v-for="m in ['Hormigón', 'Gres', 'PVC', 'PEAD', 'Fundición', 'Fibrocemento']" :key="m" :value="m">{{ m }}</option>
                  </select>
                </div>
                <div class="flex flex-col gap-3">
                  <label for="diam_salida" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Diámetro (mm)</label>
                  <input 
                    id="diam_salida" 
                    v-model.number="inspeccionStore.inspeccionActual.colector_diametro_salida_mm"
                    type="number" 
                    placeholder="DN"
                    class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none"
                  />
                </div>
              </div>
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
import { useInspeccionStore } from '@/store/inspeccion';

const inspeccionStore = useInspeccionStore();
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
