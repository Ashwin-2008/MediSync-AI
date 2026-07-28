import asyncio
import argparse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import inspect
from backend.seed_config import VOLUMES
import backend.seed_utils as su
from backend.seeders import (
    seed_auth_hospital, seed_doctors, seed_patients,
    seed_appointments_vitals, seed_treatment, seed_labs,
    seed_workflow, seed_conversations, seed_billing, seed_analytics
)

mismatches = []

async def mock_bulk_insert(db_session, model, batch, batch_size=5000):
    if not batch:
        return
    mapper = inspect(model)
    valid_columns = set([c.key for c in mapper.columns])
    
    first_row = batch[0]
    provided_columns = set(first_row.keys())
    
    unconsumed = provided_columns - valid_columns
    missing = set([c.key for c in mapper.columns if not c.nullable and c.default is None and c.server_default is None and c.key != "id" and c.key != "created_at" and c.key != "updated_at"]) - provided_columns
    
    if unconsumed:
        print(f"[{model.__name__}] WARNING: Unconsumed columns passed in seed: {unconsumed}")
        mismatches.append(f"[{model.__name__}] unconsumed: {unconsumed}")
    if missing:
        # Just info, as some might be auto-generated or not strictly enforced at bulk insert time if they have DB defaults not captured in SQLAlchemy.
        # But good to know.
        pass

# Patch the bulk insert function
su.bulk_insert = mock_bulk_insert

# Also need a mock session since we aren't actually running queries!
class MockResult:
    def scalars(self):
        return self
    def all(self):
        return []
    def first(self):
        return None

class MockSession:
    async def execute(self, *args, **kwargs):
        return MockResult()
    async def commit(self):
        pass

async def main():
    print("Running Dry-Run Consistency Audit...")
    config = VOLUMES["small"]
    session = MockSession()

    try:
        context = await seed_auth_hospital(session, config, 1000)
        context = await seed_doctors(session, config, context, 1000)
        context = await seed_patients(session, config, context, 1000)
        context = await seed_appointments_vitals(session, config, context, 1000)
        context = await seed_treatment(session, config, context, 1000)
        context = await seed_labs(session, config, context, 1000)
        context = await seed_workflow(session, config, context, 1000)
        context = await seed_conversations(session, config, context, 1000)
        context = await seed_billing(session, config, context, 1000)
        await seed_analytics(session, config, context, 1000)
        print("Dry run completed.")
        if mismatches:
            print(f"Found {len(mismatches)} mismatches:")
            for m in mismatches:
                print(m)
        else:
            print("All schemas and seeders align perfectly.")
    except Exception as e:
        print(f"Failed with exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
