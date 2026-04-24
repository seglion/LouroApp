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
            
            <!-- Origen y Destino 1 -->
            <div class="grid grid-cols-2 gap-6">
              <div class="flex flex-col gap-3">
                <label for="red_viene_de" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Viene de Pozo (ID)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">login</span>
                  <input 
                    id="red_viene_de" 
                    v-model="inspeccionStore.inspeccionActual.red_viene_de_pozo"
                    type="text" 
                    placeholder="P-0000"
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
                    placeholder="P-0000"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none uppercase"
                  />
                </div>
              </div>
            </div>

            <!-- Origen y Destino 2 -->
            <div v-if="inspeccionStore.inspeccionActual.red_viene_de_pozo_2 || inspeccionStore.inspeccionActual.red_va_a_pozo_2 || modoSeleccion === 'desde2' || modoSeleccion === 'hacia2'"
                 class="grid grid-cols-2 gap-6 pt-4 border-t border-slate-200 dark:border-slate-800 border-dashed animate-in fade-in"
            >
              <div class="flex flex-col gap-3">
                <label for="red_viene_de_2" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Viene de Pozo 2 (ID)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">login</span>
                  <input 
                    id="red_viene_de_2" 
                    v-model="inspeccionStore.inspeccionActual.red_viene_de_pozo_2"
                    type="text" 
                    placeholder="P-XXXX"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none uppercase"
                  />
                </div>
              </div>
              <div class="flex flex-col gap-3">
                <label for="red_va_a_2" class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Va a Pozo 2 (ID)</label>
                <div class="relative group">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-accent-blue transition-colors z-10">logout</span>
                  <input 
                    id="red_va_a_2" 
                    v-model="inspeccionStore.inspeccionActual.red_va_a_pozo_2"
                    type="text" 
                    placeholder="P-YYYY"
                    class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl h-16 pl-14 pr-4 text-slate-900 dark:text-white font-black tracking-tight focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue transition-all outline-none uppercase"
                  />
                </div>
              </div>
            </div>

            <!-- Mapa de Conectividad Interactiva -->
            <div class="space-y-4">
              <div class="flex flex-col gap-4">
                <div class="flex items-center justify-between">
                  <label class="text-[10px] font-black uppercase tracking-[0.2em] text-primary dark:text-accent-blue">Mapa de Conectividad</label>
                  <div class="flex flex-wrap gap-2 justify-end">
                    <button 
                      @click="modoSeleccion = 'desde'"
                      :class="modoSeleccion === 'desde' ? 'bg-green-600 text-white shadow-lg scale-105' : 'bg-slate-200 dark:bg-slate-800 text-slate-500 hover:bg-slate-300 dark:hover:bg-slate-700'"
                      class="px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-xs">login</span> Org1
                    </button>
                    <button 
                      @click="modoSeleccion = 'hacia'"
                      :class="modoSeleccion === 'hacia' ? 'bg-accent-blue text-white shadow-lg scale-105' : 'bg-slate-200 dark:bg-slate-800 text-slate-500 hover:bg-slate-300 dark:hover:bg-slate-700'"
                      class="px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-xs">logout</span> Dest1
                    </button>
                    <button 
                      @click="modoSeleccion = 'desde2'"
                      :class="modoSeleccion === 'desde2' ? 'bg-emerald-600 text-white shadow-lg scale-105' : 'bg-slate-200 dark:bg-slate-800 text-slate-500 hover:bg-slate-300 dark:hover:bg-slate-700'"
                      class="px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-xs">login</span> Org2
                    </button>
                    <button 
                      @click="modoSeleccion = 'hacia2'"
                      :class="modoSeleccion === 'hacia2' ? 'bg-indigo-600 text-white shadow-lg scale-105' : 'bg-slate-200 dark:bg-slate-800 text-slate-500 hover:bg-slate-300 dark:hover:bg-slate-700'"
                      class="px-3 py-1.5 rounded-lg text-[8px] font-black uppercase tracking-widest transition-all flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-xs">logout</span> Dest2
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="relative group">
                <div v-if="!inspeccionStore.inspeccionActual.coordenadas_utm.x" class="absolute inset-0 bg-slate-200 dark:bg-slate-800 rounded-2xl flex flex-col items-center justify-center gap-2 z-10 p-6 text-center">
                  <span class="material-symbols-outlined text-4xl text-slate-400 animate-pulse">location_off</span>
                  <p class="text-[10px] font-black uppercase tracking-widest text-slate-500">Ubicación no disponible</p>
                  <p class="text-[8px] font-medium text-slate-400">Capture la ubicación en el Paso 1 para habilitar el mapa de red.</p>
                </div>
                <div id="map-connectivity" class="w-full h-[240px] min-h-[240px] rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-inner z-0 bg-slate-100 dark:bg-slate-900 transition-opacity" :class="!inspeccionStore.inspeccionActual.coordenadas_utm.x ? 'opacity-20' : 'opacity-100'"></div>
                <!-- Overlay de modo -->
                <div v-if="modoSeleccion" class="absolute top-4 left-1/2 -translate-x-1/2 px-4 py-2 bg-white/90 dark:bg-slate-900/90 backdrop-blur border border-slate-200 dark:border-slate-800 rounded-full shadow-2xl z-[1000] pointer-events-none animate-bounce flex items-center gap-2">
                  <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" :class="modoSeleccion.includes('desde') ? 'bg-green-400' : 'bg-accent-blue'"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2" :class="modoSeleccion.includes('desde') ? 'bg-green-500' : 'bg-accent-blue'"></span>
                  </span>
                  <span class="text-[9px] font-black uppercase tracking-widest" :class="modoSeleccion.includes('desde') ? 'text-green-600' : 'text-accent-blue'">
                    Clic en pozo para: {{ modoSeleccion.includes('desde') ? (modoSeleccion === 'desde' ? 'ORIGEN 1' : 'ORIGEN 2') : (modoSeleccion === 'hacia' ? 'DESTINO 1' : 'DESTINO 2') }}
                  </span>
                </div>
              </div>

              <!-- Indicador de sentido -->
              <div class="flex flex-col gap-2">
                <div v-if="inspeccionStore.inspeccionActual.red_viene_de_pozo || inspeccionStore.inspeccionActual.red_va_a_pozo" 
                    class="flex items-center justify-center gap-4 py-2 bg-slate-100 dark:bg-slate-900/50 rounded-xl border border-dashed border-slate-200 dark:border-slate-800">
                  <span class="text-[10px] font-mono font-bold text-slate-500">{{ inspeccionStore.inspeccionActual.red_viene_de_pozo || '?' }}</span>
                  <span class="material-symbols-outlined text-slate-400 text-sm">trending_flat</span>
                  <span class="text-[10px] font-mono font-bold text-slate-500">{{ inspeccionStore.inspeccionActual.red_va_a_pozo || '?' }}</span>
                </div>
                <div v-if="inspeccionStore.inspeccionActual.red_viene_de_pozo_2 || inspeccionStore.inspeccionActual.red_va_a_pozo_2" 
                    class="flex items-center justify-center gap-4 py-2 bg-slate-100 dark:bg-slate-900/50 rounded-xl border border-dashed border-slate-200 dark:border-slate-800">
                  <span class="text-[10px] font-mono font-bold text-slate-500">{{ inspeccionStore.inspeccionActual.red_viene_de_pozo_2 || '?' }}</span>
                  <span class="material-symbols-outlined text-slate-400 text-sm">trending_flat</span>
                  <span class="text-[10px] font-mono font-bold text-slate-500">{{ inspeccionStore.inspeccionActual.red_va_a_pozo_2 || '?' }}</span>
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
            <!-- Grupo 1 (Siempre Visible) -->
            <div class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <!-- Colector Entrada 1 -->
              <div class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-xl bg-green-500/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-green-600">login</span>
                  </div>
                  <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Entrada 1</span>
                </div>

                <div class="grid grid-cols-2 gap-6">
                  <div class="flex flex-col gap-3 col-span-2">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Material Entrada</label>
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                      <button 
                        v-for="m in materialesList" 
                        :key="m.id"
                        @click="inspeccionStore.inspeccionActual.colector_mat_entrada = m.id"
                        :class="inspeccionStore.inspeccionActual.colector_mat_entrada === m.id 
                          ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg scale-[1.02]' 
                          : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                        class="py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all flex items-center justify-center"
                      >
                        {{ m.label }}
                      </button>
                    </div>
                  </div>
                  <div class="flex flex-col gap-3 col-span-2">
                    <label for="diam_entrada" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Diámetro Entrada (mm)</label>
                    <input 
                      id="diam_entrada" 
                      v-model.number="inspeccionStore.inspeccionActual.colector_diametro_entrada_mm"
                      type="number" 
                      placeholder="Ej. 300"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none"
                    />
                  </div>
                </div>
              </div>

              <!-- Colector Salida 1 -->
              <div class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-accent-blue"></div>
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-xl bg-accent-blue/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-accent-blue">logout</span>
                  </div>
                  <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Salida 1</span>
                </div>

                <div class="grid grid-cols-2 gap-6">
                  <div class="flex flex-col gap-3 col-span-2">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Material Salida</label>
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                      <button 
                        v-for="m in materialesList" 
                        :key="m.id"
                        @click="inspeccionStore.inspeccionActual.colector_mat_salida = m.id"
                        :class="inspeccionStore.inspeccionActual.colector_mat_salida === m.id 
                          ? 'bg-white dark:bg-slate-700 text-primary dark:text-white shadow-lg scale-[1.02]' 
                          : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                        class="py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all flex items-center justify-center"
                      >
                        {{ m.label }}
                      </button>
                    </div>
                  </div>
                  <div class="flex flex-col gap-3 col-span-2">
                    <label for="diam_salida" class="text-[10px] font-black uppercase tracking-[0.1em] text-slate-400">Diámetro Salida (mm)</label>
                    <input 
                      id="diam_salida" 
                      v-model.number="inspeccionStore.inspeccionActual.colector_diametro_salida_mm"
                      type="number" 
                      placeholder="Ej. 300"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-accent-blue/10 focus:border-accent-blue outline-none"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Grupo 2 (Condicional) -->
            <div v-if="inspeccionStore.inspeccionActual.red_viene_de_pozo_2 || inspeccionStore.inspeccionActual.red_va_a_pozo_2" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300 pt-4 border-t border-slate-200 dark:border-slate-800 border-dashed">
              <div class="flex items-center gap-4">
                <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-500">Conductos Secundarios</h3>
                <div class="flex-1 h-px bg-slate-200 dark:border-slate-800"></div>
              </div>

              <!-- Colector Entrada 2 (Solo si hay ID) -->
              <div v-if="inspeccionStore.inspeccionActual.red_viene_de_pozo_2" class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-emerald-600">login</span>
                  </div>
                  <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Entrada 2</span>
                </div>

                <div class="grid grid-cols-2 gap-6">
                  <div class="flex flex-col gap-3 col-span-2">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-emerald-500/70">Material Entrada 2</label>
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                      <button 
                        v-for="m in materialesList" 
                        :key="m.id"
                        @click="inspeccionStore.inspeccionActual.colector_mat_entrada_2 = m.id"
                        :class="inspeccionStore.inspeccionActual.colector_mat_entrada_2 === m.id 
                          ? 'bg-emerald-500 text-white shadow-lg scale-[1.02]' 
                          : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                        class="py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all flex items-center justify-center"
                      >
                        {{ m.label }}
                      </button>
                    </div>
                  </div>
                  <div class="flex flex-col gap-3 col-span-2">
                    <label for="diam_entrada_2" class="text-[10px] font-black uppercase tracking-[0.1em] text-emerald-500/70">Diámetro Entrada 2 (mm)</label>
                    <input 
                      id="diam_entrada_2" 
                      v-model.number="inspeccionStore.inspeccionActual.colector_diametro_entrada_mm_2"
                      type="number" 
                      placeholder="Ej. 300"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-emerald-500/10 focus:border-emerald-500 outline-none"
                    />
                  </div>
                </div>
              </div>

              <!-- Colector Salida 2 (Solo si hay ID) -->
              <div v-if="inspeccionStore.inspeccionActual.red_va_a_pozo_2" class="bg-white dark:bg-slate-900 p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 rounded-xl bg-indigo-500/10 flex items-center justify-center">
                    <span class="material-symbols-outlined text-indigo-600">logout</span>
                  </div>
                  <span class="text-xs font-black uppercase tracking-[0.2em] text-slate-900 dark:text-white">Colector Salida 2</span>
                </div>

                <div class="grid grid-cols-2 gap-6">
                  <div class="flex flex-col gap-3 col-span-2">
                    <label class="text-[10px] font-black uppercase tracking-[0.1em] text-indigo-500/70">Material Salida 2</label>
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 p-1.5 bg-slate-200 dark:bg-slate-800 rounded-2xl">
                      <button 
                        v-for="m in materialesList" 
                        :key="m.id"
                        @click="inspeccionStore.inspeccionActual.colector_mat_salida_2 = m.id"
                        :class="inspeccionStore.inspeccionActual.colector_mat_salida_2 === m.id 
                          ? 'bg-indigo-500 text-white shadow-lg scale-[1.02]' 
                          : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'"
                        class="py-4 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all flex items-center justify-center"
                      >
                        {{ m.label }}
                      </button>
                    </div>
                  </div>
                  <div class="flex flex-col gap-3 col-span-2">
                    <label for="diam_salida_2" class="text-[10px] font-black uppercase tracking-[0.1em] text-indigo-500/70">Diámetro Salida 2 (mm)</label>
                    <input 
                      id="diam_salida_2" 
                      v-model.number="inspeccionStore.inspeccionActual.colector_diametro_salida_mm_2"
                      type="number" 
                      placeholder="Ej. 300"
                      class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl h-14 px-4 text-slate-900 dark:text-white font-black text-xs focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none"
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
import { ref, onMounted, nextTick, watch } from 'vue';
import { useInspeccionStore } from '@/store/inspeccion';
import { db, type PozoInventario } from '@/db/db';
import L from 'leaflet';
import proj4 from 'proj4';
import 'leaflet/dist/leaflet.css';

