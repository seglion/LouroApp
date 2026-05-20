-- Migración: añadir resalto_altura_cm a pozos_saneamiento
ALTER TABLE pozos_saneamiento ADD COLUMN IF NOT EXISTS resalto_altura_cm NUMERIC(6,2);
