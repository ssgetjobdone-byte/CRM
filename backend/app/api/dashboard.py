diff --git a/backend/app/api/dashboard.py b/backend/app/api/dashboard.py
new file mode 100644
index 0000000000000000000000000000000000000000..d289d2a52a08ff929f63e3c9b9767c1c713302e4
--- /dev/null
+++ b/backend/app/api/dashboard.py
@@ -0,0 +1,84 @@
+from datetime import date, timedelta
+
+from fastapi import APIRouter, Depends, Query
+from sqlalchemy import and_, case, cast, Date, func, select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_any_logged_in
+from app.db.session import get_db
+from app.models.models import Customer, User, UserRole, Visit, VisitStatus
+from app.schemas.schemas import DashboardSummary, DrilldownRow
+
+router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
+
+
+@router.get("/summary", response_model=DashboardSummary)
+def summary(_: User = Depends(require_any_logged_in), db: Session = Depends(get_db)):
+    today = date.today()
+    visitors = db.scalar(select(func.count()).select_from(Visit).where(func.date(Visit.entry_time) == today, Visit.is_deleted.is_(False))) or 0
+    purchased = db.scalar(select(func.count()).select_from(Visit).where(func.date(Visit.entry_time) == today, Visit.status == VisitStatus.PURCHASED, Visit.is_deleted.is_(False))) or 0
+    left = db.scalar(select(func.count()).select_from(Visit).where(func.date(Visit.entry_time) == today, Visit.status == VisitStatus.LEFT_WITHOUT_PURCHASE, Visit.is_deleted.is_(False))) or 0
+    follow_up = db.scalar(select(func.count()).select_from(Visit).where(func.date(Visit.entry_time) == today, Visit.status == VisitStatus.FOLLOW_UP_REQUIRED, Visit.is_deleted.is_(False))) or 0
+    total_customers = db.scalar(select(func.count()).select_from(Customer)) or 0
+
+    perf_stmt = (
+        select(User.id, User.name, func.count(Visit.id).label("assigned"), func.sum(case((Visit.status == VisitStatus.PURCHASED, 1), else_=0)).label("purchased"))
+        .join(Visit, Visit.assigned_salesperson_id == User.id)
+        .where(User.role == UserRole.SALES)
+        .group_by(User.name)
+    )
+    rows = db.execute(perf_stmt).all()
+    perf = [
+        {
+            "salesperson_id": str(r.id),
+            "salesperson": r.name,
+            "assigned": int(r.assigned or 0),
+            "purchased": int(r.purchased or 0),
+            "conversion": round((r.purchased or 0) * 100 / (r.assigned or 1), 2),
+        }
+        for r in rows
+    ]
+
+    return DashboardSummary(
+        today_visitors=visitors,
+        purchased_today=purchased,
+        left_without_purchase_today=left,
+        follow_up_required_today=follow_up,
+        total_customers=total_customers,
+        conversion_rate=round((purchased * 100 / visitors), 2) if visitors else 0.0,
+        salesperson_performance=perf,
+    )
+
+
+@router.get("/drilldown", response_model=list[DrilldownRow])
+def drilldown(
+    _: User = Depends(require_any_logged_in),
+    status: VisitStatus | None = None,
+    salesperson_id: str | None = None,
+    today_only: bool = Query(True),
+    db: Session = Depends(get_db),
+):
+    stmt = (
+        select(Visit.id, Customer.name, Customer.phone_number, User.name, Visit.status, Visit.entry_time)
+        .join(Customer, Customer.id == Visit.customer_id)
+        .join(User, User.id == Visit.assigned_salesperson_id)
+        .where(Visit.is_deleted.is_(False))
+    )
+    if today_only:
+        stmt = stmt.where(func.date(Visit.entry_time) == date.today())
+    if status:
+        stmt = stmt.where(Visit.status == status)
+    if salesperson_id:
+        stmt = stmt.where(Visit.assigned_salesperson_id == salesperson_id)
+    rows = db.execute(stmt.order_by(Visit.entry_time.desc()).limit(500)).all()
+    return [
+        DrilldownRow(
+            visit_id=r[0],
+            customer_name=r[1],
+            phone_number=r[2],
+            salesperson_name=r[3],
+            status=r[4],
+            entry_time=r[5],
+        )
+        for r in rows
+    ]
