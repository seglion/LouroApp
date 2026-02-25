import { db, type InspeccionLocal } from '@/db/db';
import { apiService } from '@/services/api';

export const syncService = {
    isSyncing: false,

    async startSync() {
        if (this.isSyncing) return;
        if (!navigator.onLine) {
            console.log('Sincronización abortada: Sin conexión a internet.');
            return;
        }

        this.isSyncing = true;
        console.log('Iniciando motor de sincronización...');

        try {
            // Recogemos tanto 'pending' como 'error' (reintentos automáticos)
            const all = await db.inspecciones
                .filter(i => i.finalizada === true && (i.sync_status === 'pending' || i.sync_status === 'error'))
                .toArray();

            if (all.length === 0) {
                console.log('No hay inspecciones pendientes de sincronizar.');
                return;
            }

            console.log(`Encontradas ${all.length} inspección(es) para subir.`);

            for (const inspeccion of all) {
                await this.procesoSyncInspeccion(inspeccion);
            }
        } catch (error) {
            console.error('Error general en el motor de sincronización:', error);
        } finally {
            this.isSyncing = false;
            console.log('Motor de sincronización finalizado.');
        }
    },

    async procesoSyncInspeccion(inspeccion: InspeccionLocal) {
        console.log(`[SYNC] Procesando inspección ${inspeccion.id}...`);

        try {
            // 1. Preparar payload: eliminar campos internos de IndexedDB y blobs
            const payload = { ...inspeccion } as any;
            delete payload.sync_status;
            delete payload.last_modified;
            delete payload.estado_paso;
            delete payload.finalizada;
            delete payload.blob_foto_situacion;
            delete payload.blob_foto_interior;
            // Rutas de foto a null: el servidor las asignará al subir los archivos
            payload.ruta_foto_situacion = null;
            payload.ruta_foto_interior = null;

            // 2. Crear el registro base en la API (idempotente: 201=nuevo, 200=ya existía)
            console.log(`[SYNC] POST /inspecciones para ${inspeccion.id_pozo}...`);
            const result = await apiService.postInspeccion(payload);
            if (result?.status === 'already_exists') {
                console.log(`[SYNC] ℹ️ Inspección ya existía en servidor. Continuando con fotos...`);
            } else {
                console.log(`[SYNC] ✅ Registro creado en el servidor.`);
            }

            // 3. Subir fotos (el registro ya existe, sin riesgo de 404)
            let keySituacion: string | null = null;
            let keyInterior: string | null = null;

            if (inspeccion.blob_foto_situacion) {
                console.log('[SYNC] Subiendo foto de situación...');
                const res = await apiService.uploadPhoto(
                    inspeccion.id,
                    inspeccion.blob_foto_situacion,
                    `${inspeccion.id}_situacion.jpg`
                );
                keySituacion = res.foto_keys?.[res.foto_keys.length - 1] ?? null;
            }

            if (inspeccion.blob_foto_interior) {
                console.log('[SYNC] Subiendo foto interior...');
                const res = await apiService.uploadPhoto(
                    inspeccion.id,
                    inspeccion.blob_foto_interior,
                    `${inspeccion.id}_pozo.jpg`
                );
                keyInterior = res.foto_keys?.[res.foto_keys.length - 1] ?? null;
            }

            // 4. Solo si TODO fue bien → marcar como 'synced'
            await db.inspecciones.update(inspeccion.id, {
                sync_status: 'synced',
                last_modified: new Date().toISOString(),
                ruta_foto_situacion: keySituacion,
                ruta_foto_interior: keyInterior
            });

            console.log(`[SYNC] ✅ Inspección ${inspeccion.id} marcada como SINCRONIZADA.`);

        } catch (error: any) {
            const detail = error?.response?.data?.detail ?? error?.message ?? 'Error desconocido';
            console.error(`[SYNC] ❌ Fallo al sincronizar ${inspeccion.id}: ${detail}`);

            // Se mantiene en estado 'error' para que el próximo startSync() lo reintente
            await db.inspecciones.update(inspeccion.id, {
                sync_status: 'error',
                last_modified: new Date().toISOString()
            });
        }
    }
};