// Fix para iconos de Leaflet en producción
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
});

const UTM_29N = "+proj=utm +zone=29 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs";
const WGS84 = "EPSG:4326";

const inspeccionStore = useInspeccionStore();
const modoSeleccion = ref<'desde' | 'hacia' | 'desde2' | 'hacia2' | null>(null);

let map: L.Map | null = null;
let wellsLayer: L.LayerGroup | null = null;
let networkLines = L.featureGroup();
let gisLayerGroup: L.LayerGroup | null = null;
let gisLayers: { [key: string]: L.Layer } = {};

const materialesList = [
  { id: 'Hormigón', label: 'Hormigón' },
  { id: 'Gres', label: 'Gres' },
  { id: 'PVC', label: 'PVC' },
  { id: 'PEAD', label: 'PEAD' },
  { id: 'Fundición', label: 'Fundición' },
  { id: 'Fibrocemento', label: 'Fibrocemento' }
];

onMounted(() => {
    initMap();
});

const initMap = () => {
    // Tomar coordenadas del pozo actual del paso 1
    const { x, y } = inspeccionStore.inspeccionActual.coordenadas_utm;
    if (!x || !y) {
        console.warn('Paso 5: No hay coordenadas UTM para centrar el mapa.');
        return;
    }

    const [utmX, utmY] = [Number(x), Number(y)];
    const [lng, lat] = proj4(UTM_29N, WGS84, [utmX, utmY]);

    map = L.map('map-connectivity', {
        zoomControl: false,
        attributionControl: false,
        maxZoom: 22,
        preferCanvas: true
    }).setView([lat, lng], 19);


    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri',
        maxZoom: 22,
        maxNativeZoom: 19
    }).addTo(map);

    wellsLayer = L.layerGroup().addTo(map);
    networkLines.addTo(map);
    gisLayerGroup = L.layerGroup().addTo(map);

    // [NUEVO] Capas de Red GIS
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

    // Marcador Pozo Actual (Diferente estilo)
    L.circleMarker([lat, lng], {
        radius: 8,
        fillColor: '#ef4444',
        color: '#fff',
        weight: 3,
        opacity: 1,
        fillOpacity: 0.9
    }).addTo(map).bindTooltip('POZO ACTUAL', { permanent: true, direction: 'top', className: 'well-label-red' });

    cargarInventario();

    nextTick(() => {
        setTimeout(() => {
            if (map) {
                map.invalidateSize();
            }
        }, 100);
    });
};

