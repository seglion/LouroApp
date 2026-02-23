# Plan de Tareas: Fase 2 - Caso de Uso "Registrar Inspección"

- [x] Definir `src/domain/entities.py` y `src/domain/repository_interface.py`.
- [x] Implementar `src/application/register_inspeccion.py` (Caso de Uso).
- [x] Crear `src/infrastructure/db/models.py` (SQLAlchemy).
- [x] Crear `src/infrastructure/db/sqlalchemy_repository.py`.
- [x] Crear los schemas de `pydantic` en `src/infrastructure/api/schemas.py`.
- [x] Escribir prueba TDD (RED): `tests/test_register_inspeccion.py`.
- [x] Implementar endpoint POST en `src/infrastructure/api/main.py`.

## Fase 3: Dominio de Identidad y Usuarios
- [x] Minitarea 1: Crear `src/domain/user_entities.py` (entidad `User`/`Tecnico` y Enum `Role`).
- [x] Minitarea 2: Crear la interfaz `src/domain/user_repository_interface.py` (`save`, `get_by_email`, `get_by_id`).
- [x] Minitarea 3: Modificar `src/infrastructure/db/models.py` añadiendo `UserModel`.
- [x] Minitarea 4: Implementar `SqlAlchemyUserRepository` (en `src/infrastructure/db/repositories.py` o módulo equivalente).
- [x] Minitarea 5: Fase TDD RED: Crear `tests/test_user_repository.py` simulando la persistencia y recuperación.
- [x] Minitarea 6: Refactor de `Inspeccion` para enlazar `tecnico_id` a la entidad `User`.

## Fase 4: Autenticación JWT y Seguridad
- [x] Minitarea 1: Añadir `passlib[bcrypt]` y `python-jose[cryptography]` a `requirements.txt`.
- [x] Minitarea 2: Crear servicio `src/infrastructure/security/hashing.py`.
- [x] Minitarea 3: Crear Caso de Uso `src/application/login_user.py` para verificar hash y generar JWT.
- [x] Minitarea 4: Implementar dependencias API `src/infrastructure/api/dependencies.py` (`get_current_user`).
- [x] Minitarea 5: Testing (TDD RED): `tests/test_auth_flow.py`.
- [x] Minitarea 6: Refactor de `POST /inspecciones` y schema para obtener el `tecnico_id` del JWT.
## Fase 5: Actualización de Perfil (Update User)
- [x] Minitarea 1: Añadir `update(user: User)` a `src/domain/user_repository_interface.py`.
- [x] Minitarea 2: Crear el schema `UserUpdate` en `src/infrastructure/api/schemas.py`.
- [x] Minitarea 3: Implementar update() en `src/infrastructure/db/user_repository.py`.
- [x] Minitarea 4: Crear Caso de Uso `src/application/update_user.py` con re-hashing condicional.
- [x] Minitarea 5: Fase TDD RED: Crear `tests/test_user_update.py` con tests de name change y auth invalidation.
- [x] Minitarea 6: Añadir Endpoint PATCH `/users/me` en `main.py` protegido por `get_current_user`.
