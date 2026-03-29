diff --git a/backend/app/api/billing.py b/backend/app/api/billing.py
new file mode 100644
index 0000000000000000000000000000000000000000..3502eb85d5ac848b1232ea2fadace04727f6f870
--- /dev/null
+++ b/backend/app/api/billing.py
@@ -0,0 +1,43 @@
+from uuid import UUID
+
+from fastapi import APIRouter, Depends, HTTPException
+from sqlalchemy import select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_any_logged_in, require_roles
+from app.db.session import get_db
+from app.models.models import Billing, User, UserRole, Visit, VisitStatus
+from app.schemas.schemas import BillingCreate, BillingRead
+from app.services.audit import log_audit
+
+router = APIRouter(prefix="/api/billing", tags=["billing"])
+
+
+@router.get("", response_model=list[BillingRead])
+def list_billing(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    return db.scalars(select(Billing).order_by(Billing.created_at.desc()).limit(200)).all()
+
+
+@router.get("/{billing_id}", response_model=BillingRead)
+def get_billing(billing_id: UUID, _: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    billing = db.get(Billing, billing_id)
+    if not billing:
+        raise HTTPException(status_code=404, detail="Billing record not found")
+    return billing
+
+
+@router.post("", response_model=BillingRead)
+def create_billing(payload: BillingCreate, actor: User = Depends(require_roles(UserRole.ADMIN, UserRole.BILLING)), db: Session = Depends(get_db)):
+    visit = db.get(Visit, payload.visit_id)
+    if not visit:
+        raise HTTPException(status_code=404, detail="Visit not found")
+    if db.scalar(select(Billing).where(Billing.visit_id == payload.visit_id)):
+        raise HTTPException(status_code=409, detail="Billing already exists for this visit")
+
+    billing = Billing(**payload.model_dump(), billing_user_id=actor.id)
+    db.add(billing)
+    visit.status = VisitStatus.PURCHASED
+    log_audit(db, actor, "CREATE", "BILLING", "pending", new=payload.model_dump(mode="json"))
+    db.commit()
+    db.refresh(billing)
+    return billing
