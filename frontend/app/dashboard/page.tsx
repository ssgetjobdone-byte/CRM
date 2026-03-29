diff --git a/frontend/app/dashboard/page.tsx b/frontend/app/dashboard/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..cdc63b610c8649ce46dc2abd5c416e214b21a031
--- /dev/null
+++ b/frontend/app/dashboard/page.tsx
@@ -0,0 +1,40 @@
+'use client';
+
+import { useEffect, useState } from 'react';
+import { Bar, BarChart, Pie, PieChart, Tooltip, XAxis, YAxis } from 'recharts';
+import LayoutShell from '@/components/LayoutShell';
+import Logo from '@/components/Logo';
+import api from '@/lib/api';
+
+export default function DashboardPage() {
+  const [summary, setSummary] = useState<any>(null);
+  const [drill, setDrill] = useState<any[]>([]);
+
+  useEffect(() => { api.get('/api/dashboard/summary').then((r) => setSummary(r.data)); }, []);
+  const loadDrill = (params: Record<string, string>) => api.get('/api/dashboard/drilldown', { params }).then((r) => setDrill(r.data));
+
+  return <LayoutShell>
+    <div className="flex items-center justify-between mb-4"><h1 className="text-2xl font-semibold">Dashboard</h1><Logo /></div>
+    {summary && <>
+      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
+        {[['Today Visitors', summary.today_visitors, {}], ['Purchased', summary.purchased_today, { status: 'PURCHASED' }], ['Left W/O Purchase', summary.left_without_purchase_today, { status: 'LEFT_WITHOUT_PURCHASE' }], ['Follow-up', summary.follow_up_required_today, { status: 'FOLLOW_UP_REQUIRED' }]].map((k: any) => (
+          <button key={k[0]} onClick={() => loadDrill(k[2])} className="p-4 rounded bg-white shadow text-left"><p className="text-xs text-gray-500">{k[0]}</p><p className="text-2xl font-bold">{k[1]}</p></button>
+        ))}
+      </div>
+      <div className="grid md:grid-cols-2 gap-4">
+        <div className="bg-white p-4 rounded shadow"><h3 className="font-semibold mb-2">Salesperson Performance</h3>
+          <BarChart width={450} height={250} data={summary.salesperson_performance} onClick={(s: any)=>s?.activePayload?.[0]&&loadDrill({ salesperson_id: s.activePayload[0].payload.salesperson_id })}>
+            <XAxis dataKey="salesperson"/><YAxis/><Tooltip/><Bar dataKey="assigned" fill="#2563eb"/><Bar dataKey="purchased" fill="#16a34a"/>
+          </BarChart>
+        </div>
+        <div className="bg-white p-4 rounded shadow"><h3 className="font-semibold mb-2">Conversion</h3>
+          <PieChart width={450} height={250}><Pie data={[{ name: 'Purchased', value: summary.purchased_today }, { name: 'Non-Purchase', value: Math.max(summary.today_visitors - summary.purchased_today, 0) }]} dataKey="value" nameKey="name" outerRadius={80} onClick={(d:any)=>loadDrill({ status: d.name === 'Purchased' ? 'PURCHASED' : 'LEFT_WITHOUT_PURCHASE' })} /><Tooltip/></PieChart>
+        </div>
+      </div>
+      <div className="bg-white mt-6 p-4 rounded shadow">
+        <h3 className="font-semibold mb-2">Drill-down</h3>
+        <table className="w-full text-sm"><thead><tr className="text-left"><th>Customer</th><th>Phone</th><th>Sales</th><th>Status</th></tr></thead><tbody>{drill.map((r)=><tr key={r.visit_id} className="border-t"><td>{r.customer_name}</td><td>{r.phone_number}</td><td>{r.salesperson_name}</td><td>{r.status}</td></tr>)}</tbody></table>
+      </div>
+    </>}
+  </LayoutShell>;
+}
