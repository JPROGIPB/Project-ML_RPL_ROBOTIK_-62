"""
Check database tables and structure
"""
from app import create_app, db
from app.config import Config
from app.models.user import User, Role
from app.models.robot import Robot
from app.models.certificate import CertificationModule
from app.models.booking import Booking

app = create_app(Config)

with app.app_context():
    print("="*60)
    print("CHECKING DATABASE STRUCTURE")
    print("="*60)

    # Check if tables exist by trying to query them
    try:
        # Check Users
        users = User.query.all()
        print(f"\n✅ Users table: {len(users)} users")
        for u in users:
            print(f"   - {u.email} (role_id: {u.role_id})")

    except Exception as e:
        print(f"\n❌ Users table error: {e}")

    try:
        # Check Roles
        roles = Role.query.all()
        print(f"\n✅ Roles table: {len(roles)} roles")
        for r in roles:
            print(f"   - {r.role_name}")

    except Exception as e:
        print(f"\n❌ Roles table error: {e}")

    try:
        # Check Robots
        robots = Robot.query.all()
        print(f"\n✅ Robots table: {len(robots)} robots")
        for r in robots:
            print(f"   - {r.robot_name} (owner_id: {r.owner_id})")

    except Exception as e:
        print(f"\n❌ Robots table error: {e}")

    try:
        # Check Certification Modules
        modules = CertificationModule.query.all()
        print(f"\n✅ Certification Modules: {len(modules)} modules")
        for m in modules:
            print(f"   - Module {m.module_number}: {m.title}")

    except Exception as e:
        print(f"\n❌ Certification Modules error: {e}")

    try:
        # Check Bookings
        bookings = Booking.query.all()
        print(f"\n✅ Bookings table: {len(bookings)} bookings")

    except Exception as e:
        print(f"\n❌ Bookings table error: {e}")

    print("\n" + "="*60)
    print("DATABASE CHECK COMPLETE")
    print("="*60)

    # Check if DB needs initialization
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)

    if User.query.count() == 0:
        print("\n⚠️  WARNING: No users found!")
        print("   Run: python seed_data.py")

    if Role.query.count() == 0:
        print("\n⚠️  WARNING: No roles found!")
        print("   Run: python seed_data.py")

    if Robot.query.count() == 0:
        print("\n⚠️  WARNING: No robots found!")
        print("   Run: python seed_data.py")

    if CertificationModule.query.count() == 0:
        print("\n⚠️  WARNING: No certification modules found!")
        print("   Run: python seed_data.py")

    print("\n" + "="*60)
