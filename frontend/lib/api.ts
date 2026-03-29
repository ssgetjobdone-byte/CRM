diff --git a/frontend/lib/api.ts b/frontend/lib/api.ts
new file mode 100644
index 0000000000000000000000000000000000000000..18b0c5c2ee10b277b735509e81d129190a70a3f1
--- /dev/null
+++ b/frontend/lib/api.ts
@@ -0,0 +1,15 @@
+import axios from 'axios';
+
+const api = axios.create({
+  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
+});
+
+api.interceptors.request.use((config) => {
+  if (typeof window !== 'undefined') {
+    const token = localStorage.getItem('token');
+    if (token) config.headers.Authorization = `Bearer ${token}`;
+  }
+  return config;
+});
+
+export default api;
