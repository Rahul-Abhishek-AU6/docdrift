import json, subprocess, tempfile, unittest
from pathlib import Path
CLI=Path(__file__).resolve().parents[1]/"docdrift.py"
PATCH="""diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1 +1 @@
-TOKEN = 'OLD'
+TOKEN = 'API_TOKEN'\n+parser.add_argument('--dry-run')\n+config = {'timeout-ms': 10}
"""
class Tests(unittest.TestCase):
 def test_receipt_and_strict(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d); (r/'docs').mkdir(); (r/'README.md').write_text('Use --dry-run with API_TOKEN.\n'); p=r/'x.patch'; p.write_text(PATCH); out=r/'out.json'
   x=subprocess.run(['python3',str(CLI),str(r),'--patch',str(p),'--json',str(out),'--strict'],text=True,capture_output=True)
   self.assertEqual(x.returncode,2); data=json.loads(out.read_text()); self.assertIn('dry-run',x.stdout); self.assertFalse(any(q['token']=='timeout-ms' and q['documentation_hits'] for q in data['tokens']))
if __name__=='__main__': unittest.main()
