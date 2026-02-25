<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="max-w-[1024px] mx-auto w-full min-h-screen flex flex-col bg-white dark:bg-slate-950 shadow-2xl relative">
      
      <!-- Header / Status Bar Area -->
      <header class="sticky top-0 z-10 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
        <div class="flex items-center p-6 justify-between">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900 text-white shadow-lg">
              <span class="material-symbols-outlined text-2xl">history</span>
            </div>
            <div>
              <h1 class="text-xl font-black tracking-tight uppercase">Historial</h1>
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">Todos los registros locales</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div class="h-11 w-11 rounded-xl bg-slate-200 dark:bg-slate-700 overflow-hidden border border-white dark:border-slate-800">
              <img :src="avatarUrl" :alt="nombreTecnico" />
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content Area -->
      <main class="flex-1 p-6 md:p-10 space-y-8 overflow-y-auto">
        
        <div class="space-y-6">
          <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
            <h3 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Total Inspecciones: {{ todasLasInspecciones.length }}</h3>
          </div>

          <div class="space-y-4">
            <div v-if="todasLasInspecciones.length === 0" class="py-12 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl flex flex-col items-center justify-center text-slate-400 space-y-2">
              <span class="material-symbols-outlined text-4xl opacity-20">inventory_2</span>
              <span class="text-[10px] font-black uppercase tracking-[0.1em]">Sin registros</span>
            </div>

            <div 
              v-for="item in todasLasInspecciones" 
              :key="item.id"
              class="group flex items-center gap-4 bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 shadow-sm hover:border-accent-blue/30 transition-all"
            >
              <div :class="getStatusColor(item)" class="h-12 w-12 shrink-0 flex items-center justify-center rounded-xl transition-colors">
                <span class="material-symbols-outlined text-2xl">{{ getStatusIcon(item) }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <p class="text-sm font-black text-slate-900 dark:text-white truncate uppercase tracking-tight">{{ item.id_pozo || 'Pozo sin ID' }}</p>
                  <span v-if="item.sync_status === 'pending' && item.finalizada" class="px-1.5 py-0.5 rounded-md bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400 text-[8px] font-black uppercase tracking-widest">Listo</span>
                  <span v-else-if="item.sync_status === 'pending' && !item.finalizada" class="px-1.5 py-0.5 rounded-md bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400 text-[8px] font-black uppercase tracking-widest">Borrador</span>
                  <span v-else-if="item.sync_status === 'error'" class="px-1.5 py-0.5 rounded-md bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400 text-[8px] font-black uppercase tracking-widest">Error</span>
                </div>
                <p class="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-0.5">{{ formatFecha(item.last_modified) }}</p>
              </div>
              
              <!-- Acciones solo para registros no sincronizados -->
              <div v-if="item.sync_status !== 'synced'" class="flex items-center gap-1">
                <!-- Estado Normal -->
                <template v-if="idAEliminar !== item.id">
                  <button
                    @click.stop.prevent="editarInspeccion(item.id)"
                    class="h-9 w-9 flex items-center justify-center rounded-lg hover:bg-accent-blue/10 text-slate-400 hover:text-accent-blue transition-colors"
                    title="Editar"
                  >
                    <span class="material-symbols-outlined text-xl">edit</span>
                  </button>
                  <button
                    @click.stop.prevent="idAEliminar = item.id"
                    class="h-9 w-9 flex items-center justify-center rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-400 hover:text-red-500 transition-colors"
                    title="Eliminar"
                  >
                    <span class="material-symbols-outlined text-xl">delete</span>
                  </button>
                </template>
                
                <!-- Estado de Confirmación -->
                <template v-else>
                  <button
                    @click.stop.prevent="idAEliminar = null"
                    class="h-8 px-3 flex items-center justify-center rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-300 transition-colors text-[10px] font-black uppercase tracking-widest"
                  >
                    Cancelar
                  </button>
                  <button
                    @click.stop.prevent="ejecutarEliminar()"
                    class="h-8 px-3 flex items-center justify-center rounded-lg bg-red-100 hover:bg-red-200 text-red-600 dark:bg-red-900/40 dark:hover:bg-red-900/60 dark:text-red-400 transition-colors text-[10px] font-black uppercase tracking-widest"
                  >
                    Sí, Borrar
                  </button>
                </template>
              </div>
              <!-- Badge sincronizado -->
              <div v-else class="h-8 px-3 flex items-center justify-center rounded-lg bg-emerald-50 dark:bg-emerald-900/20">
                <span class="text-[9px] font-black uppercase tracking-widest text-emerald-600">Sync</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- Navigation Bar -->
      <nav class="sticky bottom-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 pb-8 pt-4 px-6 z-20">
        <div class="flex max-w-md mx-auto items-center justify-around">
          <button 
            v-for="link in navLinks" 
            :key="link.label" 
            @click="!link.disabled && router.push(link.route)" 
            class="flex flex-col items-center gap-1 group relative"
            :class="{ 'opacity-40 cursor-not-allowed': link.disabled }"
          >
            <div :class="route.path === link.route ? 'bg-slate-900 text-white shadow-lg' : 'text-slate-400 ' + (!link.disabled ? 'hover:text-slate-900' : '')" class="h-10 w-14 flex items-center justify-center rounded-xl transition-all">
              <span class="material-symbols-outlined" :class="{ 'fill-1': route.path === link.route }">{{ link.icon }}</span>
            </div>
            <span :class="route.path === link.route ? 'text-slate-900 font-black' : 'text-slate-400 font-bold'" class="text-[9px] uppercase tracking-widest">{{ link.label }}</span>
          </button>
        </div>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useInspeccionStore } from '@/store/inspeccion';
