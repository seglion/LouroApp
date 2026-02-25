import Dexie, { type Table } from 'dexie';

export interface CoordenadasUTM {
    x: number | null;
    y: number | null;
}

export interface AcometidaData {
    id: string;
    numero_acometida: number;
    material: string;
    diametro_mm: number;
    profundidad_m: number;
}

export interface InspeccionLocal extends InspeccionRequest {
    // Metadatos para gestión offline
    sync_status: 'pending' | 'synced' | 'error';
    last_modified: string;
    estado_paso: number; // Persistir el progreso del formulario
    finalizada: boolean; // Marcar si el registro está completado para sincronización
    // Blobs para persistencia offline real de imágenes
    blob_foto_situacion?: Blob | null;
    blob_foto_interior?: Blob | null;
}

// Interfaz basada en OpenAPI
export interface InspeccionRequest {
    id: string; // UUIDv7
    id_pozo: string;
    coordenadas_utm: CoordenadasUTM;
    fecha_inspec: string;
    calle_zona: string;
    situacion: string;
    cota_tapa: number | null;
    profundidad_m: number | null;
    estado: string;
    material_pozo: string;
    tipo_acceso: string;
    num_pates: number;
    forma_pozo: string;
    diametro_pozo_mm: number | null;
    largo_pozo_mm: number | null;
    ancho_pozo_mm: number | null;
    resalto: string;
    filtraciones: string;
    pluviales: string;
    biofilm: string;
    limpieza: string;
    tapa_forma: string;
    tapa_tipo: string;
    tapa_material: string;
    tapa_diametro_mm: number | null;
    tapa_largo_mm: number | null;
    tapa_ancho_mm: number | null;
    red_tipo: string;
    red_viene_de_pozo: string;
    red_va_a_pozo: string;
    red_carga: string;
    colector_mat_entrada: string;
    colector_diametro_entrada_mm: number | null;
    colector_mat_salida: string;
    colector_diametro_salida_mm: number | null;
    ruta_foto_situacion: string | null;
    ruta_foto_interior: string | null;
    observaciones: string;
    acometidas: AcometidaData[];
}

export class AppDB extends Dexie {
    inspecciones!: Table<InspeccionLocal>;

    constructor() {
        super('LouroAppDB');
        this.version(1).stores({
            inspecciones: 'id, id_pozo, sync_status, last_modified' // Índices para búsquedas rápidas
        });
    }
}

export const db = new AppDB();
