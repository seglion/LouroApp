import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory((import.meta as any).env.BASE_URL || '/'),
    routes: [
        {
            path: '/',
            name: 'dashboard',
            component: () => import('../views/DashboardView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/historial',
            name: 'historial',
            component: () => import('../views/HistorialView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/nueva-inspeccion',
            component: () => import('../views/inspeccion/InspeccionLayout.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '', /* default step is managed by the store, but we route here */
                    name: 'inspeccion-paso-1',
                    component: () => import('../views/inspeccion/Paso1_General.vue')
                },
                {
                    path: 'paso-2',
                    name: 'inspeccion-paso-2',
                    component: () => import('../views/inspeccion/Paso2_Detalles.vue')
                },
                {
                    path: 'paso-3',
                    name: 'inspeccion-paso-3',
                    component: () => import('../views/inspeccion/Paso3_Tapa.vue')
                },
                {
                    path: 'paso-4',
                    name: 'inspeccion-paso-4',
                    component: () => import('../views/inspeccion/Paso4_EstadoEntorno.vue')
                },
                {
                    path: 'paso-5',
                    name: 'inspeccion-paso-5',
                    component: () => import('../views/inspeccion/Paso5_RedColector.vue')
                },
                {
                    path: 'paso-6',
                    name: 'inspeccion-paso-6',
                    component: () => import('../views/inspeccion/Paso6_Acometidas.vue')
                }
            ]
        }
    ]
})

router.beforeEach((to, _from, next) => {
    const token = localStorage.getItem('token');
    const isAuthenticated = !!token;

    if (to.meta.requiresAuth && !isAuthenticated) {
        // No autenticado, redirigir al login
        next('/login');
    } else if (to.path === '/login' && isAuthenticated) {
        // Ya autenticado, redirigir al dashboard
        next('/');
    } else {
        next();
    }
})

export default router;
