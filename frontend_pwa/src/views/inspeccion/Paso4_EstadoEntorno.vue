<template>
  <div class="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 p-6 md:p-10 space-y-10 max-w-[1024px] mx-auto w-full">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Estado y Entorno</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Evaluación de conservación y registro de evidencias</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
        <!-- Left Column: Evaluación Técnica -->
        <div class="space-y-10">
          <div class="space-y-8">
            <div class="flex items-center gap-4">
              <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Evaluación Técnica</h3>
              <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
            </div>
            
            <!-- Estado de Conservación -->
            <div class="flex flex-col gap-4">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Estado de Conservación</label>
              <div class="grid grid-cols-2 gap-3">
                <button 
                  v-for="opt in ['Bueno', 'Regular', 'Malo', 'Ruina']" 
                  :key="opt"
                  @click="inspeccionStore.inspeccionActual.estado = opt"
                  :class="inspeccionStore.inspeccionActual.estado === opt 
                    ? 'bg-primary dark:bg-accent-blue text-white dark:text-primary shadow-lg border-transparent' 
                    : 'bg-white dark:bg-slate-900 text-slate-500 border-slate-200 dark:border-slate-800 hover:border-slate-300'"
                  class="py-5 text-[10px] font-black uppercase tracking-widest rounded-2xl border transition-all active:scale-[0.98]"
                >
                  {{ opt }}
                </button>
              </div>
            </div>

            <!-- Limpieza -->
            <div class="flex flex-col gap-4">
              <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Nivel de Limpieza</label>
              <div class="flex p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                <button 
                  v-for="opt in ['Limpio', 'Sedimentos', 'Obstruido']" 
                  :key="opt"
                  @click="inspeccionStore.inspeccionActual.limpieza = opt"
                  :class="inspeccionStore.inspeccionActual.limpieza === opt 
                    ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg' 
                    : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                  class="flex-1 py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all"
                >
                  {{ opt }}
                </button>
              </div>
            </div>
          </div>

          <!-- Section: Observaciones -->
          <div class="space-y-6">
            <div class="flex items-center gap-4">
              <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Notas de Campo</h3>
              <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
            </div>
            <div class="relative group">
              <textarea 
                v-model="inspeccionStore.inspeccionActual.observaciones"
                placeholder="Describa cualquier incidencia o detalle relevante..."
                class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 text-slate-900 dark:text-white font-medium text-sm focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none min-h-[160px] resize-none shadow-sm"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Right Column: Registro Fotográfico -->
        <div class="space-y-8">
          <div class="flex items-center gap-4">
            <h3 class="text-xs font-black uppercase tracking-[0.2em] text-primary/50 dark:text-accent-blue/50">Evidencias Fotográficas</h3>
            <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
          </div>
          
          <div class="flex flex-col gap-8">
            <!-- Foto de Situación (Entorno) -->
            <div class="flex flex-col gap-3">
              <span class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Foto de Situación (Entorno)</span>
              <div 
                @click="capturarFoto('situacion')"
                class="relative aspect-video w-full rounded-3xl border-2 border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 flex flex-col items-center justify-center gap-4 cursor-pointer hover:border-accent-blue/40 transition-all group overflow-hidden shadow-sm"
              >
                <template v-if="inspeccionStore.fotosTemporales.situacion">
                  <img :src="inspeccionStore.fotosTemporales.situacion" class="absolute inset-0 w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
                    <span class="material-symbols-outlined text-white text-4xl">add_a_photo</span>
                  </div>
                </template>
                <template v-else>
                  <div class="h-16 w-16 rounded-full bg-slate-50 dark:bg-slate-800 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-slate-400 group-hover:text-accent-blue transition-colors text-3xl">add_a_photo</span>
                  </div>
                  <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Capturar Entorno</span>
                </template>
              </div>
            </div>

            <!-- Foto Interior -->
            <div class="flex flex-col gap-3">
              <span class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Inspección Visual Interior</span>
              <div 
                @click="capturarFoto('interior')"
                class="relative aspect-video w-full rounded-3xl border-2 border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 flex flex-col items-center justify-center gap-4 cursor-pointer hover:border-accent-blue/40 transition-all group overflow-hidden shadow-sm"
              >
                <template v-if="inspeccionStore.fotosTemporales.interior">
                  <img :src="inspeccionStore.fotosTemporales.interior" class="absolute inset-0 w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
                    <span class="material-symbols-outlined text-white text-4xl">add_a_photo</span>
                  </div>
                </template>
                <template v-else>
                  <div class="h-16 w-16 rounded-full bg-slate-50 dark:bg-slate-800 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span class="material-symbols-outlined text-slate-400 group-hover:text-accent-blue transition-colors text-3xl">videocam</span>
                  </div>
                  <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Capturar Interior</span>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Hidden Input for File Capture -->
      <input 
        type="file" 
        accept="image/*" 
        capture="environment" 
        class="hidden" 
        ref="fotoInput" 
        @change="handleFotoChange"
      />

      <!-- Placeholder spacing for navigation bar (Mobile only) -->
      <div class="h-24 md:hidden"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useInspeccionStore } from '@/store/inspeccion';

const inspeccionStore = useInspeccionStore();
// const router = useRouter(); // No Longer needed for navigation here
const fotoInput = ref<HTMLInputElement | null>(null);
const currentFotoType = ref<'situacion' | 'interior' | null>(null);

const capturarFoto = (type: 'situacion' | 'interior') => {
  currentFotoType.value = type;
  fotoInput.value?.click();
};

const handleFotoChange = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file && currentFotoType.value) {
    const url = URL.createObjectURL(file);
    inspeccionStore.fotosTemporales[currentFotoType.value] = url;
    
    // Guardar el Blob real para la persistencia offline e integración con Sync
    if (currentFotoType.value === 'situacion') {
      inspeccionStore.fotosTemporales.blob_situacion = file;
    } else {
      inspeccionStore.fotosTemporales.blob_interior = file;
    }

    // Disparar guardado inmediato para persistir el binario en IndexedDB
    await inspeccionStore.guardarEnDB();
  }
};
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
</style>
