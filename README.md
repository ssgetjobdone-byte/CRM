diff --git a/README.md b/README.md
index a777f590a626a5ac48561c3b493ce77d4a2a52a6..9ece6d656c0fa6488024c6eec65da5e71ff3a676 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,107 @@
-# CRM
\ No newline at end of file
+# Kamla Horeca Customer Visit Tracking System
+
+Production-grade internal business application for Kamla Horeca to manage customer footfall, sales assignment, billing, reporting, exports, and operational analytics.
+
+## Architecture
+- **Frontend**: Next.js + React + TypeScript + Tailwind CSS + Recharts (deploy on Vercel)
+- **Backend**: FastAPI + SQLAlchemy + JWT Auth + role-based authorization
+- **Database**: PostgreSQL (Supabase-compatible)
+- **Migrations**: Alembic
+- **Exports**: WeasyPrint (PDF), openpyxl (Excel)
+- **Messaging**: WhatsApp integration service with mock mode and persisted logs
+
+## Repository Structure
+
+```text
+backend/
+  app/
+    api/               # REST routes
+    core/              # config + security
+    db/                # SQLAlchemy base/session
+    models/            # ORM models + enums
+    schemas/           # Pydantic schemas
+    services/          # audit/whatsapp/export service layer
+    utils/             # phone normalization
+    main.py
+  alembic/
+  seed.py
+frontend/
+  app/
+    login dashboard contacts entry-desk sales billing users reports
+  components/
+  lib/
+  types/
+  public/logo.png
+```
+
+## Core Features Delivered
+- JWT login (`/api/auth/login`) and profile (`/api/auth/me`)
+- Role-based access for Admin / Contact / Sales / Billing
+- Customer master (unique normalized phone, no duplicates)
+- Visit lifecycle tracking (assigned, in-progress, purchased, follow-up, left without purchase)
+- Billing linked 1:1 to visit and auto-updates visit status to `PURCHASED`
+- Dashboard KPIs + charts + API-backed drill-down
+- Reports endpoints and exports for contacts/visits/billing/users/dashboard in PDF + Excel
+- WhatsApp welcome service layer with provider env config + persisted whatsapp_logs
+- Audit logs for create/update/status operations
+- Soft delete flag on visits (`is_deleted`)
+- Logo used in login, sidebar/header, dashboard, and PDF export template
+
+## Environment Variables
+
+### Backend (`backend/.env`)
+```bash
+DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/kamla_horeca
+JWT_SECRET=super-secret-change-me
+JWT_ALGORITHM=HS256
+ACCESS_TOKEN_EXPIRE_MINUTES=720
+CORS_ORIGINS=http://localhost:3000
+WHATSAPP_PROVIDER=mock
+WHATSAPP_API_URL=
+WHATSAPP_API_KEY=
+```
+
+### Frontend (`frontend/.env.local`)
+```bash
+NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
+```
+
+## Backend Setup
+```bash
+cd backend
+python -m venv .venv
+source .venv/bin/activate
+pip install -r requirements.txt
+alembic upgrade head
+python seed.py
+uvicorn app.main:app --reload --port 8000
+```
+
+## Frontend Setup
+```bash
+cd frontend
+npm install
+npm run dev
+```
+
+## Seeded Credentials
+- Admin: `admin@kamla.local` / `Admin@1234`
+- Contact: `contact@kamla.local` / `Contact@1234`
+- Sales: `sales1@kamla.local` / `Sales@1234`
+- Sales: `sales2@kamla.local` / `Sales@1234`
+- Billing: `billing@kamla.local` / `Billing@1234`
+
+Seed data includes: 10 customers, 15 visits, 5 billing records.
+
+## API Map
+Auth, Users, Customers, Visits, Billing, Dashboard, Reports, Exports, WhatsApp endpoints implemented under `/api/*` as requested.
+
+## Deployment Notes
+- **Frontend**: Deploy `frontend` to Vercel; set `NEXT_PUBLIC_API_BASE_URL`.
+- **Backend**: Deploy FastAPI app (Render/Fly/Railway/VM) using `uvicorn app.main:app`.
+- **Database**: Point `DATABASE_URL` to Supabase PostgreSQL connection string.
+- Enable CORS origin to Vercel frontend domain.
+
+## Notes
+- Replace `frontend/public/logo.png` with the final uploaded Kamla Horeca logo if needed.
+- WhatsApp provider integration hook is in service layer; default is mock mode with logs.
