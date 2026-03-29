diff --git a/frontend/app/sales/page.tsx b/frontend/app/sales/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..7dcea0b1609acea81362ef574419c41b30e41c48
--- /dev/null
+++ b/frontend/app/sales/page.tsx
@@ -0,0 +1,12 @@
+'use client';
+import { useEffect, useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function SalesPage(){
+  const [rows,setRows]=useState<any[]>([]);
+  const load=()=>api.get('/api/visits').then(r=>setRows(r.data));
+  useEffect(load,[]);
+  const update=async(id:string,status:string)=>{ await api.patch(`/api/visits/${id}`,{status}); load(); };
+  return <LayoutShell><h1 className='text-2xl font-semibold mb-4'>Sales Visits</h1><table className='w-full bg-white shadow rounded'><thead><tr><th>Visit</th><th>Status</th><th>Actions</th></tr></thead><tbody>{rows.map(r=><tr key={r.id} className='border-t'><td>{r.id.slice(0,8)}</td><td>{r.status}</td><td className='space-x-2'><button onClick={()=>update(r.id,'IN_PROGRESS')} className='px-2 py-1 bg-blue-500 text-white rounded'>In Progress</button><button onClick={()=>update(r.id,'FOLLOW_UP_REQUIRED')} className='px-2 py-1 bg-orange-500 text-white rounded'>Follow-up</button><button onClick={()=>update(r.id,'LEFT_WITHOUT_PURCHASE')} className='px-2 py-1 bg-red-500 text-white rounded'>Left</button></td></tr>)}</tbody></table></LayoutShell>
+}
