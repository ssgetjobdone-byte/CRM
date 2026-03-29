diff --git a/backend/app/api/exports.py b/backend/app/api/exports.py
new file mode 100644
index 0000000000000000000000000000000000000000..630f1ac835769ff37c8fa7397ce8809d14006bde
--- /dev/null
+++ b/backend/app/api/exports.py
@@ -0,0 +1,75 @@
+from fastapi import APIRouter, Depends
+from fastapi.responses import StreamingResponse
+from sqlalchemy import select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_roles
+from app.db.session import get_db
+from app.models.models import Billing, Customer, User, UserRole, Visit
+from app.services.exporters import build_excel, build_pdf
+
+router = APIRouter(prefix="/api/export", tags=["exports"])
+
+
+def file_response(buf, filename, mime):
+    return StreamingResponse(buf, media_type=mime, headers={"Content-Disposition": f"attachment; filename={filename}"})
+
+
+@router.get("/contacts/excel")
+def contacts_excel(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Customer.name, Customer.phone_number, Customer.business_type, Customer.city)).all()
+    return file_response(build_excel("contacts", ["Name", "Phone", "Business Type", "City"], [list(r) for r in rows]), "contacts.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
+
+
+@router.get("/contacts/pdf")
+def contacts_pdf(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Customer.name, Customer.phone_number, Customer.business_type, Customer.city)).all()
+    return file_response(build_pdf("Contacts Report", "all", ["Name", "Phone", "Business Type", "City"], [list(r) for r in rows]), "contacts.pdf", "application/pdf")
+
+
+@router.get("/visits/excel")
+def visits_excel(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Visit.id, Visit.status, Visit.entry_time)).all()
+    return file_response(build_excel("visits", ["Visit ID", "Status", "Entry Time"], [list(r) for r in rows]), "visits.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
+
+
+@router.get("/visits/pdf")
+def visits_pdf(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Visit.id, Visit.status, Visit.entry_time)).all()
+    return file_response(build_pdf("Visits Report", "all", ["Visit ID", "Status", "Entry Time"], [list(r) for r in rows]), "visits.pdf", "application/pdf")
+
+
+@router.get("/billing/excel")
+def billing_excel(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Billing.invoice_number, Billing.bill_amount, Billing.payment_mode, Billing.billing_time)).all()
+    return file_response(build_excel("billing", ["Invoice", "Amount", "Payment", "Time"], [list(r) for r in rows]), "billing.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
+
+
+@router.get("/billing/pdf")
+def billing_pdf(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Billing.invoice_number, Billing.bill_amount, Billing.payment_mode, Billing.billing_time)).all()
+    return file_response(build_pdf("Billing Report", "all", ["Invoice", "Amount", "Payment", "Time"], [list(r) for r in rows]), "billing.pdf", "application/pdf")
+
+
+@router.get("/users/excel")
+def users_excel(_: User = Depends(require_roles(UserRole.ADMIN)), db: Session = Depends(get_db)):
+    rows = db.execute(select(User.name, User.email, User.role, User.is_active)).all()
+    return file_response(build_excel("users", ["Name", "Email", "Role", "Active"], [list(r) for r in rows]), "users.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
+
+
+@router.get("/users/pdf")
+def users_pdf(_: User = Depends(require_roles(UserRole.ADMIN)), db: Session = Depends(get_db)):
+    rows = db.execute(select(User.name, User.email, User.role, User.is_active)).all()
+    return file_response(build_pdf("Users Report", "all", ["Name", "Email", "Role", "Active"], [list(r) for r in rows]), "users.pdf", "application/pdf")
+
+
+@router.get("/dashboard/excel")
+def dashboard_excel(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Visit.status, Visit.entry_time)).all()
+    return file_response(build_excel("dashboard", ["Status", "Entry Time"], [list(r) for r in rows]), "dashboard.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
+
+
+@router.get("/dashboard/pdf")
+def dashboard_pdf(_: User = Depends(require_roles(UserRole.ADMIN, UserRole.CONTACT, UserRole.SALES, UserRole.BILLING)), db: Session = Depends(get_db)):
+    rows = db.execute(select(Visit.status, Visit.entry_time)).all()
+    return file_response(build_pdf("Dashboard Summary", "all", ["Status", "Entry Time"], [list(r) for r in rows]), "dashboard.pdf", "application/pdf")
