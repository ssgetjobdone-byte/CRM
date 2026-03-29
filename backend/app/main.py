diff --git a/backend/app/main.py b/backend/app/main.py
new file mode 100644
index 0000000000000000000000000000000000000000..d279d93c1b1ac8f88df40bcdc1c57425b6b7d3ac
--- /dev/null
+++ b/backend/app/main.py
@@ -0,0 +1,23 @@
+from fastapi import FastAPI
+from fastapi.middleware.cors import CORSMiddleware
+
+from app.api import auth, billing, customers, dashboard, exports, reports, users, visits, whatsapp
+from app.core.config import settings
+
+app = FastAPI(title=settings.app_name)
+
+app.add_middleware(
+    CORSMiddleware,
+    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
+    allow_credentials=True,
+    allow_methods=["*"],
+    allow_headers=["*"],
+)
+
+for router in [auth.router, users.router, customers.router, visits.router, billing.router, dashboard.router, reports.router, exports.router, whatsapp.router]:
+    app.include_router(router)
+
+
+@app.get("/health")
+def health():
+    return {"status": "ok"}
