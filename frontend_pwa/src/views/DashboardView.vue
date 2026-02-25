<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 font-display transition-colors duration-300">
    <div class="max-w-[1024px] mx-auto w-full min-h-screen flex flex-col bg-white dark:bg-slate-950 shadow-2xl relative">
      
      <!-- Header / Status Bar Area -->
      <header class="sticky top-0 z-10 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
        <div class="flex items-center p-6 justify-between">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900 text-white shadow-lg">
              <span class="material-symbols-outlined text-2xl">monitoring</span>
            </div>
            <div>
              <h1 class="text-xl font-black tracking-tight uppercase">Terminal de Inspección</h1>
              <div class="flex items-center gap-2">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-blue opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-accent-blue"></span>
                </span>
                <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">Sincronización Activa</span>
              </div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button @click="handleLogout" class="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-600 dark:text-slate-300 hover:text-red-600 transition-colors" title="Cerrar Sesión">
              <span class="material-symbols-outlined">logout</span>
            </button>
            <div class="h-11 w-11 rounded-xl bg-slate-200 dark:bg-slate-700 overflow-hidden border border-white dark:border-slate-800">
              <img :src="avatarUrl" :alt="nombreTecnico" />
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content Container -->
      <main class="flex-1 p-6 md:p-10 space-y-8">
        
        <!-- Welcome Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="md:col-span-2 space-y-2">
            <h2 class="text-3xl font-black tracking-tighter text-slate-900 dark:text-white uppercase">{{ saludo }}, {{ nombreTecnico }}</h2>
            <p class="text-slate-500 font-medium">Hay {{ totalPendientes }} registros esperando ser subidos al servidor central.</p>
          </div>
          <div v-if="totalPendientes > 0" class="flex items-center gap-4 bg-slate-900 text-white p-6 rounded-2xl shadow-xl border-l-4 border-accent-blue">
            <span class="material-symbols-outlined text-accent-blue text-4xl">cloud_upload</span>
            <div class="flex-1">
              <p class="text-sm font-black uppercase tracking-widest">Pendientes</p>
              <p class="text-2xl font-black tracking-tighter">{{ totalPendientes }}</p>
            </div>
          </div>
        </div>

        <!-- Grid Layout for Actions and Activity -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8">
          
          <!-- Left Column: Actions -->
          <div class="md:col-span-7 space-y-6">
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
              <h3 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Panel de Control</h3>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <!-- Nueva Inspección (Big Card) -->
              <button 
                @click="iniciarInspeccion" 
                class="sm:col-span-2 group relative flex flex-col justify-between h-56 rounded-3xl bg-slate-900 p-8 text-white shadow-2xl overflow-hidden active:scale-[0.99] transition-all hover:ring-4 hover:ring-accent-blue/20"
              >
                <div class="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform">
                  <span class="material-symbols-outlined text-9xl">add_circle</span>
                </div>
                <div class="bg-accent-blue p-3 rounded-xl w-fit text-slate-900">
                  <span class="material-symbols-outlined text-2xl font-bold">add</span>
                </div>
                <div class="space-y-1">
                  <span class="block text-3xl font-black tracking-tighter uppercase">Nueva Inspección</span>
                  <span class="text-slate-400 font-medium">Registro técnico de red y activos</span>
                </div>
              </button>

              <!-- Sync Action -->
              <button 
                @click="ejecutarSync"
                :disabled="sincronizando"
                class="sm:col-span-2 flex flex-col justify-between h-48 rounded-3xl bg-white dark:bg-slate-800 p-6 border border-slate-200 dark:border-slate-700 shadow-sm active:scale-[0.97] transition-all hover:border-accent-blue group"
              >
                <div :class="{ 'animate-spin': sincronizando }" class="h-12 w-12 rounded-2xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-slate-900 dark:text-white group-hover:bg-accent-blue group-hover:text-slate-900 transition-colors">
                  <span class="material-symbols-outlined">sync</span>
                </div>
                <div>
                  <span class="block text-xl font-black tracking-tight uppercase">{{ sincronizando ? 'Sincronizando' : 'Sincronizar' }}</span>
                  <span class="text-sm text-slate-500 font-medium">Enviar datos a la central</span>
                </div>
              </button>
            </div>
          </div>

          <!-- Right Column: Recent Activity -->
          <div class="md:col-span-5 space-y-6">
            <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2">
              <h3 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Actividad Reciente</h3>
              <button class="text-slate-900 dark:text-white text-[10px] font-black uppercase tracking-widest hover:text-accent-blue transition-colors">Historial Completo</button>
            </div>

            <div class="space-y-4">
              <div v-if="inspeccionesRecientes.length === 0" class="py-12 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl flex flex-col items-center justify-center text-slate-400 space-y-2">
                <span class="material-symbols-outlined text-4xl opacity-20">inventory_2</span>
                <span class="text-[10px] font-black uppercase tracking-[0.1em]">Sin actividad registrada</span>
              </div>

              <div 
                v-for="item in inspeccionesRecientes" 
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
import { syncService } from '@/services/sync';

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

const saludo = computed(() => {
  const h = new Date().getHours();
  if (h >= 6 && h < 14) return 'Buenos días';
  if (h >= 14 && h < 21) return 'Buenas tardes';
  return 'Buenas noches';
});

const avatarUrl = computed(() => {
  const name = encodeURIComponent(jwtPayload?.full_name ?? 'Inspector');
  return `https://ui-avatars.com/api/?name=${name}&background=363842&color=fff`;
});

const inspeccionesRecientes = ref<InspeccionLocal[]>([]);
const totalPendientes = ref(0);
const sincronizando = ref(false);

const navLinks = ref([
  { label: 'Home', icon: 'home', route: '/', disabled: false },
  { label: 'Mapa', icon: 'map', route: '/mapa', disabled: true },
  { label: 'Historial', icon: 'history', route: '/historial', disabled: false },
  { label: 'Config', icon: 'settings', route: '/configuracion', disabled: true },
]);

const cargarDatos = async () => {
    // Obtener las últimas 5 inspecciones para el historial
    inspeccionesRecientes.value = await db.inspecciones
        .orderBy('last_modified')
        .reverse()
        .limit(5)
        .toArray();
    
    // Contar pendientes finalizados (pending + error = reintentables)
    const pendientes = await db.inspecciones
        .filter(i => i.finalizada === true && (i.sync_status === 'pending' || i.sync_status === 'error'))
        .toArray();
    
    totalPendientes.value = pendientes.length;
};

onMounted(() => {
    cargarDatos();
});

const iniciarInspeccion = async () => {
  await inspeccionStore.iniciarNuevaInspeccion();
  router.push('/nueva-inspeccion');
};

const ejecutarSync = async () => {
    if (sincronizando.value) return;
    sincronizando.value = true;
    try {
        await syncService.startSync();
        await cargarDatos(); // Recargar tras sync
    } finally {
        sincronizando.value = false;
    }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

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
