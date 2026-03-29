diff --git a/frontend/app/page.tsx b/frontend/app/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..6f3853447072e29019086995be4bb324ee59bee4
--- /dev/null
+++ b/frontend/app/page.tsx
@@ -0,0 +1,2 @@
+import { redirect } from 'next/navigation';
+export default function Page(){ redirect('/login'); }
