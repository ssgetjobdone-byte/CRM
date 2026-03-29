diff --git a/backend/app/services/audit.py b/backend/app/services/audit.py
new file mode 100644
index 0000000000000000000000000000000000000000..26e9a15e4ed1e06f3cba7423186b64ad0819c5e1
--- /dev/null
+++ b/backend/app/services/audit.py
@@ -0,0 +1,16 @@
+from sqlalchemy.orm import Session
+
+from app.models.models import AuditLog, User
+
+
+def log_audit(db: Session, actor: User, action: str, entity_type: str, entity_id: str, old=None, new=None):
+    db.add(
+        AuditLog(
+            user_id=actor.id,
+            action=action,
+            entity_type=entity_type,
+            entity_id=entity_id,
+            old_value_json=old,
+            new_value_json=new,
+        )
+    )
