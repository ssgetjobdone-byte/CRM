diff --git a/frontend/app/billing/page.tsx b/frontend/app/billing/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..108d255f37037041281a26fe7809c5bd5ed7dde8
--- /dev/null
+++ b/frontend/app/billing/page.tsx
@@ -0,0 +1,10 @@
+'use client';
+import { useState } from 'react';
+import LayoutShell from '@/components/LayoutShell';
+import api from '@/lib/api';
+
+export default function BillingPage(){
+  const [visitId,setVisitId]=useState(''); const [customerId,setCustomerId]=useState(''); const [invoice,setInvoice]=useState(''); const [amount,setAmount]=useState('');
+  const submit=async()=>{ await api.post('/api/billing',{visit_id:visitId,customer_id:customerId,invoice_number:invoice,bill_amount:Number(amount),payment_mode:'UPI'}); alert('Billing created'); };
+  return <LayoutShell><h1 className='text-2xl font-semibold mb-4'>Billing</h1><div className='bg-white rounded shadow p-4 max-w-xl space-y-2'><input className='border p-2 rounded w-full' placeholder='Visit ID' value={visitId} onChange={e=>setVisitId(e.target.value)}/><input className='border p-2 rounded w-full' placeholder='Customer ID' value={customerId} onChange={e=>setCustomerId(e.target.value)}/><input className='border p-2 rounded w-full' placeholder='Invoice' value={invoice} onChange={e=>setInvoice(e.target.value)}/><input className='border p-2 rounded w-full' placeholder='Amount' value={amount} onChange={e=>setAmount(e.target.value)}/><button onClick={submit} className='bg-green-600 text-white px-3 py-2 rounded'>Create Billing</button></div></LayoutShell>
+}
