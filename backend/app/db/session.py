diff --git a/backend/app/db/session.py b/backend/app/db/session.py
new file mode 100644
index 0000000000000000000000000000000000000000..1c48e02c65642910e886d8ca5f899ee69470dcab
--- /dev/null
+++ b/backend/app/db/session.py
@@ -0,0 +1,15 @@
+from sqlalchemy import create_engine
+from sqlalchemy.orm import sessionmaker
+
+from app.core.config import settings
+
+engine = create_engine(settings.database_url, pool_pre_ping=True)
+SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
+
+
+def get_db():
+    db = SessionLocal()
+    try:
+        yield db
+    finally:
+        db.close()
