import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.core.database import engine

async def check():
    async with AsyncSession(engine) as s:
        # Check if users table has any rows
        r = await s.execute(text("SELECT COUNT(*) FROM users"))
        count = r.scalar()
        print(f"Total users in DB: {count}")

        # Check for admin specifically
        r2 = await s.execute(text("SELECT email, is_active FROM users WHERE email='admin@hospital.com' LIMIT 1"))
        row = r2.fetchone()
        if row:
            print(f"Admin found: email={row[0]}, is_active={row[1]}")
        else:
            print("Admin user NOT FOUND — database has not been seeded.")

        # List first 5 users if any exist
        if count > 0:
            r3 = await s.execute(text("SELECT email FROM users LIMIT 5"))
            print("Sample users:", [row[0] for row in r3.fetchall()])

asyncio.run(check())
