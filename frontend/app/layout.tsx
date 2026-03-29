diff --git a/frontend/app/layout.tsx b/frontend/app/layout.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..0e080b1c39a256e141e4d0b19ccdc9929891fe3a
--- /dev/null
+++ b/frontend/app/layout.tsx
@@ -0,0 +1,9 @@
+import './globals.css';
+
+export default function RootLayout({ children }: { children: React.ReactNode }) {
+  return (
+    <html lang="en">
+      <body>{children}</body>
+    </html>
+  );
+}
