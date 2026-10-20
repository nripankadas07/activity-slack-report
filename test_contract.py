import copy,itertools,json,pathlib,random,sqlite3,subprocess,sys,tempfile,unittest
from activity_slack_report import analyze
ROOT=pathlib.Path(__file__).absolute().parent
def example():return json.loads((ROOT/'example.json').read_text())
class Contract(unittest.TestCase):
    def test_strict_cli_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)/'bad.json'
            for raw in ('{', '{"x":1,"x":2}', '{"x":NaN}', '{}', ' '*1048577):
                p.write_text(raw);r=subprocess.run([sys.executable,str(ROOT/'activity_slack_report.py'),str(p)],text=True,capture_output=True,timeout=5)
                self.assertEqual(r.returncode,2);self.assertTrue(r.stderr);self.assertFalse(r.stdout)
    def test_input_unchanged(self):
        x=example();saved=copy.deepcopy(x);analyze(x);self.assertEqual(x,saved)

    def test_timing_and_lag(self):
        r=analyze(example());self.assertEqual(r['minimum_finish'],10);self.assertEqual(r['longest_chain'],['buy','build','review'])
        t={x['id']:x for x in r['tasks']};self.assertEqual(t['design']['total_slack'],4);self.assertEqual(t['design']['free_slack'],4);self.assertEqual(t['build']['earliest_start'],6)
    def test_negative_slack_deadline(self):
        d=example();d['deadline']=8;r=analyze(d);self.assertFalse(r['deadline_feasible']);self.assertEqual(r['exit_code'],1);self.assertEqual(min(t['total_slack'] for t in r['tasks']),-2)
    def test_cycle(self):
        d=example();d['links'].append({'from':'review','to':'buy','lag':0})
        with self.assertRaisesRegex(ValueError,'cycle'):analyze(d)
    def test_unknown_duplicate_and_boolean(self):
        for field,bad in [('tasks',[{'id':'a','duration':True}]),('links',[{'from':'absent','to':'buy','lag':0}])]:
            d=example();d[field]=bad
            with self.assertRaises(ValueError):analyze(d)
        d=example();d['links']*=2
        with self.assertRaises(ValueError):analyze(d)
    def test_exhaustive_small_dag_path_oracle(self):
        pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
        for mask in range(64):
            durations=[0,2,1,3];edges=[e for i,e in enumerate(pairs) if mask>>i&1]
            d={'tasks':[{'id':str(i),'duration':n} for i,n in enumerate(durations)],'links':[{'from':str(a),'to':str(b),'lag':1} for a,b in edges]}
            # Enumerate every directed path instead of using a forward/backward recurrence.
            paths=[]
            def walk(path):
                paths.append(path)
                for a,b in edges:
                    if a==path[-1]:walk(path+[b])
            for i in range(4):walk([i])
            length=lambda p:sum(durations[i] for i in p)+len(p)-1
            finish=max(map(length,paths));r=analyze(d);self.assertEqual(r['minimum_finish'],finish)
            for t in r['tasks']:
                i=int(t['id']);self.assertEqual(t['total_slack'],finish-max(length(p) for p in paths if i in p))
    def test_disconnected_zero_milestone(self):
        d={'tasks':[{'id':'a','duration':0},{'id':'b','duration':2}],'links':[]};r=analyze(d);self.assertEqual(r['tasks'][0]['total_slack'],2)

if __name__ == '__main__':unittest.main()
