diff --git a/backend/alembic/versions/0001_initial.py b/backend/alembic/versions/0001_initial.py
new file mode 100644
index 0000000000000000000000000000000000000000..5a511bca4c8e18086df70c33356c9145c9190150
--- /dev/null
+++ b/backend/alembic/versions/0001_initial.py
@@ -0,0 +1,106 @@
+"""initial
+
+Revision ID: 0001_initial
+Revises:
+Create Date: 2026-03-29
+"""
+from alembic import op
+import sqlalchemy as sa
+from sqlalchemy.dialects import postgresql
+
+revision = '0001_initial'
+down_revision = None
+branch_labels = None
+depends_on = None
+
+
+def upgrade() -> None:
+    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
+    op.create_table('users',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('name', sa.String(100), nullable=False),
+        sa.Column('email', sa.String(255), nullable=False, unique=True),
+        sa.Column('password_hash', sa.String(255), nullable=False),
+        sa.Column('phone', sa.String(20)),
+        sa.Column('role', sa.Enum('ADMIN','CONTACT','SALES','BILLING', name='user_roles'), nullable=False),
+        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+        sa.Column('updated_at', sa.DateTime(), nullable=False),
+        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
+    )
+    op.create_index('ix_users_email', 'users', ['email'])
+    op.create_table('customers',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('phone_number', sa.String(20), nullable=False, unique=True),
+        sa.Column('name', sa.String(120), nullable=False),
+        sa.Column('business_name', sa.String(120)),
+        sa.Column('business_type', sa.String(100)),
+        sa.Column('alternate_phone', sa.String(20)),
+        sa.Column('city', sa.String(100)),
+        sa.Column('notes', sa.Text()),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+        sa.Column('updated_at', sa.DateTime(), nullable=False),
+        sa.Column('created_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
+        sa.Column('updated_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
+    )
+    op.create_index('ix_customers_phone_number', 'customers', ['phone_number'])
+    op.create_table('visits',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('customer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('customers.id'), nullable=False),
+        sa.Column('entry_time', sa.DateTime(), nullable=False),
+        sa.Column('exit_time', sa.DateTime()),
+        sa.Column('entered_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
+        sa.Column('assigned_salesperson_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
+        sa.Column('status', sa.Enum('ASSIGNED','IN_PROGRESS','PURCHASED','LEFT_WITHOUT_PURCHASE','FOLLOW_UP_REQUIRED','CLOSED', name='visit_statuses'), nullable=False),
+        sa.Column('remarks', sa.Text()),
+        sa.Column('follow_up_date', sa.DateTime()),
+        sa.Column('welcome_message_sent', sa.Boolean(), server_default='false', nullable=False),
+        sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+        sa.Column('updated_at', sa.DateTime(), nullable=False),
+    )
+    op.create_table('billing',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('visit_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('visits.id'), nullable=False, unique=True),
+        sa.Column('customer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('customers.id'), nullable=False),
+        sa.Column('invoice_number', sa.String(50), nullable=False),
+        sa.Column('bill_amount', sa.Numeric(12,2), nullable=False),
+        sa.Column('payment_mode', sa.String(50), nullable=False),
+        sa.Column('billing_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
+        sa.Column('billing_time', sa.DateTime(), nullable=False),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+    )
+    op.create_table('whatsapp_logs',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('visit_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('visits.id'), nullable=False),
+        sa.Column('customer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('customers.id'), nullable=False),
+        sa.Column('phone_number', sa.String(20), nullable=False),
+        sa.Column('message_type', sa.String(50), nullable=False),
+        sa.Column('message_content', sa.Text(), nullable=False),
+        sa.Column('status', sa.String(50), nullable=False),
+        sa.Column('provider_response', postgresql.JSONB()),
+        sa.Column('sent_at', sa.DateTime(), nullable=False),
+    )
+    op.create_table('audit_logs',
+        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
+        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
+        sa.Column('action', sa.String(50), nullable=False),
+        sa.Column('entity_type', sa.String(50), nullable=False),
+        sa.Column('entity_id', sa.String(50), nullable=False),
+        sa.Column('old_value_json', postgresql.JSONB()),
+        sa.Column('new_value_json', postgresql.JSONB()),
+        sa.Column('created_at', sa.DateTime(), nullable=False),
+    )
+
+
+def downgrade() -> None:
+    op.drop_table('audit_logs')
+    op.drop_table('whatsapp_logs')
+    op.drop_table('billing')
+    op.drop_table('visits')
+    op.drop_index('ix_customers_phone_number', table_name='customers')
+    op.drop_table('customers')
+    op.drop_index('ix_users_email', table_name='users')
+    op.drop_table('users')
+    sa.Enum(name='visit_statuses').drop(op.get_bind(), checkfirst=True)
+    sa.Enum(name='user_roles').drop(op.get_bind(), checkfirst=True)
