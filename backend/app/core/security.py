diff --git a/backend/app/core/security.py b/backend/app/core/security.py
new file mode 100644
index 0000000000000000000000000000000000000000..77cf41c4d7521773eb8dc137337ca21efd662d83
--- /dev/null
+++ b/backend/app/core/security.py
@@ -0,0 +1,21 @@
+from datetime import datetime, timedelta, timezone
+from jose import jwt
+from passlib.context import CryptContext
+
+from app.core.config import settings
+
+pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
+
+
+def hash_password(password: str) -> str:
+    return pwd_context.hash(password)
+
+
+def verify_password(plain: str, hashed: str) -> bool:
+    return pwd_context.verify(plain, hashed)
+
+
+def create_access_token(subject: str) -> str:
+    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
+    payload = {"sub": subject, "exp": expire}
+    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
