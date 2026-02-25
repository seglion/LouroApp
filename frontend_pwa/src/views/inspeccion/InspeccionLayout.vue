<template>
  <div class="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="flex-1 flex flex-col max-w-[1024px] mx-auto w-full bg-white dark:bg-slate-950 shadow-2xl overflow-hidden relative">
      <!-- Header Multi-paso (Stationary) -->
      <header class="shrink-0 z-20 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div class="flex items-center justify-between p-4">
          <button @click="volverAlDashboard" class="p-2 -ml-2 text-slate-500 hover:text-primary transition-colors rounded-full">
            <span class="material-symbols-outlined">close</span>
          </button>
          <div class="flex flex-col items-center">
            <span class="text-xs font-bold uppercase tracking-widest text-primary/60">Paso {{ inspeccionStore.inspeccionActual.estado_paso }} de 6</span>
            <h1 class="text-base font-bold text-primary dark:text-white">{{ getTituloPaso }}</h1>
          </div>
          <div class="w-10"></div>
        </div>
        <!-- Barra Progreso -->
        <div class="h-1.5 w-full bg-slate-100 dark:bg-slate-800">
          <div 
            class="h-full bg-accent-blue transition-all duration-500 ease-out"
            :style="{ width: `${(inspeccionStore.inspeccionActual.estado_paso / 6) * 100}%` }"
          ></div>
        </div>
      </header>

      <!-- Contenedor Dinámico para cada Paso (Scrollable) -->
      <main class="flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-950 scroll-smooth relative">
        <router-view></router-view>
        <!-- Espaciador final -->
        <div class="h-8"></div>
      </main>

      <!-- Global Action Bar -->
      <footer class="shrink-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 p-4 pb-8">
        <div class="flex gap-3 max-w-[400px] mx-auto">
          <!-- Botón Atrás -->
          <button 
            v-if="inspeccionStore.inspeccionActual.estado_paso > 1"
            @click="retroceder" 
            class="h-14 w-14 flex items-center justify-center bg-slate-100 dark:bg-slate-800 rounded-xl text-slate-600 dark:text-slate-300 active:scale-95 transition-all"
          >
            <span class="material-symbols-outlined">arrow_back_ios_new</span>
          </button>

          <!-- Botón Siguiente / Finalizar -->
          <button 
            @click="avanzar" 
            :disabled="!inspeccionStore.pasoActualValido"
            :class="[
              'flex-1 h-14 flex items-center justify-between px-6 rounded-xl font-black uppercase tracking-widest transition-all active:scale-[0.98] group shadow-lg',
              inspeccionStore.inspeccionActual.estado_paso === 6 
                ? 'bg-green-600 dark:bg-green-500 text-white' 
                : 'bg-primary dark:bg-accent-blue text-white dark:text-primary disabled:opacity-50 disabled:grayscale'
            ]"
          >
            <div class="flex flex-col items-start gap-0.5 text-left">
              <span class="text-[10px] font-bold opacity-60">{{ inspeccionStore.inspeccionActual.estado_paso === 6 ? 'Finalizar' : 'Siguiente' }}</span>
              <span class="text-sm">{{ getLabelBotonSiguiente }}</span>
            </div>
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white/20 group-hover:bg-white/30 transition-colors">
              <span class="material-symbols-outlined">{{ inspeccionStore.inspeccionActual.estado_paso === 6 ? 'task_alt' : 'arrow_forward' }}</span>
            </div>
          </button>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useInspeccionStore } from '@/store/inspeccion';

const router = useRouter();
const route = useRoute();
const inspeccionStore = useInspeccionStore();

const titulos = [
    "Ubicación y General",
    "Detalles del Pozo",
    "Detalles de la Tapa",
    "Estado y Entorno",
    "Red y Colector",
    "Acometidas domiciliarias"
];

const labelsBotones = [
    "Ir a Detalles",
    "Ir a Tapa",
    "Ir a Estado",
    "Ir a Red",
    "Ir a Acometidas",
    "Completar Registro"
];

const sincronizarPaso = (routeName: string | symbol | null | undefined) => {
    if (!routeName) return;
    const stepMatch = String(routeName).match(/paso-(\d+)/);
    if (stepMatch && stepMatch[1]) {
        inspeccionStore.inspeccionActual.estado_paso = parseInt(stepMatch[1]);
    } else if (routeName === 'nueva_inspeccion' || routeName === 'inspeccion-paso-1') {
        inspeccionStore.inspeccionActual.estado_paso = 1;
    }
};

onMounted(async () => {
    if (!inspeccionStore.inspeccionActual.id) {
        const recuperado = await inspeccionStore.recuperarUltimoBorrador();
        if (recuperado) {
            sincronizarPaso(route.name);
            if (route.name === 'inspeccion-paso-1' && inspeccionStore.inspeccionActual.estado_paso > 1) {
                router.replace(`/nueva-inspeccion/paso-${inspeccionStore.inspeccionActual.estado_paso}`);
            }
        }
    }
});

watch(() => inspeccionStore.inspeccionActual, (newValue) => {
    if (!newValue.id) return;
    // Guardado automático debounced manejado por el store o aquí
    // Para simplificar, confiamos en el watch de route y cambios explícitos
}, { deep: true });

watch(() => route.name, async (newRouteName) => {
    sincronizarPaso(newRouteName);
    await inspeccionStore.guardarEnDB();
}, { immediate: true });

const volverAlDashboard = () => router.push('/');

const retroceder = () => {
    if (inspeccionStore.inspeccionActual.estado_paso > 1) {
        inspeccionStore.retrocederPaso();
        router.push(`/nueva-inspeccion/paso-${inspeccionStore.inspeccionActual.estado_paso}`);
    }
};

const avanzar = () => {
    if (inspeccionStore.inspeccionActual.estado_paso === 6) {
        finalizar();
    } else if (inspeccionStore.pasoActualValido) {
        inspeccionStore.avanzarPaso();
        router.push(`/nueva-inspeccion/paso-${inspeccionStore.inspeccionActual.estado_paso}`);
    }
};

const finalizar = async () => {
    console.log('Finalizando inspección...', inspeccionStore.inspeccionActual);
    inspeccionStore.inspeccionActual.finalizada = true;
    await inspeccionStore.guardarEnDB();
    router.push('/');
};

const getTituloPaso = computed(() => titulos[inspeccionStore.inspeccionActual.estado_paso - 1] || "Inspección");
const getLabelBotonSiguiente = computed(() => labelsBotones[inspeccionStore.inspeccionActual.estado_paso - 1] || "Continuar");
</script>
