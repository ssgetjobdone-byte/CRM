diff --git a/frontend/components/Logo.tsx b/frontend/components/Logo.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..fac18d8770d2a04aa9f2cada1e4c0fa289958793
--- /dev/null
+++ b/frontend/components/Logo.tsx
@@ -0,0 +1,5 @@
+import Image from 'next/image';
+
+export default function Logo({ className = '' }: { className?: string }) {
+  return <Image src="/logo.png" alt="Kamla Horeca" width={120} height={40} className={className} />;
+}
