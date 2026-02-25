import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para añadir el Token en cada petición
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor para manejar errores globales (ej. 401)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            console.error('API Error Response:', error.response.status, error.response.data);
            if (error.response.status === 401) {
                console.warn('Token expirado o inválido. Redirigiendo a login...');
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
        } else {
            console.error('API Network or Setup Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export const apiService = {
    // Autenticación
    async login(credentials: any) {
        const params = new URLSearchParams();
        params.append('username', credentials.email);
        params.append('password', credentials.password);

        // El backend espera form-data en: POST /login
        const response = await api.post('/login', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },

    // Inspecciones
    async postInspeccion(data: any) {
        const response = await api.post('/inspecciones', data);
        return response.data;
    },

    // Fotos (Multipart)
    async uploadPhoto(inspeccionId: string, fileBlob: Blob, fileName: string) {
        const formData = new FormData();
        formData.append('file', fileBlob, fileName);

        const response = await api.post(`/inspecciones/${inspeccionId}/photos`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
};

export default api;
