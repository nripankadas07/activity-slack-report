"""Explain finish-to-start activity slack in a bounded acyclic project."""
import argparse, json, pathlib, sys

def need(ok, message):
    if not ok: raise ValueError(message)

def integer(n, low=0, high=10**9):
    need(type(n) is int and low <= n <= high, 'integer outside supported range')
    return n

def ident(s):
    need(type(s) is str and 0 < len(s) <= 80, 'invalid identifier')
    return s

def fields(obj, required, optional=()):
    need(type(obj) is dict and set(required) <= set(obj) <= set(required)|set(optional), 'missing or unknown fields')

def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out, 'duplicate JSON key')
        out[k]=v
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=pathlib.Path);a=p.parse_args()
    try:
        with a.input.open('rb') as f: raw=f.read(1048577)
        need(len(raw) <= 1048576, 'input exceeds 1 MiB')
        doc=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
        out=analyze(doc);print(json.dumps(out,ensure_ascii=True,sort_keys=True));return out.get('exit_code',0)
    except (ValueError,OSError,UnicodeError,RecursionError,OverflowError) as e:
        print(str(e),file=sys.stderr);return 2


import heapq

def analyze(doc):
    fields(doc,('tasks','links'),('deadline',))
    need(type(doc['tasks']) is list and 1<=len(doc['tasks'])<=200, 'expected 1..200 tasks')
    tasks={}
    for t in doc['tasks']:
        fields(t,('id','duration'));k=ident(t['id']);need(k not in tasks,'duplicate task');tasks[k]=integer(t['duration'])
    need(type(doc['links']) is list and len(doc['links'])<=2000,'too many links')
    pred={k:[] for k in tasks};succ={k:[] for k in tasks};seen=set()
    for e in doc['links']:
        fields(e,('from','to','lag'));a,b=ident(e['from']),ident(e['to']);lag=integer(e['lag'])
        need(a in tasks and b in tasks and (a,b) not in seen,'unknown or duplicate dependency');seen.add((a,b));pred[b].append((a,lag));succ[a].append((b,lag))
    degree={k:len(v) for k,v in pred.items()};queue=[k for k in tasks if not degree[k]];heapq.heapify(queue);order=[]
    while queue:
        k=heapq.heappop(queue);order.append(k)
        for b,_ in sorted(succ[k]):
            degree[b]-=1
            if degree[b]==0:heapq.heappush(queue,b)
    need(len(order)==len(tasks),'dependency cycle; no schedule emitted')
    es={};ef={};parents={}
    for k in order:
        es[k]=max([ef[a]+lag for a,lag in pred[k]]+[0]);ef[k]=es[k]+tasks[k]
        parents[k]=sorted(a for a,lag in pred[k] if ef[a]+lag==es[k])
    finish=max(ef.values());deadline=integer(doc.get('deadline',finish),0,10**15);ls={};lf={}
    for k in reversed(order):
        lf[k]=min([ls[b]-lag for b,lag in succ[k]]+[deadline]);ls[k]=lf[k]-tasks[k]
    # One deterministic longest-chain witness, independent of any supplied deadline.
    k=min(k for k in tasks if ef[k]==finish);chain=[k]
    while parents[k]:k=parents[k][0];chain.append(k)
    chain.reverse()
    rows=[{'id':k,'duration':tasks[k],'earliest_start':es[k],'earliest_finish':ef[k],'latest_start':ls[k],'latest_finish':lf[k],'total_slack':ls[k]-es[k],'free_slack':min([es[b]-ef[k]-lag for b,lag in succ[k]]+[finish-ef[k]]),'binding_predecessors':parents[k]} for k in sorted(tasks)]
    return {'minimum_finish':finish,'deadline':deadline,'deadline_feasible':deadline>=finish,'longest_chain':chain,'tasks':rows,'exit_code':int(deadline<finish)}

if __name__ == '__main__':
    raise SystemExit(main())
