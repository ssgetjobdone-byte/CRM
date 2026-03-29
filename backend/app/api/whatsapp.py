diff --git a/backend/app/api/whatsapp.py b/backend/app/api/whatsapp.py
new file mode 100644
index 0000000000000000000000000000000000000000..5be5b27f3ebce3825564733ccdc1ffb08a06ddce
--- /dev/null
+++ b/backend/app/api/whatsapp.py
@@ -0,0 +1,29 @@
+from uuid import UUID
+
+from fastapi import APIRouter, Depends, HTTPException
+from pydantic import BaseModel
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_roles
+from app.db.session import get_db
+from app.models.models import Customer, User, UserRole, Visit
+from app.services.whatsapp import send_welcome_message
+
+router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])
+
+
+class WelcomeRequest(BaseModel):
+    visit_id: UUID
+
+
+@router.post("/send-welcome")
+def send_welcome(payload: WelcomeRequest, _: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT)), db: Session = Depends(get_db)):
+    visit = db.get(Visit, payload.visit_id)
+    if not visit:
+        raise HTTPException(status_code=404, detail="Visit not found")
+    customer = db.get(Customer, visit.customer_id)
+    salesperson = db.get(User, visit.assigned_salesperson_id)
+    result = send_welcome_message(db, visit_id=visit.id, customer_id=customer.id, phone_number=customer.phone_number, salesperson_name=salesperson.name)
+    visit.welcome_message_sent = True
+    db.commit()
+    return result
