diff --git a/frontend/app/entry-desk/page.tsx b/frontend/app/entry-desk/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..f1ce363bff048afaf6fa0317e117cdb1d884652c
--- /dev/null
+++ b/frontend/app/entry-desk/page.tsx
@@ -0,0 +1,27 @@
+'use client';
+import { useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function EntryDeskPage() {
+  const [phone, setPhone] = useState('');
+  const [customer, setCustomer] = useState<any>(null);
+  const [salesperson, setSalesperson] = useState('');
+  const [salesUsers, setSalesUsers] = useState<any[]>([]);
+  useState(() => { api.get('/api/users').then(r=>setSalesUsers(r.data.filter((x:any)=>x.role==='SALES'))).catch(()=>{}); });
+
+  const lookup = async () => {
+    const res = await api.get('/api/customers/search', { params: { phone } });
+    setCustomer(res.data ?? { phone_number: phone, name: '' });
+  };
+  const save = async () => {
+    const cust = customer.id ? (await api.patch(`/api/customers/${customer.id}`, customer)).data : (await api.post('/api/customers', customer)).data;
+    await api.post('/api/visits', { customer_id: cust.id, assigned_salesperson_id: salesperson });
+    alert('Visit created');
+  };
+
+  return <LayoutShell><h1 className="text-2xl font-semibold mb-4">Entry Desk</h1>
+    <div className="bg-white p-4 rounded shadow max-w-2xl space-y-3"><div className="flex gap-2"><input value={phone} onChange={e=>setPhone(e.target.value)} className="border p-2 rounded flex-1" placeholder="Phone"/><button onClick={lookup} className="bg-blue-600 text-white px-3 rounded">Lookup</button></div>
+    {customer && <><input className="border p-2 w-full rounded" placeholder="Name" value={customer.name||''} onChange={e=>setCustomer({...customer,name:e.target.value})}/><input className="border p-2 w-full rounded" placeholder="Business Name" value={customer.business_name||''} onChange={e=>setCustomer({...customer,business_name:e.target.value})}/><select className="border p-2 rounded w-full" value={salesperson} onChange={e=>setSalesperson(e.target.value)}><option value=''>Assign salesperson</option>{salesUsers.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}</select><button onClick={save} className="bg-green-600 text-white px-3 py-2 rounded">Create Visit + Send Welcome</button></>}
+    </div></LayoutShell>;
+}
