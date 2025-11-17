"""
Initialize database - create all tables
"""
from app import create_app, db
from app.config import Config

app = create_app(Config)

with app.app_context():
    print("="*60)
    print("INITIALIZING DATABASE")
    print("="*60)

    print("\nCreating all tables...")
    db.create_all()

    print("✅ Database tables created successfully!")

    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Run seed data:")
    print("   python seed_data.py")
    print("\n2. Start the server:")
    print("   python run.py")
    print("\n" + "="*60)
