diff --git a/frontend/types/index.ts b/frontend/types/index.ts
new file mode 100644
index 0000000000000000000000000000000000000000..1b43f63511e4f26525705ad367d2f83d73a25cff
--- /dev/null
+++ b/frontend/types/index.ts
@@ -0,0 +1,9 @@
+export type Role = 'ADMIN' | 'CONTACT' | 'SALES' | 'BILLING';
+
+export interface User {
+  id: string;
+  name: string;
+  email: string;
+  role: Role;
+  is_active: boolean;
+}
