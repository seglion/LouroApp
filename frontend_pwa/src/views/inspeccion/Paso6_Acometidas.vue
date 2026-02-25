<template>
  <div class="flex flex-col min-h-full bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 p-6 md:p-10 space-y-10 max-w-[1024px] mx-auto w-full">
      
      <!-- Section Header -->
      <div class="space-y-2 border-b border-slate-200 dark:border-slate-800 pb-6">
        <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">Acometidas</h2>
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Registro de conexiones domiciliarias al pozo</p>
      </div>

      <div class="space-y-8">
        <!-- Add Button -->
        <button 
          @click="anyadirAcometida"
          class="w-full py-6 bg-white dark:bg-slate-900 border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-3xl flex items-center justify-center gap-4 text-slate-500 hover:border-accent-blue hover:text-accent-blue hover:bg-accent-blue/5 transition-all group shadow-sm"
        >
          <span class="material-symbols-outlined text-3xl group-hover:rotate-90 transition-transform">add_circle</span>
          <span class="text-xs font-black uppercase tracking-[0.2em]">Añadir Nueva Acometida</span>
        </button>

        <!-- Empty State -->
        <div v-if="acometidas.length === 0" class="py-20 flex flex-col items-center justify-center text-slate-400 gap-6 bg-white/50 dark:bg-slate-900/50 rounded-3xl border border-slate-200/50 dark:border-slate-800/50">
          <div class="h-20 w-20 rounded-full bg-slate-200/50 dark:bg-slate-800/50 flex items-center justify-center">
            <span class="material-symbols-outlined text-5xl opacity-30">home_repair_service</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-[0.3em] opacity-40">Sin acometidas registradas</p>
        </div>

        <!-- Acometidas List -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          <div 
            v-for="(ac, index) in acometidas" 
            :key="ac.id"
            class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col group transition-all hover:shadow-md h-full"
          >
            <!-- Card Header -->
            <div class="flex items-center justify-between px-6 py-4 bg-slate-50 dark:bg-slate-800/30 border-b border-slate-100 dark:border-slate-800">
              <div class="flex items-center gap-3">
                <span class="flex h-8 w-8 items-center justify-center bg-primary dark:bg-accent-blue text-white dark:text-primary rounded-xl text-[10px] font-black shadow-sm">
                  {{ index + 1 }}
                </span>
                <span class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Acometida Domiciliaria</span>
              </div>
              <button @click="eliminarAcometida(index)" class="h-8 w-8 flex items-center justify-center rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-500/10 transition-all">
                <span class="material-symbols-outlined text-[18px]">delete</span>
              </button>
            </div>

            <!-- Card Body -->
            <div class="p-6 space-y-6 flex-1">
              <div class="grid grid-cols-1 gap-6">
                <!-- Material -->
                <div class="flex flex-col gap-3">
                  <label class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Material de Conducto</label>
                  <div class="relative group">
                    <select 
                      v-model="ac.material"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none appearance-none transition-all"
                    >
                      <option value="PVC">PVC</option>
                      <option value="Gres">Gres</option>
                      <option value="Hormigón">Hormigón</option>
                      <option value="PEAD">PEAD</option>
                      <option value="Fibrocemento">Fibrocemento</option>
                    </select>
                    <span class="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-sm">expand_more</span>
                  </div>
                </div>

                <!-- Diámetro y Profundidad -->
                <div class="grid grid-cols-2 gap-4">
                  <div class="flex flex-col gap-3">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Diámetro (mm)</label>
                    <input 
                      v-model.number="ac.diametro_mm"
                      type="number"
                      placeholder="DN"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none transition-all"
                    />
                  </div>
                  <div class="flex flex-col gap-3">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Prof. (m)</label>
                    <input 
                      v-model.number="ac.profundidad_m"
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none transition-all"
                    />
                  </div>
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
import { computed } from 'vue';
import { useInspeccionStore } from '@/store/inspeccion';
import { v4 as uuidv4 } from 'uuid';

const inspeccionStore = useInspeccionStore();

const acometidas = computed(() => inspeccionStore.inspeccionActual.acometidas);

const anyadirAcometida = () => {
  const nuevaAcometida = {
    id: uuidv4(),
    numero_acometida: acometidas.value.length + 1,
    material: 'PVC',
    diametro_mm: 160,
    profundidad_m: 0.5
  };
  inspeccionStore.inspeccionActual.acometidas.push(nuevaAcometida);
};

const eliminarAcometida = (index: number) => {
  inspeccionStore.inspeccionActual.acometidas.splice(index, 1);
  // Re-numerar para mantener consistencia
  inspeccionStore.inspeccionActual.acometidas.forEach((ac, idx) => {
    ac.numero_acometida = idx + 1;
  });
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

select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}
</style>
