diff --git a/backend/app/api/reports.py b/backend/app/api/reports.py
new file mode 100644
index 0000000000000000000000000000000000000000..f9f72db4d95b040174e874606ebed98329b55eb6
--- /dev/null
+++ b/backend/app/api/reports.py
@@ -0,0 +1,33 @@
+from fastapi import APIRouter, Depends
+from sqlalchemy import func, select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_any_logged_in
+from app.db.session import get_db
+from app.models.models import Billing, Customer, User, Visit
+
+router = APIRouter(prefix="/api/reports", tags=["reports"])
+
+
+@router.get("/visits")
+def visits_report(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    rows = db.execute(select(Visit.status, func.count()).group_by(Visit.status)).all()
+    return [{"status": r[0], "count": r[1]} for r in rows]
+
+
+@router.get("/billing")
+def billing_report(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    total = db.scalar(select(func.sum(Billing.bill_amount))) or 0
+    return {"total_bill_amount": float(total)}
+
+
+@router.get("/customers")
+def customers_report(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    by_type = db.execute(select(Customer.business_type, func.count()).group_by(Customer.business_type)).all()
+    return [{"business_type": r[0] or "Unknown", "count": r[1]} for r in by_type]
+
+
+@router.get("/salespersons")
+def salespersons_report(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    rows = db.execute(select(User.name, func.count(Visit.id)).join(Visit, Visit.assigned_salesperson_id == User.id).group_by(User.name)).all()
+    return [{"salesperson": r[0], "visits": r[1]} for r in rows]
