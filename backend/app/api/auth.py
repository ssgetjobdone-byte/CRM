diff --git a/backend/app/api/auth.py b/backend/app/api/auth.py
new file mode 100644
index 0000000000000000000000000000000000000000..0c7420a6889616f1fb60e64d83684c16ff6b78bc
--- /dev/null
+++ b/backend/app/api/auth.py
@@ -0,0 +1,27 @@
+from fastapi import APIRouter, Depends, HTTPException
+from fastapi.security import OAuth2PasswordRequestForm
+from sqlalchemy import select
+from sqlalchemy.orm import Session
+
+from app.api.deps import get_current_user
+from app.core.security import create_access_token, verify_password
+from app.db.session import get_db
+from app.models.models import User
+from app.schemas.schemas import TokenResponse, UserRead
+
+router = APIRouter(prefix="/api/auth", tags=["auth"])
+
+
+@router.post("/login", response_model=TokenResponse)
+def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
+    user = db.scalar(select(User).where(User.email == form_data.username))
+    if not user or not verify_password(form_data.password, user.password_hash):
+        raise HTTPException(status_code=401, detail="Invalid credentials")
+    if not user.is_active:
+        raise HTTPException(status_code=403, detail="Inactive user")
+    return TokenResponse(access_token=create_access_token(str(user.id)))
+
+
+@router.get("/me", response_model=UserRead)
+def me(current: User = Depends(get_current_user)):
+    return current
