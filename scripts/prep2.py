"""Export mix by product group, main partners and import chapters from UN Comtrade (writes data/data2.json)."""
import json,sys
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'data','raw')
def load(f): return json.load(open(f'{RAW}/comtrade/{f}'))['data']
out={}
grp=[('Food & farm',1,24),('Fuels & minerals',25,27),('Chemicals & plastics',28,40),('Metals & gold',71,83),('Machinery & vehicles',84,89)]
comp={}
for y in (2004,2014,2024):
    d=[r for r in load(f'x2_{y}.json') if r['cmdCode']!='TOTAL' and r['partnerCode']==0]
    tot=sum(r['primaryValue'] for r in d)
    sh=[]
    for n,a,b in grp:
        sh.append(round(100*sum(r['primaryValue'] for r in d if a<=int(r['cmdCode'])<=b)/tot,1))
    sh.append(round(100-sum(sh),1))
    comp[y]={'tot':round(tot/1e9,1),'sh':sh}
out['comp']=comp
def part(f):
    d=load(f); tot=[r for r in d if r['partnerCode']==0][0]['primaryValue']
    rows=[(r['partnerDesc'],r['primaryValue']) for r in d if r['partnerCode']!=0]
    rows.sort(key=lambda x:-x[1])
    hhi=sum((v/tot)**2 for _,v in rows)
    return {'tot':round(tot/1e9,1),'hhi':round(hhi,3),'top':[[n,round(100*v/tot,1),round(v/1e9,2)] for n,v in rows[:8]]}
out['xp']=part('xpart_2024.json'); out['mp']=part('mpart_2024.json')
m=[r for r in load('m2_2024.json') if r['cmdCode']!='TOTAL' and r['partnerCode']==0]
mt=sum(r['primaryValue'] for r in m); m.sort(key=lambda r:-r['primaryValue'])
out['mchap']={'tot':round(mt/1e9,1),'top':[[r['cmdCode'],round(100*r['primaryValue']/mt,1)] for r in m[:9]]}
json.dump(out,open(os.path.join(ROOT,'data','data2.json'),'w'),separators=(',',':'))
print(json.dumps(out,indent=0)[:3000])
