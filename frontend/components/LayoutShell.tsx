diff --git a/frontend/components/LayoutShell.tsx b/frontend/components/LayoutShell.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..28376136458edda7ff4565b2b312d27c7599a0a8
--- /dev/null
+++ b/frontend/components/LayoutShell.tsx
@@ -0,0 +1,41 @@
+'use client';
+
+import Link from 'next/link';
+import { usePathname, useRouter } from 'next/navigation';
+import Logo from './Logo';
+
+const items = [
+  ['dashboard', '/dashboard', ['ADMIN', 'CONTACT', 'SALES', 'BILLING']],
+  ['contacts', '/contacts', ['ADMIN', 'CONTACT', 'SALES', 'BILLING']],
+  ['entry desk', '/entry-desk', ['ADMIN', 'CONTACT']],
+  ['sales', '/sales', ['ADMIN', 'SALES']],
+  ['billing', '/billing', ['ADMIN', 'BILLING']],
+  ['users', '/users', ['ADMIN']],
+  ['reports', '/reports', ['ADMIN', 'CONTACT', 'SALES', 'BILLING']],
+] as const;
+
+export default function LayoutShell({ children }: { children: React.ReactNode }) {
+  const pathname = usePathname();
+  const role = typeof window !== 'undefined' ? localStorage.getItem('role') : null;
+  const router = useRouter();
+
+  return (
+    <div className="min-h-screen bg-gray-100 flex">
+      <aside className="w-64 bg-white border-r p-4">
+        <Logo className="mb-6" />
+        <nav className="space-y-2">
+          {items.filter((x) => role && x[2].includes(role as any)).map(([label, href]) => (
+            <Link key={href} href={href} className={`block px-3 py-2 rounded ${pathname === href ? 'bg-blue-600 text-white' : 'hover:bg-gray-200'}`}>{label}</Link>
+          ))}
+        </nav>
+      </aside>
+      <main className="flex-1">
+        <header className="bg-white border-b p-4 flex justify-between items-center">
+          <Logo />
+          <button onClick={() => { localStorage.clear(); router.push('/login'); }} className="text-sm px-3 py-1 bg-gray-800 text-white rounded">Logout</button>
+        </header>
+        <section className="p-6">{children}</section>
+      </main>
+    </div>
+  );
+}
