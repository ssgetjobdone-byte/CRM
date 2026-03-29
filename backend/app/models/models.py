diff --git a/backend/app/models/models.py b/backend/app/models/models.py
new file mode 100644
index 0000000000000000000000000000000000000000..b79a698c196ef995d31884cc60b5a45c97a0d6ea
--- /dev/null
+++ b/backend/app/models/models.py
@@ -0,0 +1,118 @@
+import enum
+import uuid
+from datetime import datetime
+
+from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text
+from sqlalchemy.dialects.postgresql import JSONB, UUID
+from sqlalchemy.orm import Mapped, mapped_column, relationship
+
+from app.db.base import Base
+
+
+class UserRole(str, enum.Enum):
+    ADMIN = "ADMIN"
+    CONTACT = "CONTACT"
+    SALES = "SALES"
+    BILLING = "BILLING"
+
+
+class VisitStatus(str, enum.Enum):
+    ASSIGNED = "ASSIGNED"
+    IN_PROGRESS = "IN_PROGRESS"
+    PURCHASED = "PURCHASED"
+    LEFT_WITHOUT_PURCHASE = "LEFT_WITHOUT_PURCHASE"
+    FOLLOW_UP_REQUIRED = "FOLLOW_UP_REQUIRED"
+    CLOSED = "CLOSED"
+
+
+class User(Base):
+    __tablename__ = "users"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    name: Mapped[str] = mapped_column(String(100), nullable=False)
+    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
+    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
+    phone: Mapped[str | None] = mapped_column(String(20))
+    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_roles"), nullable=False)
+    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
+    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
+
+
+class Customer(Base):
+    __tablename__ = "customers"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
+    name: Mapped[str] = mapped_column(String(120), nullable=False)
+    business_name: Mapped[str | None] = mapped_column(String(120))
+    business_type: Mapped[str | None] = mapped_column(String(100))
+    alternate_phone: Mapped[str | None] = mapped_column(String(20))
+    city: Mapped[str | None] = mapped_column(String(100))
+    notes: Mapped[str | None] = mapped_column(Text)
+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
+    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
+    updated_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
+
+
+class Visit(Base):
+    __tablename__ = "visits"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
+    entry_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
+    exit_time: Mapped[datetime | None] = mapped_column(DateTime)
+    entered_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
+    assigned_salesperson_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
+    status: Mapped[VisitStatus] = mapped_column(Enum(VisitStatus, name="visit_statuses"), default=VisitStatus.ASSIGNED)
+    remarks: Mapped[str | None] = mapped_column(Text)
+    follow_up_date: Mapped[datetime | None] = mapped_column(DateTime)
+    welcome_message_sent: Mapped[bool] = mapped_column(Boolean, default=False)
+    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
+
+    customer = relationship("Customer")
+
+
+class Billing(Base):
+    __tablename__ = "billing"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    visit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("visits.id"), nullable=False, unique=True)
+    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
+    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
+    bill_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
+    payment_mode: Mapped[str] = mapped_column(String(50), nullable=False)
+    billing_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
+    billing_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+
+
+class WhatsAppLog(Base):
+    __tablename__ = "whatsapp_logs"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    visit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("visits.id"), nullable=False)
+    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
+    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
+    message_type: Mapped[str] = mapped_column(String(50), nullable=False)
+    message_content: Mapped[str] = mapped_column(Text, nullable=False)
+    status: Mapped[str] = mapped_column(String(50), nullable=False)
+    provider_response: Mapped[dict | None] = mapped_column(JSONB)
+    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
+
+
+class AuditLog(Base):
+    __tablename__ = "audit_logs"
+
+    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
+    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
+    action: Mapped[str] = mapped_column(String(50), nullable=False)
+    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
+    entity_id: Mapped[str] = mapped_column(String(50), nullable=False)
+    old_value_json: Mapped[dict | None] = mapped_column(JSONB)
+    new_value_json: Mapped[dict | None] = mapped_column(JSONB)
+    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
