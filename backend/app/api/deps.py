diff --git a/backend/app/api/deps.py b/backend/app/api/deps.py
new file mode 100644
index 0000000000000000000000000000000000000000..3f1e6b9730dadd12fe6425b851dc92308b27f25f
--- /dev/null
+++ b/backend/app/api/deps.py
@@ -0,0 +1,43 @@
+from typing import Iterable
+from uuid import UUID
+
+from fastapi import Depends, HTTPException, status
+from fastapi.security import OAuth2PasswordBearer
+from jose import JWTError, jwt
+from sqlalchemy.orm import Session
+
+from app.core.config import settings
+from app.db.session import get_db
+from app.models.models import User, UserRole
+
+oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
+
+
+def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
+    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
+    try:
+        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
+        sub = payload.get("sub")
+        if not sub:
+            raise credentials_exception
+        user_id = UUID(sub)
+    except (JWTError, ValueError):
+        raise credentials_exception
+
+    user = db.get(User, user_id)
+    if not user or not user.is_active:
+        raise credentials_exception
+    return user
+
+
+def require_roles(*roles: UserRole):
+    def checker(user: User = Depends(get_current_user)) -> User:
+        if roles and user.role not in set(roles):
+            raise HTTPException(status_code=403, detail="Insufficient permissions")
+        return user
+
+    return checker
+
+
+def require_any_logged_in(user: User = Depends(get_current_user)) -> User:
+    return user