const cargarCapasGIS = async () => {
  if (!map) return;

  const capas = [
    { url: '/data/principales.geojson', style: { color: '#FF0000', weight: 6, opacity: 1 }, name: 'principales' },
    { url: '/data/secundarios.geojson', style: { color: '#FFFF00', weight: 4, opacity: 1 }, name: 'secundarios' },
    { url: '/data/Prioritaria.geojson', style: { color: '#3b82f6', weight: 6, opacity: 1 }, name: 'prioritarios' }
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
          if (Math.abs(coords[0]) > 180) {
            const [lng, lat] = proj4(UTM_29N, WGS84, [coords[0], coords[1]]);
            return L.latLng(lat, lng);
          }
          return L.latLng(coords[1], coords[0]);
        }
      }).addTo(gisLayerGroup!);
    } catch (e) {
      console.warn(`Paso 5: No se pudo cargar la capa GIS ${capa.name}:`, e);
    }
  }
};


const wellsCoordsCache = new Map<string, L.LatLng>();

const cargarInventario = async () => {
    if (!map || !wellsLayer) return;
    
    // Limpiar capa anterior
    wellsLayer.clearLayers();
    wellsCoordsCache.clear();

    const { x, y } = inspeccionStore.inspeccionActual.coordenadas_utm;
    if (!x || !y) return;

    try {
        const radioBusqueda = 200; // Radio más amplio para conectividad
        
        // Búsqueda espacial optimizada en IndexedDB
        const pozos = await db.inventario_pozos
            .where('x').between(x - radioBusqueda, x + radioBusqueda)
            .and((p: PozoInventario) => p.y >= y - radioBusqueda && p.y <= y + radioBusqueda)
            .toArray();

        pozos.forEach((pozo: PozoInventario) => {
            const id_pozo = pozo.id;
            const [lng, lat] = proj4(UTM_29N, WGS84, [pozo.x, pozo.y]);
            const latlng = L.latLng(lat, lng);
            
            // Cachear coords para dibujo de líneas
            wellsCoordsCache.set(id_pozo, latlng);

            // No pintar el pozo actual de nuevo como interactivo
            if (id_pozo === inspeccionStore.inspeccionActual.id_pozo) return;

            L.circleMarker(latlng, {
                radius: 15, // Gigante para campo (60px de diámetro térmico)
                fillColor: '#3b82f6',
                color: '#fff',
                weight: 5,
                opacity: 1,
                fillOpacity: 0.9
            }).addTo(wellsLayer!)
            .on('click', () => {
                if (modoSeleccion.value === 'desde') {
                    inspeccionStore.inspeccionActual.red_viene_de_pozo = id_pozo;
                    modoSeleccion.value = null;
                } else if (modoSeleccion.value === 'hacia') {
                    inspeccionStore.inspeccionActual.red_va_a_pozo = id_pozo;
                    modoSeleccion.value = null;
                } else if (modoSeleccion.value === 'desde2') {
                    inspeccionStore.inspeccionActual.red_viene_de_pozo_2 = id_pozo;
                    modoSeleccion.value = null;
                } else if (modoSeleccion.value === 'hacia2') {
                    inspeccionStore.inspeccionActual.red_va_a_pozo_2 = id_pozo;
                    modoSeleccion.value = null;
                }
            }).bindTooltip(pozo.properties?.COD_CAMPO || id_pozo, { 
                permanent: true, 
                direction: 'bottom', 
                className: 'well-label-small',
                offset: [0, 10]
            });
        });

        // Intentar dibujar línea inicial si ya existen datos
        actualizarLineaRed();

    } catch (e) {
        console.error('Error al cargar inventario desde DB para mapa de red:', e);
    }
};

