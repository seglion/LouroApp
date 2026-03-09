import { defineStore } from 'pinia';
import { toRaw } from 'vue';
import { v7 as uuidv7 } from 'uuid';
import { db, type InspeccionLocal } from '@/db/db';

const getInitialState = () => ({
    inspeccionActual: {
        id: '',
        id_pozo: '',
        coordenadas_utm: { x: null as number | null, y: null as number | null },
        fecha_inspec: '',
        calle_zona: '',
        situacion: '',
        cota_tapa: null as number | null,
        profundidad_m: null as number | null,
        material_pozo: 'Hormigón',
        tipo_acceso: 'Ninguno',
        num_pates: 0,
        forma_pozo: 'Circular',
        diametro_pozo_mm: 1000 as number | null,
        largo_pozo_mm: null as number | null,
        ancho_pozo_mm: null as number | null,
        resalto: 'No',
        filtraciones: 'No',
        pluviales: 'No',
        biofilm: 'No',
        estado: 'Bueno',
        limpieza: 'Limpio',
        observaciones: '',
        tapa_forma: 'Circular',
        tapa_tipo: 'Abatible',
        tapa_material: 'Fundición Dúctil',
        tapa_diametro_mm: 600 as number | null,
        tapa_largo_mm: null as number | null,
        tapa_ancho_mm: null as number | null,
        red_tipo: 'Unitario',
        red_viene_de_pozo: '',
        red_va_a_pozo: '',
        red_carga: 'Media',
        colector_mat_entrada: 'PVC',
        colector_diametro_entrada_mm: null as number | null,
        colector_mat_salida: 'PVC',
        colector_diametro_salida_mm: null as number | null,
        acometidas: [] as any[],
        estado_paso: 1,
        finalizada: false,
        ruta_foto_situacion: null as string | null,
        ruta_foto_interior: null as string | null
    },
    fotosTemporales: {
        situacion: null as string | null,
        interior: null as string | null,
        blob_situacion: null as Blob | null,
        blob_interior: null as Blob | null
    }
});

