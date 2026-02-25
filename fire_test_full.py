import requests
import uuid
import time
import os

# Configuración de la API Central
API_URL = "http://localhost:8000"
USER_EMAIL = "admin@example.com"
USER_PASS = "password123"

def run_fire_test():
    print("🚀 Iniciando PRUEBA DE FUEGO Integral...")

    # 1. Login
    print("\n🔐 1. Autenticando en la API...")
    login_res = requests.post(f"{API_URL}/login", data={
        "username": USER_EMAIL,
        "password": USER_PASS
    })
    if login_res.status_code != 200:
        print(f"❌ Error de login: {login_res.text}")
        return
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Token obtenido con éxito.")

    # 2. Crear Inspección
    inspeccion_id = str(uuid.uuid4())
    pozo_tag = f"P-FIRE-{int(time.time())}"
    print(f"\n📝 2. Creando Inspección [{inspeccion_id}] para Pozo [{pozo_tag}]...")
    payload = {
        "id": inspeccion_id,
        "id_pozo": pozo_tag,
        "fecha_inspec": "2026-02-25",
        "calle_zona": "Avenida de la Integración Total",
        "coordenadas_utm": {"x": 537123, "y": 4681234},
        "situacion": "Normal",
        "profundidad_m": 2.5,
        "estado": "Operativo",
        "acometidas": [
            {"id": str(uuid.uuid4()), "material": "PVC", "diametro_mm": 110, "numero_acometida": 100, "profundidad_m": 1.2}
        ]
    }
    
    res = requests.post(f"{API_URL}/inspecciones", json=payload, headers=headers)
    if res.status_code not in [200, 201]:
        print(f"❌ Error creando inspección: {res.text}")
        return
    print("✅ Inspección creada en PostgreSQL y evento publicado en RabbitMQ.")
    
    # Pausa para asegurar persistencia en DB antes de subir fotos
    time.sleep(1)

    # 3. Subir Fotos (Esto disparará la descarga en el Worker)
    print("\n📸 3. Subiendo fotos de inspección...")
    # Crear fotos temporales para el test
    with open("test_situacion.jpg", "wb") as f: f.write(b"fake-image-situacion")
    with open("test_interior.jpg", "wb") as f: f.write(b"fake-image-interior")

    for photo_name in ["test_situacion.jpg", "test_interior.jpg"]:
        with open(photo_name, "rb") as f:
            files = {"file": (photo_name, f, "image/jpeg")}
            photo_res = requests.post(f"{API_URL}/inspecciones/{inspeccion_id}/photos", files=files, headers=headers)
            if photo_res.status_code not in [200, 201]:
                print(f"❌ Error subiendo {photo_name}: {photo_res.text}")
            else:
                print(f"✅ {photo_name} subida a MinIO.")

    print("\n🏁 FLUJO DE API COMPLETADO.")
    print("⏳ Ahora el Worker On-Premise debería detectar el evento y generar el GeoPackage en X:.")
    print("🔍 Revisa los logs de 'gis-worker' para confirmar el éxito final.")

if __name__ == "__main__":
    run_fire_test()
