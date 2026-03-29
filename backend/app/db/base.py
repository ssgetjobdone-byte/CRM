diff --git a/backend/app/db/base.py b/backend/app/db/base.py
new file mode 100644
index 0000000000000000000000000000000000000000..fa2b68a5d245bbdde7fbea6b86c9650a584167d6
--- /dev/null
+++ b/backend/app/db/base.py
@@ -0,0 +1,5 @@
+from sqlalchemy.orm import DeclarativeBase
+
+
+class Base(DeclarativeBase):
+    pass
