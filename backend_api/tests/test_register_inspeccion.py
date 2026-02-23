import uuid
import random
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import PozoSaneamientoModel

client = TestClient(app)

def test_register_inspeccion_success():
    """Test para validar TDD: Creación de Inspección Completa"""
    # Simulamos UUIDv7 válidos generados desde la PWA según el ADR-001
    pozo_id = "018f6d54-1b9a-7000-8000-000000000001"
    acometida_id = "018f6d54-1b9a-7000-8000-000000000002"
    id_pozo_real = f"P-{random.randint(1000, 99999)}"

    payload = {
        "id": pozo_id,
        "id_pozo": id_pozo_real,
        "coordenadas_utm": {
            "x": 535492.31,
            "y": 4801123.54
        },
        "fecha_inspec": "2026-02-23",
        "calle_zona": "Av. Principal",
        "situacion": "Calzada",
        "cota_tapa": 12.345,
        "profundidad_m": 2.10,
        "estado": "BUENO",
        "material_pozo": "HORMIGON",
        "tipo_acceso": "LIBRE",
        "num_pates": 5,
        "forma_pozo": "CIRCULAR",
        "diametro_pozo_mm": 1000,
        "tapa_forma": "CIRCULAR",
        "tapa_tipo": "ABISAGRADA",
        "tapa_material": "FUNDICION",
        "tapa_diametro_mm": 600,
        "red_tipo": "SANEAMIENTO",
        "colector_mat_entrada": "PVC",
        "colector_diametro_entrada_mm": 315,
        "colector_mat_salida": "PVC",
        "colector_diametro_salida_mm": 400,
        "ruta_foto_situacion": "s3://gis-captures/pozos/test_sit.jpg",
        "ruta_foto_interior": "s3://gis-captures/pozos/test_int.jpg",
        "observaciones": "Test integration TDD",
        "acometidas": [
            {
                "id": acometida_id,
                "numero_acometida": 1,
                "material": "PVC",
                "diametro_mm": 200,
                "profundidad_m": 1.25
            }
        ]
    }

    response = client.post("/inspecciones", json=payload)
    
    assert response.status_code == 201
    assert response.json() == {"status": "created", "id": pozo_id}

    db = SessionLocal()
    pozo = db.query(PozoSaneamientoModel).filter(PozoSaneamientoModel.id == pozo_id).first()
    assert pozo is not None
    assert pozo.id_pozo == id_pozo_real
    assert len(pozo.acometidas) == 1
    db.close()
