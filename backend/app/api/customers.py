diff --git a/backend/app/api/customers.py b/backend/app/api/customers.py
new file mode 100644
index 0000000000000000000000000000000000000000..9cbeb688c0267e13939558dec25e7ed0f24b2f2d
--- /dev/null
+++ b/backend/app/api/customers.py
@@ -0,0 +1,62 @@
+from uuid import UUID
+
+from fastapi import APIRouter, Depends, HTTPException, Query
+from sqlalchemy import or_, select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_any_logged_in, require_roles
+from app.db.session import get_db
+from app.models.models import Customer, User, UserRole
+from app.schemas.schemas import CustomerCreate, CustomerRead, CustomerUpdate
+from app.services.audit import log_audit
+from app.utils.phone import normalize_phone
+
+router = APIRouter(prefix="/api/customers", tags=["customers"])
+
+
+@router.get("", response_model=list[CustomerRead])
+def list_customers(_: User = Depends(require_any_logged_in), q: str | None = None, db: Session = Depends(get_db)):
+    stmt = select(Customer)
+    if q:
+        stmt = stmt.where(or_(Customer.name.ilike(f"%{q}%"), Customer.phone_number.ilike(f"%{q}%")))
+    return db.scalars(stmt.order_by(Customer.created_at.desc()).limit(200)).all()
+
+
+@router.get("/search", response_model=CustomerRead | None)
+def search_customer(phone: str = Query(...), _: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    return db.scalar(select(Customer).where(Customer.phone_number == normalize_phone(phone)))
+
+
+@router.get("/{customer_id}", response_model=CustomerRead)
+def get_customer(customer_id: UUID, _: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    customer = db.get(Customer, customer_id)
+    if not customer:
+        raise HTTPException(status_code=404, detail="Customer not found")
+    return customer
+
+
+@router.post("", response_model=CustomerRead)
+def create_customer(payload: CustomerCreate, actor: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT)), db: Session = Depends(get_db)):
+    if db.scalar(select(Customer).where(Customer.phone_number == payload.phone_number)):
+        raise HTTPException(status_code=409, detail="Phone number already exists")
+    customer = Customer(**payload.model_dump(), created_by=actor.id, updated_by=actor.id)
+    db.add(customer)
+    log_audit(db, actor, "CREATE", "CUSTOMER", "pending", new=payload.model_dump())
+    db.commit()
+    db.refresh(customer)
+    return customer
+
+
+@router.patch("/{customer_id}", response_model=CustomerRead)
+def update_customer(customer_id: UUID, payload: CustomerUpdate, actor: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT)), db: Session = Depends(get_db)):
+    customer = db.get(Customer, customer_id)
+    if not customer:
+        raise HTTPException(status_code=404, detail="Customer not found")
+    before = {"name": customer.name, "city": customer.city, "business_type": customer.business_type}
+    for k, v in payload.model_dump(exclude_unset=True).items():
+        setattr(customer, k, v)
+    customer.updated_by = actor.id
+    log_audit(db, actor, "UPDATE", "CUSTOMER", str(customer_id), old=before, new=payload.model_dump(exclude_unset=True))
+    db.commit()
+    db.refresh(customer)
+    return customer
