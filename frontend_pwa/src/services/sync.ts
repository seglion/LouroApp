import { db, type InspeccionLocal } from '@/db/db';
import { apiService } from '@/services/api';

export const syncService = {
    isSyncing: false,

    async startSync(): Promise<{ total: number; synced: number; errors: number }> {
        const result = { total: 0, synced: 0, errors: 0 };
        if (this.isSyncing) return result;
        if (!navigator.onLine) {
            console.log('Sincronización abortada: Sin conexión a internet.');
            return result;
        }

        this.isSyncing = true;
        console.log('Iniciando motor de sincronización...');

        try {
            // Recogemos tanto 'pending' como 'error' (reintentos automáticos)
            const all = await db.inspecciones
                .filter(i => i.finalizada === true && (i.sync_status === 'pending' || i.sync_status === 'error'))
                .toArray();

            result.total = all.length;
            if (all.length === 0) {
                console.log('No hay inspecciones pendientes de sincronizar.');
                return result;
            }

            console.log(`Encontradas ${all.length} inspección(es) para subir.`);

            for (const inspeccion of all) {
                const success = await this.procesoSyncInspeccion(inspeccion);
                if (success) result.synced++;
                else result.errors++;
            }
        } catch (error) {
            console.error('Error general en el motor de sincronización:', error);
        } finally {
            this.isSyncing = false;
            console.log('Motor de sincronización finalizado.');
        }
        return result;
    },

    async procesoSyncInspeccion(inspeccion: InspeccionLocal): Promise<boolean> {
        console.log(`[SYNC] Procesando inspección ${inspeccion.id}...`);

        try {
            // 1. Preparar payload: separar metadatos locales de los datos de la API
            const {
                sync_status,
                last_modified,
                estado_paso,
                finalizada,
                blob_foto_situacion,
                blob_foto_interior,
                ...payload
            } = inspeccion;

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

            // 3. Subir fotos
            const keys = await this._subirFotos(inspeccion.id, inspeccion.blob_foto_situacion, inspeccion.blob_foto_interior);

            // 4. Solo si TODO fue bien → marcar como 'synced'
            await db.inspecciones.update(inspeccion.id, {
                sync_status: 'synced',
                last_modified: new Date().toISOString(),
                ruta_foto_situacion: keys.situacion,
                ruta_foto_interior: keys.interior
            });

            console.log(`[SYNC] ✅ Inspección ${inspeccion.id} marcada como SINCRONIZADA.`);
            return true;

        } catch (error: any) {
            const detail = error?.response?.data?.detail ?? error?.message ?? 'Error desconocido';
            console.error(`[SYNC] ❌ Fallo al sincronizar ${inspeccion.id}: ${detail}`);

            // Se mantiene en estado 'error' para que el próximo startSync() lo reintente
            await db.inspecciones.update(inspeccion.id, {
                sync_status: 'error',
                last_modified: new Date().toISOString()
            });
            return false;
        }
    },

    async _subirFotos(inspeccionId: string, blobSituacion?: Blob | null, blobInterior?: Blob | null) {
        let situacion: string | null = null;
        let interior: string | null = null;

        if (blobSituacion) {
            console.log('[SYNC] Subiendo foto de situación...');
            const res = await apiService.uploadPhoto(inspeccionId, blobSituacion, `${inspeccionId}_situacion.jpg`);
            situacion = res.foto_keys?.[res.foto_keys.length - 1] ?? null;
        }

        if (blobInterior) {
            console.log('[SYNC] Subiendo foto interior...');
            const res = await apiService.uploadPhoto(inspeccionId, blobInterior, `${inspeccionId}_pozo.jpg`);
            interior = res.foto_keys?.[res.foto_keys.length - 1] ?? null;
        }

        return { situacion, interior };
    }
};