import { db, type InspeccionLocal } from '@/db/db';

const router = useRouter();
const route = useRoute();
const inspeccionStore = useInspeccionStore();

// Decodificación ligera del JWT (sin verificación de firma, solo lectura del payload)
const getJwtPayload = (): Record<string, any> | null => {
  const token = localStorage.getItem('token');
  if (!token) return null;
  try {
    const part = token.split('.')[1];
    const base64 = (part ?? '').replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(atob(base64));
  } catch {
    return null;
  }
};

const jwtPayload = getJwtPayload();
const nombreTecnico = computed(() => {
  const fullName = jwtPayload?.full_name as string | undefined;
  if (fullName) return fullName.split(' ')[0];
  const email = jwtPayload?.email as string | undefined;
  return email ? email.split('@')[0] : 'Inspector';
});

const avatarUrl = computed(() => {
  const name = encodeURIComponent(jwtPayload?.full_name ?? 'Inspector');
  return `https://ui-avatars.com/api/?name=${name}&background=363842&color=fff`;
});

const todasLasInspecciones = ref<InspeccionLocal[]>([]);

const navLinks = ref([
  { label: 'Home', icon: 'home', route: '/', disabled: false },
  { label: 'Mapa', icon: 'map', route: '/mapa', disabled: true },
  { label: 'Historial', icon: 'history', route: '/historial', disabled: false },
  { label: 'Config', icon: 'settings', route: '/configuracion', disabled: true },
]);

const cargarDatos = async () => {
    // Obtener todas las inspecciones iterables localmente ordenadas por fecha más reciente
    todasLasInspecciones.value = await db.inspecciones
        .orderBy('last_modified')
        .reverse()
        .toArray();
};

onMounted(() => {
    cargarDatos();
});

const idAEliminar = ref<string | null>(null);

const ejecutarEliminar = async () => {
  if (!idAEliminar.value) return;
  try {
    await db.inspecciones.delete(idAEliminar.value);
    await cargarDatos();
  } catch (err) {
    console.error('Error al eliminar inspección:', err);
  } finally {
    idAEliminar.value = null;
  }
};

const editarInspeccion = async (id: string) => {
  await inspeccionStore.cargarInspeccionExistente(id);
  router.push('/nueva-inspeccion');
};

const formatFecha = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const getStatusIcon = (item: InspeccionLocal) => {
    if (item.sync_status === 'synced') return 'cloud_done';
    if (item.sync_status === 'error') return 'sync_problem';
    if (item.sync_status === 'pending' && item.finalizada) return 'check_circle'; // Listo para sync
    if (item.sync_status === 'pending' && !item.finalizada) return 'edit_document'; // Borrador inacabado
    return 'help';
};

const getStatusColor = (item: InspeccionLocal) => {
    if (item.sync_status === 'synced') return 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30';
    if (item.sync_status === 'error') return 'bg-red-100 text-red-600 dark:bg-red-900/30';
    if (item.sync_status === 'pending' && item.finalizada) return 'bg-blue-100 text-blue-600 dark:bg-blue-900/30'; // Listo para sync
    if (item.sync_status === 'pending' && !item.finalizada) return 'bg-amber-100 text-amber-600 dark:bg-amber-900/30'; // Borrador inacabado
    return 'bg-slate-100 text-slate-400';
};
</script>
