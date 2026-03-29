diff --git a/backend/app/api/users.py b/backend/app/api/users.py
new file mode 100644
index 0000000000000000000000000000000000000000..8483bea7457d8a4b78d10b03ae1220e12bbaabd3
--- /dev/null
+++ b/backend/app/api/users.py
@@ -0,0 +1,74 @@
+from uuid import UUID
+
+from fastapi import APIRouter, Depends, HTTPException
+from sqlalchemy import select
+from sqlalchemy.orm import Session
+
+from app.api.deps import require_roles
+from app.core.security import hash_password
+from app.db.session import get_db
+from app.models.models import User, UserRole
+from app.schemas.schemas import UserCreate, UserRead, UserUpdate
+from app.services.audit import log_audit
+
+router = APIRouter(prefix="/api/users", tags=["users"])
+admin_only = require_roles(UserRole.ADMIN)
+
+
+@router.get("", response_model=list[UserRead])
+def list_users(_: User = Depends(admin_only), db: Session = Depends(get_db)):
+    return db.scalars(select(User).order_by(User.created_at.desc())).all()
+
+
+@router.post("", response_model=UserRead)
+def create_user(payload: UserCreate, actor: User = Depends(admin_only), db: Session = Depends(get_db)):
+    if db.scalar(select(User).where(User.email == payload.email)):
+        raise HTTPException(status_code=409, detail="Email already exists")
+    user = User(
+        name=payload.name,
+        email=payload.email,
+        password_hash=hash_password(payload.password),
+        phone=payload.phone,
+        role=payload.role,
+        is_active=payload.is_active,
+        created_by=actor.id,
+    )
+    db.add(user)
+    log_audit(db, actor, "CREATE", "USER", "pending", new=payload.model_dump(exclude={"password"}))
+    db.commit()
+    db.refresh(user)
+    return user
+
+
+@router.get("/{user_id}", response_model=UserRead)
+def get_user(user_id: UUID, _: User = Depends(admin_only), db: Session = Depends(get_db)):
+    user = db.get(User, user_id)
+    if not user:
+        raise HTTPException(status_code=404, detail="User not found")
+    return user
+
+
+@router.patch("/{user_id}", response_model=UserRead)
+def patch_user(user_id: UUID, payload: UserUpdate, actor: User = Depends(admin_only), db: Session = Depends(get_db)):
+    user = db.get(User, user_id)
+    if not user:
+        raise HTTPException(status_code=404, detail="User not found")
+    before = {"name": user.name, "phone": user.phone, "role": user.role.value}
+    for k, v in payload.model_dump(exclude_unset=True).items():
+        setattr(user, k, v)
+    log_audit(db, actor, "UPDATE", "USER", str(user_id), old=before, new=payload.model_dump(exclude_unset=True))
+    db.commit()
+    db.refresh(user)
+    return user
+
+
+@router.patch("/{user_id}/status", response_model=UserRead)
+def patch_user_status(user_id: UUID, is_active: bool, actor: User = Depends(admin_only), db: Session = Depends(get_db)):
+    user = db.get(User, user_id)
+    if not user:
+        raise HTTPException(status_code=404, detail="User not found")
+    user.is_active = is_active
+    log_audit(db, actor, "STATUS", "USER", str(user_id), old=None, new={"is_active": is_active})
+    db.commit()
+    db.refresh(user)
+    return user
