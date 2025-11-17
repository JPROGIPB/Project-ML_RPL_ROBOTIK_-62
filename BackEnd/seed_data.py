"""
Seed data script untuk initial database setup
Run: python seed_data.py
"""
from app import create_app, db
from app.config import Config
from app.models.user import User, Role, Permission, RolePermission
from app.models.certificate import CertificationModule
from app.models.product import Product
from app.models.robot import Robot
from app.utils.auth import hash_password

app = create_app(Config)

with app.app_context():
    # Clear existing data (optional - be careful in production!)
    # db.drop_all()
    # db.create_all()
    
    # Create Roles
    print("Creating roles...")
    admin_role = Role.query.filter_by(role_name='admin').first()
    if not admin_role:
        admin_role = Role(role_name='admin', description='System administrator with full access')
        db.session.add(admin_role)
    
    operator_role = Role.query.filter_by(role_name='operator').first()
    if not operator_role:
        operator_role = Role(role_name='operator', description='Certified robot operator')
        db.session.add(operator_role)
    
    customer_role = Role.query.filter_by(role_name='customer').first()
    if not customer_role:
        customer_role = Role(role_name='customer', description='Regular customer')
        db.session.add(customer_role)
    
    db.session.commit()
    
    # Create Permissions
    print("Creating permissions...")
    permissions_data = [
        ('view_dashboard', 'View dashboard and analytics'),
        ('control_robot', 'Control robot operations'),
        ('manage_robots', 'Manage robot inventory'),
        ('manage_users', 'Manage user accounts'),
        ('view_reports', 'View reports and analytics')
    ]
    
    for perm_name, description in permissions_data:
        perm = Permission.query.filter_by(perm_name=perm_name).first()
        if not perm:
            perm = Permission(perm_name=perm_name, description=description)
            db.session.add(perm)
    
    db.session.commit()
    
    # Link admin to all permissions
    admin_perms = RolePermission.query.filter_by(role_id=admin_role.role_id).all()
    if not admin_perms:
        all_perms = Permission.query.all()
        for perm in all_perms:
            rp = RolePermission(role_id=admin_role.role_id, perm_id=perm.perm_id)
            db.session.add(rp)
    
    db.session.commit()
    
    # Create Certification Modules
    print("Creating certification modules...")
    modules_data = [
        (1, 'Pengenalan Teknologi Sealen', 30, 'Pelajari dasar-dasar robot pembersih laut dan teknologi AI yang digunakan.', 1),
        (2, 'Navigasi dan Kontrol Robot', 45, 'Memahami sistem kontrol, navigasi otonom, dan antarmuka operator.', 2),
        (3, 'Pemeliharaan dan Troubleshooting', 40, 'Prosedur pemeliharaan rutin dan penanganan masalah umum.', 3),
        (4, 'Keselamatan dan Regulasi', 35, 'Standar keselamatan operasional dan regulasi maritim yang berlaku.', 4)
    ]
    
    for module_num, title, duration, description, order_idx in modules_data:
        module = CertificationModule.query.filter_by(module_number=module_num).first()
        if not module:
            module = CertificationModule(
                module_number=module_num,
                title=title,
                duration_minutes=duration,
                description=description,
                order_index=order_idx
            )
            db.session.add(module)
    
    db.session.commit()
    
    # Create Sample Products
    print("Creating sample products...")
    products_data = [
        {
            'name': 'Sealen CleanBot',
            'category': 'Robot',
            'price': 250000000,
            'description': 'Robot pembersih laut otonom dengan AI navigation',
            'image_url': 'https://images.unsplash.com/photo-1754297813436-28cba2aec2da',
            'features': ['Kapasitas sampah 100L', 'Baterai 8 jam operasi', 'AI object detection', 'GPS & sonar navigation'],
            'is_available': True
        },
        {
            'name': 'Sealen Dock',
            'category': 'Aksesori',
            'price': 50000000,
            'description': 'Stasiun pengisian daya dan pembuangan otomatis',
            'image_url': 'https://images.unsplash.com/photo-1660846477676-49d7e2cc6f66',
            'features': ['Fast charging 2 jam', 'Auto waste disposal', 'Weather resistant', 'Solar panel ready'],
            'is_available': True
        },
        {
            'name': 'Sealen Vision AI',
            'category': 'Robot',
            'price': 300000000,
            'description': 'Model premium dengan computer vision dan sensor lingkungan',
            'image_url': 'https://images.unsplash.com/photo-1610093366806-b2907e880fb7',
            'features': ['Advanced AI vision', 'Water quality sensors', 'Deep learning model', 'Cloud analytics'],
            'is_available': True
        },
        {
            'name': 'Spare Parts Kit',
            'category': 'Spare Part',
            'price': 15000000,
            'description': 'Paket lengkap suku cadang untuk pemeliharaan',
            'image_url': 'https://images.unsplash.com/photo-1711062717295-b12347cb17e6',
            'features': ['Motor propeller', 'Filter air', 'Sensor replacement', 'Battery pack'],
            'is_available': True
        }
    ]
    
    for product_data in products_data:
        product = Product.query.filter_by(name=product_data['name']).first()
        if not product:
            product = Product(**product_data)
            db.session.add(product)
    
    db.session.commit()
    
    # Create Sample Robots
    print("Creating sample robots...")
    robots_data = [
        {
            'robot_name': 'CleanBot Alpha',
            'model': 'Sealen CleanBot',
            'model_type': 'CleanBot',
            'status': 'active',
            'battery_lvl': 78,
            'location': 'Jakarta Bay',
            'current_position': {'latitude': -6.2088, 'longitude': 106.8456, 'depth': 2.5},
            'firmware_version': 'v2.1.0'
        },
        {
            'robot_name': 'CleanBot Beta',
            'model': 'Sealen CleanBot',
            'model_type': 'CleanBot',
            'status': 'charging',
            'battery_lvl': 45,
            'location': 'Jakarta Bay',
            'current_position': {'latitude': -6.2100, 'longitude': 106.8500, 'depth': 0},
            'firmware_version': 'v2.1.0'
        },
        {
            'robot_name': 'Vision AI Pro',
            'model': 'Sealen Vision AI',
            'model_type': 'Vision AI',
            'status': 'active',
            'battery_lvl': 92,
            'location': 'Jakarta Bay',
            'current_position': {'latitude': -6.2050, 'longitude': 106.8400, 'depth': 3.0},
            'firmware_version': 'v3.0.0'
        }
    ]
    
    for robot_data in robots_data:
        robot = Robot.query.filter_by(robot_name=robot_data['robot_name']).first()
        if not robot:
            robot = Robot(**robot_data)
            db.session.add(robot)
    
    db.session.commit()
    
    # Create Demo Users
    print("Creating demo users...")
    demo_users = [
        {
            'username': 'admin',
            'email': 'admin@sealen.com',
            'password': 'admin123',
            'full_name': 'Admin User',
            'role_name': 'admin'
        },
        {
            'username': 'operator',
            'email': 'operator@sealen.com',
            'password': 'operator123',
            'full_name': 'Operator User',
            'role_name': 'operator'
        },
        {
            'username': 'customer',
            'email': 'customer@sealen.com',
            'password': 'customer123',
            'full_name': 'Customer User',
            'role_name': 'customer'
        }
    ]
    
    for user_data in demo_users:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            role = Role.query.filter_by(role_name=user_data['role_name']).first()
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=hash_password(user_data['password']),
                full_name=user_data['full_name'],
                role_id=role.role_id
            )
            db.session.add(user)
    
    db.session.commit()
    
    print("Seed data created successfully!")


