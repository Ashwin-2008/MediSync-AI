import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from backend.core.database import engine
from backend.models.auth import User, Role
from backend.core.auth import get_password_hash

async def create_admin():
    async with AsyncSession(engine) as db:
        # Get or confirm Admin role exists
        result = await db.execute(select(Role).where(Role.name == "Admin"))
        role = result.scalars().first()
        if not role:
            print("ERROR: Admin role not found. Run full seed first.")
            return

        # Check if admin user already exists
        result = await db.execute(select(User).where(User.email == "admin@hospital.com"))
        existing = result.scalars().first()
        if existing:
            print(f"Admin user already exists: email=admin@hospital.com, is_active={existing.is_active}")
            return

        admin = User(
            email="admin@hospital.com",
            username="admin",
            hashed_password=get_password_hash("password123"),
            first_name="Admin",
            last_name="User",
            role_id=role.id,
            is_active=True,
        )
        db.add(admin)
        await db.commit()
        print("Admin user created: admin@hospital.com / password123")

asyncio.run(create_admin())
