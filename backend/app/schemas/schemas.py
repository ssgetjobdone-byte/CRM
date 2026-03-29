diff --git a/backend/app/schemas/schemas.py b/backend/app/schemas/schemas.py
new file mode 100644
index 0000000000000000000000000000000000000000..64e34055b203641231624b73025b6d16d1a268d6
--- /dev/null
+++ b/backend/app/schemas/schemas.py
@@ -0,0 +1,139 @@
+from datetime import datetime
+from decimal import Decimal
+from typing import Any
+from uuid import UUID
+
+from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
+
+from app.models.models import UserRole, VisitStatus
+from app.utils.phone import normalize_phone
+
+
+class TokenResponse(BaseModel):
+    access_token: str
+    token_type: str = "bearer"
+
+
+class UserBase(BaseModel):
+    name: str
+    email: EmailStr
+    phone: str | None = None
+    role: UserRole
+    is_active: bool = True
+
+
+class UserCreate(UserBase):
+    password: str = Field(min_length=8)
+
+
+class UserUpdate(BaseModel):
+    name: str | None = None
+    phone: str | None = None
+    role: UserRole | None = None
+
+
+class UserRead(UserBase):
+    id: UUID
+    created_at: datetime
+    model_config = ConfigDict(from_attributes=True)
+
+
+class CustomerBase(BaseModel):
+    phone_number: str
+    name: str
+    business_name: str | None = None
+    business_type: str | None = None
+    alternate_phone: str | None = None
+    city: str | None = None
+    notes: str | None = None
+
+    @field_validator("phone_number")
+    @classmethod
+    def normalize_customer_phone(cls, value: str):
+        return normalize_phone(value)
+
+
+class CustomerCreate(CustomerBase):
+    pass
+
+
+class CustomerUpdate(BaseModel):
+    name: str | None = None
+    business_name: str | None = None
+    business_type: str | None = None
+    alternate_phone: str | None = None
+    city: str | None = None
+    notes: str | None = None
+
+
+class CustomerRead(CustomerBase):
+    id: UUID
+    created_at: datetime
+    updated_at: datetime
+    model_config = ConfigDict(from_attributes=True)
+
+
+class VisitCreate(BaseModel):
+    customer_id: UUID
+    assigned_salesperson_id: UUID
+    remarks: str | None = None
+
+
+class VisitUpdate(BaseModel):
+    status: VisitStatus | None = None
+    remarks: str | None = None
+    follow_up_date: datetime | None = None
+    exit_time: datetime | None = None
+
+
+class VisitRead(BaseModel):
+    id: UUID
+    customer_id: UUID
+    entry_time: datetime
+    exit_time: datetime | None
+    entered_by_user_id: UUID
+    assigned_salesperson_id: UUID
+    status: VisitStatus
+    remarks: str | None
+    follow_up_date: datetime | None
+    welcome_message_sent: bool
+    model_config = ConfigDict(from_attributes=True)
+
+
+class BillingCreate(BaseModel):
+    visit_id: UUID
+    customer_id: UUID
+    invoice_number: str
+    bill_amount: Decimal = Field(gt=0)
+    payment_mode: str
+
+
+class BillingRead(BaseModel):
+    id: UUID
+    visit_id: UUID
+    customer_id: UUID
+    invoice_number: str
+    bill_amount: Decimal
+    payment_mode: str
+    billing_user_id: UUID
+    billing_time: datetime
+    model_config = ConfigDict(from_attributes=True)
+
+
+class DashboardSummary(BaseModel):
+    today_visitors: int
+    purchased_today: int
+    left_without_purchase_today: int
+    follow_up_required_today: int
+    total_customers: int
+    conversion_rate: float
+    salesperson_performance: list[dict[str, Any]]
+
+
+class DrilldownRow(BaseModel):
+    visit_id: UUID
+    customer_name: str
+    phone_number: str
+    salesperson_name: str
+    status: VisitStatus
+    entry_time: datetime
