-- Habilitación de extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Tabla: tecnicos (Gestión de Identidad y Autorización Offline-First)
CREATE TABLE tecnicos (
    id UUID PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla principal: pozos_saneamiento
CREATE TABLE pozos_saneamiento (
    id UUID PRIMARY KEY,
    id_pozo VARCHAR(50) UNIQUE NOT NULL,
    geom GEOMETRY(Point, 25829), -- EPSG:25829 (UTM ETRS89 Huso 29N)
    tecnico_id UUID REFERENCES tecnicos(id),
    fecha_inspec DATE,
    calle_zona VARCHAR(255),
    situacion VARCHAR(100),
    cota_tapa NUMERIC(8,3),
    profundidad_m NUMERIC(6,2),
    estado VARCHAR(50),
    material_pozo VARCHAR(50),
    tipo_acceso VARCHAR(50),
    num_pates INTEGER,
    forma_pozo VARCHAR(50),
    diametro_pozo_mm INTEGER,
    largo_pozo_mm INTEGER,
    ancho_pozo_mm INTEGER,
    resalto VARCHAR(50),
    filtraciones VARCHAR(50),
    pluviales VARCHAR(50),
    biofilm VARCHAR(50),
    tapa_forma VARCHAR(50),
    tapa_tipo VARCHAR(50),
    tapa_material VARCHAR(50),
    tapa_diametro_mm INTEGER,
    tapa_largo_mm INTEGER,
    tapa_ancho_mm INTEGER,
    red_tipo VARCHAR(50),
    red_viene_de_pozo VARCHAR(50),
    red_va_a_pozo VARCHAR(50),
    red_carga VARCHAR(50),
    colector_mat_entrada VARCHAR(50),
    colector_diametro_entrada_mm INTEGER,
    colector_mat_salida VARCHAR(50),
    colector_diametro_salida_mm INTEGER,
    ruta_foto_situacion TEXT,
    ruta_foto_interior TEXT,
    observaciones TEXT
);

-- Índices geoespaciales y de integridad
CREATE INDEX idx_pozos_geom ON pozos_saneamiento USING GIST (geom);

-- Tabla dependiente: acometidas_saneamiento
CREATE TABLE acometidas_saneamiento (
    id UUID PRIMARY KEY,
    pozo_id UUID REFERENCES pozos_saneamiento(id) ON DELETE CASCADE,
    numero_acometida INTEGER,
    material VARCHAR(50),
    diametro_mm INTEGER,
    profundidad_m NUMERIC(5,2)
);

CREATE INDEX idx_acometidas_pozo_id ON acometidas_saneamiento (pozo_id);

-- Tabla: outbox_events (Transaccionalidad garantizada)
CREATE TABLE outbox_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ
);

CREATE INDEX idx_outbox_unprocessed ON outbox_events (created_at) WHERE processed_at IS NULL;
