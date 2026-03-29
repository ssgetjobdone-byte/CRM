diff --git a/backend/app/services/whatsapp.py b/backend/app/services/whatsapp.py
new file mode 100644
index 0000000000000000000000000000000000000000..81f16fe2992da0030d3a4f109dfa6f97b2f3e994
--- /dev/null
+++ b/backend/app/services/whatsapp.py
@@ -0,0 +1,27 @@
+from sqlalchemy.orm import Session
+
+from app.core.config import settings
+from app.models.models import WhatsAppLog
+
+
+def send_welcome_message(db: Session, *, visit_id, customer_id, phone_number: str, salesperson_name: str) -> dict:
+    content = f"Welcome to our shop, {salesperson_name} will assist you. Please give us your feedback"
+    if settings.whatsapp_provider == "mock":
+        status = "MOCK_SENT"
+        response = {"provider": "mock", "ok": True}
+    else:
+        status = "PENDING_PROVIDER"
+        response = {"provider": settings.whatsapp_provider, "message": "Implement provider call"}
+
+    db.add(
+        WhatsAppLog(
+            visit_id=visit_id,
+            customer_id=customer_id,
+            phone_number=phone_number,
+            message_type="WELCOME",
+            message_content=content,
+            status=status,
+            provider_response=response,
+        )
+    )
+    return {"status": status, "message": content, "provider_response": response}
