diff --git a/frontend/app/reports/page.tsx b/frontend/app/reports/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..0fcae49abf8e193c93d7f6ac36f49a077d095b4e
--- /dev/null
+++ b/frontend/app/reports/page.tsx
@@ -0,0 +1,10 @@
+'use client';
+import { useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function ReportsPage(){
+  const [data,setData]=useState<any>(null);
+  const load=async()=>{ const [v,b,c,s]=await Promise.all([api.get('/api/reports/visits'),api.get('/api/reports/billing'),api.get('/api/reports/customers'),api.get('/api/reports/salespersons')]); setData({visits:v.data,billing:b.data,customers:c.data,sales:s.data}); }
+  return <LayoutShell><h1 className='text-2xl font-semibold mb-4'>Reports</h1><div className='flex gap-2 mb-3'><button onClick={load} className='bg-blue-600 text-white px-3 py-2 rounded'>Load Reports</button><a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/export/dashboard/pdf`} className='bg-rose-600 text-white px-3 py-2 rounded'>PDF</a><a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/export/dashboard/excel`} className='bg-green-600 text-white px-3 py-2 rounded'>Excel</a></div><pre className='bg-white p-4 rounded shadow overflow-auto'>{JSON.stringify(data,null,2)}</pre></LayoutShell>
+}
