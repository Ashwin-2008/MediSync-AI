import sys, os, asyncio
sys.modules['google._upb._message'] = None
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
sys.path.insert(0, r"d:\Third year Projects\Agentverse")

async def main():
    from backend.core.database import engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import text

    async with AsyncSession(engine) as db:
        # Test patients query directly
        print("=== Testing patients query ===")
        try:
            from backend.crud.crud_patient import patient as crud_patient
            items, total = await crud_patient.get_multi_with_count(db, skip=0, limit=10)
            print(f"OK: {total} patients, first={items[0].first_name if items else 'none'}")
        except Exception as e:
            print(f"FAIL: {type(e).__name__}: {e}")

        # Test treatments query directly
        print("\n=== Testing treatments query ===")
        try:
            from backend.crud.crud_treatment import treatment_plan as crud_tp
            items, total = await crud_tp.get_multi_with_count(db, skip=0, limit=10)
            print(f"OK: {total} treatment plans")
        except Exception as e:
            print(f"FAIL: {type(e).__name__}: {e}")

        # Test auth/me — check if user serialization works
        print("\n=== Testing user serialization ===")
        try:
            from backend.crud.crud_auth import user as crud_user
            u = await crud_user.get_by_email(db, email="admin@hospital.com")
            print(f"User found: {u.email}, role_id={u.role_id}")
            # Try serializing with schema
            from backend.schemas.auth import UserResponse
            resp = UserResponse.model_validate(u)
            print(f"Serialized OK: {resp.email}")
        except Exception as e:
            print(f"FAIL: {type(e).__name__}: {e}")

asyncio.run(main())
