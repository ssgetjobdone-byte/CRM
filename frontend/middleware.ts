diff --git a/frontend/middleware.ts b/frontend/middleware.ts
new file mode 100644
index 0000000000000000000000000000000000000000..d5ac2c748f694567f617fb51b3d78fe37a34b484
--- /dev/null
+++ b/frontend/middleware.ts
@@ -0,0 +1,21 @@
+import { NextRequest, NextResponse } from 'next/server';
+
+const roleRoutes: Record<string, string[]> = {
+  '/users': ['ADMIN'],
+  '/billing': ['ADMIN', 'BILLING'],
+  '/entry-desk': ['ADMIN', 'CONTACT'],
+  '/sales': ['ADMIN', 'SALES'],
+};
+
+export function middleware(req: NextRequest) {
+  const token = req.cookies.get('token')?.value;
+  const role = req.cookies.get('role')?.value;
+  const path = req.nextUrl.pathname;
+  if (!path.startsWith('/login') && !token) return NextResponse.redirect(new URL('/login', req.url));
+  for (const [prefix, roles] of Object.entries(roleRoutes)) {
+    if (path.startsWith(prefix) && role && !roles.includes(role)) return NextResponse.redirect(new URL('/dashboard', req.url));
+  }
+  return NextResponse.next();
+}
+
+export const config = { matcher: ['/((?!_next|favicon.ico).*)'] };