const actualizarLineaRed = () => {
    if (!map || !networkLines) return;
    networkLines.clearLayers();

    // Coordenadas del pozo actual
    const { x, y } = inspeccionStore.inspeccionActual.coordenadas_utm;
    if (!x || !y) return;
    const [l_curr, lat_curr] = proj4(UTM_29N, WGS84, [x, y]);
    const p_actual = L.latLng(lat_curr, l_curr);

    // Grupo 1
    const vD1 = inspeccionStore.inspeccionActual.red_viene_de_pozo;
    const vA1 = inspeccionStore.inspeccionActual.red_va_a_pozo;
    
    if (vD1 && wellsCoordsCache.has(vD1)) {
        L.polyline([wellsCoordsCache.get(vD1)!, p_actual], { color: '#10b981', weight: 8, dashArray: '12, 12', opacity: 0.8 }).addTo(networkLines);
    }
    if (vA1 && wellsCoordsCache.has(vA1)) {
        L.polyline([p_actual, wellsCoordsCache.get(vA1)!], { color: '#3b82f6', weight: 8, dashArray: '12, 12', opacity: 0.8 }).addTo(networkLines);
    }

    // Grupo 2
    const vD2 = inspeccionStore.inspeccionActual.red_viene_de_pozo_2;
    const vA2 = inspeccionStore.inspeccionActual.red_va_a_pozo_2;

    if (vD2 && wellsCoordsCache.has(vD2)) {
        L.polyline([wellsCoordsCache.get(vD2)!, p_actual], { color: '#059669', weight: 8, dashArray: '8, 16', opacity: 0.6 }).addTo(networkLines);
    }
    if (vA2 && wellsCoordsCache.has(vA2)) {
        L.polyline([p_actual, wellsCoordsCache.get(vA2)!], { color: '#4f46e5', weight: 8, dashArray: '8, 16', opacity: 0.6 }).addTo(networkLines);
    }
};

watch(() => [
    inspeccionStore.inspeccionActual.red_viene_de_pozo, 
    inspeccionStore.inspeccionActual.red_va_a_pozo,
    inspeccionStore.inspeccionActual.red_viene_de_pozo_2,
    inspeccionStore.inspeccionActual.red_va_a_pozo_2
], () => {
    actualizarLineaRed();
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

:deep(.well-label-red) {
  background: #ef4444 !important;
  border: 2px solid white !important;
  color: white !important;
  font-weight: 900 !important;
  font-size: 8px !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
}

:deep(.well-label-small) {
  background: #000000 !important;
  border: 1.5px solid #FFFFFF !important;
  color: white !important;
  font-weight: 900 !important;
  font-size: 10px !important;
  padding: 2px 6px !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
  opacity: 1 !important;
}

#map-connectivity {
  height: 240px !important;
  width: 100% !important;
}
</style>
