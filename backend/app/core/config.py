diff --git a/backend/app/core/config.py b/backend/app/core/config.py
new file mode 100644
index 0000000000000000000000000000000000000000..ecb55b2fb506c75f30448be18922fa7a3cb793cc
--- /dev/null
+++ b/backend/app/core/config.py
@@ -0,0 +1,20 @@
+from pydantic_settings import BaseSettings, SettingsConfigDict
+
+
+class Settings(BaseSettings):
+    app_name: str = "Kamla Horeca API"
+    environment: str = "development"
+    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/kamla_horeca"
+    jwt_secret: str = "change-me"
+    jwt_algorithm: str = "HS256"
+    access_token_expire_minutes: int = 60 * 12
+    cors_origins: str = "http://localhost:3000"
+
+    whatsapp_provider: str = "mock"
+    whatsapp_api_url: str = ""
+    whatsapp_api_key: str = ""
+
+    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
+
+
+settings = Settings()
