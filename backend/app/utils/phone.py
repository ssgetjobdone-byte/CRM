diff --git a/backend/app/utils/phone.py b/backend/app/utils/phone.py
new file mode 100644
index 0000000000000000000000000000000000000000..4729545347a52399781853b017be38833211fda6
--- /dev/null
+++ b/backend/app/utils/phone.py
@@ -0,0 +1,12 @@
+import re
+
+
+def normalize_phone(phone: str) -> str:
+    digits = re.sub(r"\D", "", phone or "")
+    if len(digits) == 10:
+        return f"+91{digits}"
+    if digits.startswith("91") and len(digits) == 12:
+        return f"+{digits}"
+    if phone.startswith("+"):
+        return "+" + re.sub(r"\D", "", phone)
+    return f"+{digits}"