export const useInspeccionStore = defineStore('inspeccion', {
    state: () => getInitialState(),
    getters: {
        pasoActualValido(state): boolean {
            const i = state.inspeccionActual;
            switch (i.estado_paso) {
                case 1:
                    const cotaValida = i.cota_tapa !== null && i.cota_tapa !== undefined && i.cota_tapa.toString() !== '';
                    return !!(i.id_pozo && i.situacion && i.fecha_inspec && i.coordenadas_utm.x && i.coordenadas_utm.y && cotaValida);
                case 2:
                    const tapaOk = i.tapa_forma === 'Circular'
                        ? (i.tapa_diametro_mm && i.tapa_diametro_mm > 0)
                        : (i.tapa_largo_mm && i.tapa_largo_mm > 0 && i.tapa_ancho_mm && i.tapa_ancho_mm > 0);
                    return !!(i.tapa_material && i.tapa_tipo && tapaOk);
                case 3:
                    const dimOk = i.forma_pozo === 'Circular'
                        ? (i.diametro_pozo_mm && i.diametro_pozo_mm > 0)
                        : (i.largo_pozo_mm && i.largo_pozo_mm > 0 && i.ancho_pozo_mm && i.ancho_pozo_mm > 0);
                    return !!(i.material_pozo && i.profundidad_m && i.tipo_acceso && dimOk);
                case 4:
                    return !!(i.estado && i.limpieza);
                case 5:
                    return !!(i.red_tipo && i.red_viene_de_pozo && i.red_va_a_pozo);
                case 6:
                    return true; // Acometidas son opcionales o lista dinámica
                default:
                    return false;
            }
        }
    },
    actions: {
        async iniciarNuevaInspeccion() {
            // Reset inicial
            const initialState = getInitialState();
            Object.assign(this.$state, initialState);

            try {
                // Buscar el último pozo finalizado o sincronizado para heredar datos
                const ultimo = await db.inspecciones
                    .orderBy('last_modified')
                    .reverse()
                    .filter(i => i.finalizada === true || i.sync_status === 'synced')
                    .first();

                if (ultimo) {
                    console.log('Heredando datos del pozo anterior:', ultimo.id_pozo);
                    this.inspeccionActual.situacion = ultimo.situacion || '';
                    this.inspeccionActual.tapa_forma = ultimo.tapa_forma || 'Circular';
                    this.inspeccionActual.tapa_diametro_mm = ultimo.tapa_diametro_mm || 600;
                    this.inspeccionActual.tapa_material = ultimo.tapa_material || 'Fundición Dúctil';
                    this.inspeccionActual.tapa_tipo = ultimo.tapa_tipo || 'Abatible';

                    // Herencia Paso 3: Detalles del Pozo
                    this.inspeccionActual.forma_pozo = ultimo.forma_pozo || 'Circular';
                    this.inspeccionActual.material_pozo = ultimo.material_pozo || 'Hormigón';
                    this.inspeccionActual.diametro_pozo_mm = ultimo.diametro_pozo_mm || 1000;
                    this.inspeccionActual.largo_pozo_mm = ultimo.largo_pozo_mm || null;
                    this.inspeccionActual.ancho_pozo_mm = ultimo.ancho_pozo_mm || null;
                    this.inspeccionActual.tipo_acceso = ultimo.tipo_acceso || 'Ninguno';
                }
            } catch (error) {
                console.warn('No se pudo recuperar datos de herencia, usando valores por defecto:', error);
            }

            this.inspeccionActual.id = uuidv7();
            const datePart = new Date().toISOString().split('T')[0];
            this.inspeccionActual.fecha_inspec = datePart || '';

            await this.guardarEnDB();
        },
        async guardarEnDB() {
            if (!this.inspeccionActual.id) return;

            try {
                // Clonar el objeto de forma nativa eliminando proxies de Vue
                const plainData = structuredClone(toRaw(this.inspeccionActual));

                const data: InspeccionLocal = {
                    ...plainData,
                    sync_status: 'pending',
                    last_modified: new Date().toISOString(),
                    // Inyectar los blobs para persistencia offline real
                    blob_foto_situacion: this.fotosTemporales.blob_situacion,
                    blob_foto_interior: this.fotosTemporales.blob_interior
                };

                await db.inspecciones.put(data);
                console.log('Inspección guardada con éxito en IndexedDB:', data.id);
            } catch (error) {
                console.error('Error crítico al guardar en IndexedDB:', error);
                throw error; // Re-lanzar para que quien llame pueda manejarlo si es necesario
            }
        },
        async cargarInspeccion(id: string) {
            const data = await db.inspecciones.get(id);
            if (data) {
                // Separar metadatos de IndexedDB de los datos de la inspección
                const { sync_status, last_modified, blob_foto_situacion, blob_foto_interior, ...datosInspeccion } = data;

                // Mezclar con el estado inicial para rellenar campos vacíos en borradores antiguos
                const defaults = getInitialState().inspeccionActual;
                this.inspeccionActual = {
                    ...defaults,
                    ...datosInspeccion,
                    // Asegurar que si los strings están vacíos pero tienen default, se usen los defaults
                    colector_mat_entrada: datosInspeccion.colector_mat_entrada || defaults.colector_mat_entrada,
                    colector_mat_salida: datosInspeccion.colector_mat_salida || defaults.colector_mat_salida,
                    material_pozo: datosInspeccion.material_pozo || defaults.material_pozo,
                    tapa_material: datosInspeccion.tapa_material || defaults.tapa_material,
                    tapa_forma: datosInspeccion.tapa_forma || defaults.tapa_forma,
                    tapa_tipo: datosInspeccion.tapa_tipo || defaults.tapa_tipo
                };

                // Reconstruir URLs temporales si hay blobs persistidos
                if (blob_foto_situacion) {
                    this.fotosTemporales.blob_situacion = blob_foto_situacion;
                    this.fotosTemporales.situacion = URL.createObjectURL(blob_foto_situacion);
                }
                if (blob_foto_interior) {
                    this.fotosTemporales.blob_interior = blob_foto_interior;
                    this.fotosTemporales.interior = URL.createObjectURL(blob_foto_interior);
                }

                console.log('Inspección cargada desde IndexedDB:', id);
            }
        },
        async recuperarUltimoBorrador() {
            try {
                const ultimo = await db.inspecciones
                    .orderBy('last_modified')
                    .last();

                if (ultimo && ultimo.sync_status === 'pending') {
                    const { sync_status, last_modified, ...datos } = ultimo;

                    // Aplicar defaults a campos vacíos
                    const defaults = getInitialState().inspeccionActual;
                    this.inspeccionActual = {
                        ...defaults,
                        ...datos,
                        colector_mat_entrada: datos.colector_mat_entrada || defaults.colector_mat_entrada,
                        colector_mat_salida: datos.colector_mat_salida || defaults.colector_mat_salida,
                        material_pozo: datos.material_pozo || defaults.material_pozo,
                        tapa_material: datos.tapa_material || defaults.tapa_material,
                        tapa_forma: datos.tapa_forma || defaults.tapa_forma,
                        tapa_tipo: datos.tapa_tipo || defaults.tapa_tipo
                    };

                    console.log('Sesión recuperada automáticamente:', ultimo.id);
                    return true;
                }
            } catch (error) {
                console.error('Error al recuperar el último borrador:', error);
            }
            return false;
        },
        avanzarPaso() {
            if (this.inspeccionActual.estado_paso < 6) {
                this.inspeccionActual.estado_paso++;
                this.guardarEnDB();
            }
        },
        retrocederPaso() {
            if (this.inspeccionActual.estado_paso > 1) {
                this.inspeccionActual.estado_paso--;
                this.guardarEnDB();
            }
        },
        async cargarInspeccionExistente(id: string) {
            // Carga los datos y resetea al paso 1 para poder editar
            await this.cargarInspeccion(id);
            this.inspeccionActual.estado_paso = 1;
        }
    }
});
