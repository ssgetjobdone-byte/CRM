diff --git a/backend/seed.py b/backend/seed.py
new file mode 100644
index 0000000000000000000000000000000000000000..ad438d91c6498591a65bf061c334fd4560ffe2a1
--- /dev/null
+++ b/backend/seed.py
@@ -0,0 +1,45 @@
+from datetime import datetime, timedelta
+from decimal import Decimal
+
+from sqlalchemy import select
+
+from app.core.security import hash_password
+from app.db.base import Base
+from app.db.session import SessionLocal, engine
+from app.models.models import Billing, Customer, User, UserRole, Visit, VisitStatus
+from app.utils.phone import normalize_phone
+
+Base.metadata.create_all(bind=engine)
+db = SessionLocal()
+
+if not db.scalar(select(User).where(User.email == "admin@kamla.local")):
+    admin = User(name="Admin User", email="admin@kamla.local", password_hash=hash_password("Admin@1234"), role=UserRole.ADMIN, is_active=True)
+    contact = User(name="Entry Desk", email="contact@kamla.local", password_hash=hash_password("Contact@1234"), role=UserRole.CONTACT, is_active=True)
+    sales1 = User(name="Ravi Sales", email="sales1@kamla.local", password_hash=hash_password("Sales@1234"), role=UserRole.SALES, is_active=True)
+    sales2 = User(name="Priya Sales", email="sales2@kamla.local", password_hash=hash_password("Sales@1234"), role=UserRole.SALES, is_active=True)
+    biller = User(name="Billing Desk", email="billing@kamla.local", password_hash=hash_password("Billing@1234"), role=UserRole.BILLING, is_active=True)
+    db.add_all([admin, contact, sales1, sales2, biller])
+    db.flush()
+
+    customers = []
+    for i in range(10):
+        c = Customer(name=f"Customer {i+1}", phone_number=normalize_phone(f"9876500{i:03d}"), business_type="Restaurant" if i % 2 == 0 else "Cafe", city="Pune", created_by=admin.id, updated_by=admin.id)
+        customers.append(c)
+    db.add_all(customers)
+    db.flush()
+
+    visits = []
+    for i in range(15):
+        v = Visit(customer_id=customers[i % 10].id, entered_by_user_id=contact.id, assigned_salesperson_id=sales1.id if i % 2 == 0 else sales2.id, status=VisitStatus.PURCHASED if i < 5 else VisitStatus.ASSIGNED, entry_time=datetime.utcnow() - timedelta(days=i % 5))
+        visits.append(v)
+    db.add_all(visits)
+    db.flush()
+
+    for i in range(5):
+        b = Billing(visit_id=visits[i].id, customer_id=visits[i].customer_id, invoice_number=f"INV-10{i}", bill_amount=Decimal("1000.00") + i * 50, payment_mode="UPI", billing_user_id=biller.id)
+        db.add(b)
+
+    db.commit()
+    print("Seeded successfully")
+else:
+    print("Seed data already exists")
