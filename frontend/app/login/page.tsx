diff --git a/frontend/app/login/page.tsx b/frontend/app/login/page.tsx
new file mode 100644
index 0000000000000000000000000000000000000000..12368cf3ceb314f1bacca702b24110563cd191dd
--- /dev/null
+++ b/frontend/app/login/page.tsx
@@ -0,0 +1,41 @@
+'use client';
+
+import { useRouter } from 'next/navigation';
+import { useState } from 'react';
+import Logo from '@/components/Logo';
+import api from '@/lib/api';
+
+export default function LoginPage() {
+  const router = useRouter();
+  const [email, setEmail] = useState('admin@kamla.local');
+  const [password, setPassword] = useState('Admin@1234');
+  const [error, setError] = useState('');
+
+  const login = async () => {
+    try {
+      const form = new URLSearchParams();
+      form.append('username', email);
+      form.append('password', password);
+      const res = await api.post('/api/auth/login', form);
+      localStorage.setItem('token', res.data.access_token);
+      const me = await api.get('/api/auth/me');
+      localStorage.setItem('role', me.data.role);
+      document.cookie = `token=${res.data.access_token}; path=/`;
+      document.cookie = `role=${me.data.role}; path=/`;
+      router.push('/dashboard');
+    } catch {
+      setError('Invalid login');
+    }
+  };
+
+  return <div className="min-h-screen grid place-items-center bg-slate-100">
+    <div className="bg-white p-8 rounded-xl shadow w-full max-w-md">
+      <div className="flex justify-center mb-4"><Logo /></div>
+      <h1 className="text-xl font-semibold text-center mb-4">Kamla Horeca Login</h1>
+      <input className="w-full border p-2 rounded mb-3" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="Email"/>
+      <input type="password" className="w-full border p-2 rounded mb-3" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password"/>
+      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
+      <button onClick={login} className="w-full bg-blue-600 text-white rounded p-2">Sign in</button>
+    </div>
+  </div>;
+}
