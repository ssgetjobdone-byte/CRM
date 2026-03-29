diff --git a/frontend/app/contacts/page.tsx b/frontend/app/contacts/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..70b2122041e9b91108a20799332f90d09db6d301
--- /dev/null
+++ b/frontend/app/contacts/page.tsx
@@ -0,0 +1,15 @@
+'use client';
+import { useEffect, useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function ContactsPage() {
+  const [rows, setRows] = useState<any[]>([]);
+  const [q, setQ] = useState('');
+  const load = () => api.get('/api/customers', { params: { q } }).then((r) => setRows(r.data));
+  useEffect(load, []);
+  return <LayoutShell><h1 className="text-2xl font-semibold mb-4">Contacts</h1>
+    <div className="flex gap-2 mb-3"><input className="border p-2 rounded" value={q} onChange={e=>setQ(e.target.value)} placeholder="Search"/><button onClick={load} className="bg-blue-600 text-white px-3 rounded">Search</button><a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/export/contacts/excel`} className="px-3 py-2 bg-green-600 text-white rounded">Excel</a><a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/export/contacts/pdf`} className="px-3 py-2 bg-rose-600 text-white rounded">PDF</a></div>
+    <table className="w-full bg-white rounded shadow"><thead><tr><th>Name</th><th>Phone</th><th>Business Type</th><th>City</th></tr></thead><tbody>{rows.map((r)=><tr key={r.id} className="border-t"><td>{r.name}</td><td>{r.phone_number}</td><td>{r.business_type}</td><td>{r.city}</td></tr>)}</tbody></table>
+  </LayoutShell>;
+}
