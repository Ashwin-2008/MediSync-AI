import asyncio
from backend.core.database import AsyncSessionLocal
from backend.models.auth import User, Role
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).join(Role).where(Role.name == 'Admin').limit(1)
        )
        user = result.scalars().first()
        if user:
            print(f"EMAIL: {user.email}")
            print(f"PASSWORD: password123")
        else:
            print("No user found")

if __name__ == "__main__":
    asyncio.run(main())
