CREATE TABLE tecnicos (
    id UUID PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

ALTER TABLE pozos_saneamiento
ADD COLUMN tecnico_id UUID,
ADD CONSTRAINT fk_pozo_tecnico
    FOREIGN KEY (tecnico_id)
    REFERENCES tecnicos(id);
