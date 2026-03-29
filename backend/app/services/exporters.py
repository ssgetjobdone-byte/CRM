diff --git a/backend/app/services/exporters.py b/backend/app/services/exporters.py
new file mode 100644
index 0000000000000000000000000000000000000000..f10342ae8e477b6d32a2540c6d459bd792851699
--- /dev/null
+++ b/backend/app/services/exporters.py
@@ -0,0 +1,32 @@
+from datetime import datetime
+from io import BytesIO
+
+from openpyxl import Workbook
+from weasyprint import HTML
+
+
+def build_excel(sheet_name: str, columns: list[str], rows: list[list]):
+    wb = Workbook()
+    ws = wb.active
+    ws.title = sheet_name[:31]
+    ws.append(columns)
+    for row in rows:
+        ws.append(row)
+    buf = BytesIO()
+    wb.save(buf)
+    buf.seek(0)
+    return buf
+
+
+def build_pdf(title: str, filters: str, columns: list[str], rows: list[list], logo_path: str = "frontend/public/logo.png"):
+    head = "".join([f"<th>{c}</th>" for c in columns])
+    body = "".join(["<tr>" + "".join([f"<td>{str(v)}</td>" for v in r]) + "</tr>" for r in rows])
+    html = f"""
+    <html><body>
+    <div style='display:flex;align-items:center;gap:16px'><img src='{logo_path}' style='height:48px'/><h2>{title}</h2></div>
+    <p>Exported at: {datetime.utcnow().isoformat()} UTC</p>
+    <p>Filters: {filters}</p>
+    <table border='1' cellspacing='0' cellpadding='6'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>
+    </body></html>
+    """
+    return BytesIO(HTML(string=html, base_url=".").write_pdf())
