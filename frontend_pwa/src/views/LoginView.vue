<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white dark:bg-background-dark group/design-root overflow-x-hidden font-display">
    
    <!-- Header / Logo Area -->
    <div class="flex items-center bg-white dark:bg-background-dark p-6 pb-2 justify-center">
      <div class="flex flex-col items-center gap-2">
        <div class="h-20 w-auto overflow-hidden">
          <img src="/pwa-512x512.png" alt="AQUATICA Logo" class="h-full w-full object-contain drop-shadow-sm" />
        </div>
        <h2 class="text-primary dark:text-slate-100 text-sm font-bold tracking-widest uppercase mt-4">Aplicación de Campo</h2>
      </div>
    </div>
    
    <!-- Hero Illustration -->
    <div class="@container">
      <div class="@[480px]:px-4 @[480px]:py-3">
        <div 
          class="w-full bg-center bg-no-repeat bg-cover flex flex-col justify-end overflow-hidden bg-slate-100 dark:bg-slate-800 @[480px]:rounded-lg min-h-[200px]" 
          data-alt="Industrial steel pipes and engineering infrastructure background" 
          style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDOdl2TF5DqgafJZUXYjmNOKoNJPLBFHgII3aCJIeBYZLEwK09HnKSmu2GE-bWqgkRfp-dpSZ7mk-kFxFFAAnbc_pnqHoJy_uB5YG_boCQ3L4BlKKY226vJffuSUpz6cLz5wF-5miaXpMQUANXYngdsihYWNKK_5TvgjQdk7ZKihceZx1XhhwxEbNn8ekdPWOzVrVLITKEF5pKhdXkhsKeDDjaDik0DFk_TFrKb2_IJ-LBKJvFFKusQU3ge9lrLG2DlQ_SXh2CoXSK4");'
        >
        </div>
      </div>
    </div>
    
    <!-- Form Container -->
    <div class="px-6 py-8">
      <h1 class="text-slate-900 dark:text-slate-100 tracking-tight text-3xl font-bold leading-tight text-center pb-2">Agente de Campo</h1>
      <p class="text-slate-500 dark:text-slate-400 text-sm font-normal leading-normal pb-8 text-center uppercase tracking-wider">Authentication Required</p>
      
      <form class="space-y-6" @submit.prevent="login">
        <!-- Email/ID Field -->
        <div class="flex flex-col gap-2">
          <label class="text-primary dark:text-slate-300 text-xs font-bold uppercase tracking-tight">
              Inspector ID / Email
          </label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">badge</span>
            <input 
              v-model="email"
              class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-slate-100 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 h-[48px] placeholder:text-slate-400 pl-12 pr-4 text-base font-normal leading-normal transition-all" 
              placeholder="tech_alfa_04" 
              type="text"
              required
            />
          </div>
        </div>
        
        <!-- Password Field -->
        <div class="flex flex-col gap-2">
          <label class="text-primary dark:text-slate-300 text-xs font-bold uppercase tracking-tight">
              Secure Password
          </label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">lock</span>
            <input 
              v-model="password"
              class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-slate-100 focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 h-[48px] placeholder:text-slate-400 pl-12 pr-4 text-base font-normal leading-normal transition-all" 
              placeholder="••••••••" 
              type="password"
              required
            />
          </div>
        </div>
        
        <!-- Error Message -->
        <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 p-4 rounded-lg text-sm font-bold flex items-center gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
          <span class="material-symbols-outlined text-xl">error</span>
          {{ errorMessage }}
        </div>
        
        <!-- Action Button -->
        <div class="pt-4">
          <button 
            :disabled="isLoading"
            class="w-full bg-primary hover:bg-slate-800 text-white font-bold py-4 px-6 rounded-lg transition-colors flex items-center justify-center gap-2 h-[48px] disabled:opacity-50 disabled:cursor-not-allowed" 
            type="submit"
          >
            <span v-if="!isLoading">ACCEDER</span>
            <span v-else class="animate-spin material-symbols-outlined">sync</span>
            <span v-if="!isLoading" class="material-symbols-outlined">arrow_forward</span>
          </button>
        </div>
      </form>
      
      <!-- Secondary Actions -->
      <div class="mt-8 flex flex-col items-center gap-4">
        <a class="text-slate-500 dark:text-slate-400 text-sm font-medium hover:text-primary dark:hover:text-slate-200 transition-colors" href="#">
            Trouble accessing account?
        </a>
        <div class="flex items-center gap-2 text-slate-400 dark:text-slate-600">
          <div class="h-px w-8 bg-current"></div>
          <span class="text-[10px] uppercase font-bold tracking-[0.2em]">v1.0.0-beta</span>
          <div class="h-px w-8 bg-current"></div>
        </div>
      </div>
    </div>
    
    <!-- Bottom Safe Area Spacer (iOS) -->
    <div class="h-10 bg-white dark:bg-background-dark"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '@/services/api';

const router = useRouter();
const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const login = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  
  try {
    const response = await apiService.login({
      email: email.value,
      password: password.value
    });
    
    // El backend devuelve { access_token: "...", token_type: "bearer" }
    if (response.access_token) {
      localStorage.setItem('token', response.access_token);
      router.push('/');
    } else {
      errorMessage.value = 'Token no recibido del servidor.';
    }
  } catch (error: any) {
    console.error('Login failed:', error);
    errorMessage.value = error.response?.data?.detail || 'Error al conectar con el servidor. Verifica tus credenciales.';
  } finally {
    isLoading.value = false;
  }
};
</script>
