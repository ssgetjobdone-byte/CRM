diff --git a/frontend/app/users/page.tsx b/frontend/app/users/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..3002d74747cca50dc8de1adb6acabd4e0b799785
--- /dev/null
+++ b/frontend/app/users/page.tsx
@@ -0,0 +1,12 @@
+'use client';
+import { useEffect, useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function UsersPage(){
+  const [rows,setRows]=useState<any[]>([]); const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [role,setRole]=useState('CONTACT');
+  const load=()=>api.get('/api/users').then(r=>setRows(r.data));
+  useEffect(load,[]);
+  const add=async()=>{ await api.post('/api/users',{name,email,password:'Welcome@123',role,is_active:true}); load(); };
+  return <LayoutShell><h1 className='text-2xl font-semibold mb-4'>User Management</h1><div className='bg-white p-3 rounded shadow mb-3 flex gap-2'><input className='border p-2 rounded' placeholder='Name' value={name} onChange={e=>setName(e.target.value)}/><input className='border p-2 rounded' placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)}/><select className='border p-2 rounded' value={role} onChange={e=>setRole(e.target.value)}><option>CONTACT</option><option>SALES</option><option>BILLING</option><option>ADMIN</option></select><button onClick={add} className='bg-blue-600 text-white px-3 rounded'>Create</button></div><table className='w-full bg-white rounded shadow'><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Active</th></tr></thead><tbody>{rows.map(r=><tr key={r.id} className='border-t'><td>{r.name}</td><td>{r.email}</td><td>{r.role}</td><td>{String(r.is_active)}</td></tr>)}</tbody></table></LayoutShell>
+}
