import asyncio
import argparse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.seed_config import VOLUMES
from backend.core.database import DATABASE_URL
from backend.seeders import (
    seed_auth_hospital, seed_doctors, seed_patients,
    seed_appointments_vitals, seed_treatment, seed_labs,
    seed_workflow, seed_conversations, seed_billing, seed_analytics
)

async def main():
    parser = argparse.ArgumentParser(description="Hospital Management Synthetic Data Seeder")
    parser.add_argument("--size", choices=["small", "full", "demo"], default="small", help="Volume of data to generate")
    parser.add_argument("--batch-size", type=int, default=5000, help="Batch size for bulk inserts")
    parser.add_argument("--reset", action="store_true", help="Reset/Truncate database before seeding")
    args = parser.parse_args()

    print(f"Starting Seeder in {args.size} mode with batch size {args.batch_size}")
    
    # Select config
    config = VOLUMES["full"] if args.size == "full" else VOLUMES["small"]
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        if args.reset:
            print("WARNING: Resetting database... (Not fully implemented, rely on alembic downgrade for now)")

        print("--- 1. Seeding Auth & Hospital ---")
        context = await seed_auth_hospital(session, config, args.batch_size)
        
        print("--- 2. Seeding Doctors ---")
        context = await seed_doctors(session, config, context, args.batch_size)
        
        print("--- 3. Seeding Patients ---")
        context = await seed_patients(session, config, context, args.batch_size)
        
        print("--- 4. Seeding Appointments & Vitals ---")
        context = await seed_appointments_vitals(session, config, context, args.batch_size)
        
        print("--- 5. Seeding Treatments ---")
        context = await seed_treatment(session, config, context, args.batch_size)
        
        print("--- 6. Seeding Labs ---")
        context = await seed_labs(session, config, context, args.batch_size)
        
        print("--- 7. Seeding Workflow ---")
        context = await seed_workflow(session, config, context, args.batch_size)
        
        print("--- 8. Seeding Conversations ---")
        context = await seed_conversations(session, config, context, args.batch_size)
        
        print("--- 9. Seeding Billing ---")
        context = await seed_billing(session, config, context, args.batch_size)
        
        print("--- 10. Seeding Analytics ---")
        await seed_analytics(session, config, context, args.batch_size)

        print("Seeding Complete!")

if __name__ == "__main__":
    asyncio.run(main())
