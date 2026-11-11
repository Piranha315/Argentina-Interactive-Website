"""Chart series, WGI scores and the gravity regression from raw World Bank and UN Comtrade files (writes data/data.json)."""
import json,math,sys
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'data','raw')
def wb(ind):
    d=json.load(open(f'{RAW}/wb/{ind}.json')); rows=d[1] if isinstance(d,list) else d
    o={}
    for r in rows:
        if r['value'] is not None: o.setdefault(r['countryiso3code'],{})[int(r['date'])]=r['value']
    return o
Y=list(range(2005,2026))
out={}
g=wb('NY.GDP.MKTP.CD')['ARG']; gr=wb('NY.GDP.MKTP.KD.ZG')['ARG']
out['gdp']=[[y,round(g[y]/1e9,1),round(gr[y],1)] for y in Y]
op=wb('NE.TRD.GNFS.ZS')
out['open']={c:[[y,round(op[c][y],1)] for y in Y if y in op[c]] for c in op}
gx,gm,sx_,sm=[wb(i)['ARG'] for i in ('BX.GSR.MRCH.CD','BM.GSR.MRCH.CD','BX.GSR.NFSV.CD','BM.GSR.NFSV.CD')]
out['bal']=[[y,round((gx[y]-gm[y])/1e9,1),round((sx_[y]-sm[y])/1e9,1)] for y in Y]
fi,fo=wb('BX.KLT.DINV.WD.GD.ZS')['ARG'],wb('BM.KLT.DINV.WD.GD.ZS')['ARG']
out['fdi']=[[y,round(fi[y],2),round(fo[y],2)] for y in Y]
cpi=wb('FP.CPI.TOTL.ZG')['ARG']; out['cpi']=[[y,round(cpi[y],1)] for y in Y if y in cpi]
# WGI
wg={}
for ind in ['VA','PV','GE','RQ','RL','CC']:
    d=json.load(open(f'{RAW}/wgi/wgi_{ind}.json'))[1]
    for r in d:
        if r['value'] is not None: wg.setdefault(r['countryiso3code'],{})[ind]=round(r['value'],1)
out['wgi']=wg
# gravity
c=json.load(open(f'{RAW}/wb/countries.json')); C=c[1] if isinstance(c,list) else c
coord={r['id']:(float(r['latitude']),float(r['longitude'])) for r in C if r['latitude']}
names={r['id']:r['name'] for r in C}
gd=json.load(open(f'{RAW}/wb/gdp_all.json')); G=gd[1] if isinstance(gd,list) else gd
gdp={r['countryiso3code']:r['value'] for r in G if r['value']}
x=json.load(open(f'{RAW}/comtrade/xpart_2024.json'))['data']
la,lo=coord['ARG']
def dist(a,b):
    p1,l1,p2,l2=map(math.radians,(la,lo,a,b))
    return 6371*2*math.asin(math.sqrt(math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin((l2-l1)/2)**2))
pts=[]
for r in x:
    i=r['partnerISO']
    if i in coord and i in gdp and r['primaryValue']>0 and i!='ARG':
        pts.append((i,math.log(r['primaryValue']),math.log(gdp[i]),math.log(dist(*coord[i])),r['primaryValue']))
n=len(pts)
# OLS y on [1,lg,ld]
import itertools
X=[[1,p[2],p[3]] for p in pts]; yv=[p[1] for p in pts]
XtX=[[sum(a[i]*a[j] for a in X) for j in range(3)] for i in range(3)]
Xty=[sum(a[i]*b for a,b in zip(X,yv)) for i in range(3)]
def solve(A,b):
    A=[row[:]+[bb] for row,bb in zip(A,b)]
    for i in range(3):
        p=max(range(i,3),key=lambda r:abs(A[r][i])); A[i],A[p]=A[p],A[i]
        for r in range(3):
            if r!=i:
                f=A[r][i]/A[i][i]; A[r]=[x-f*y for x,y in zip(A[r],A[i])]
    return [A[i][3]/A[i][i] for i in range(3)]
beta=solve(XtX,Xty)
res=[yy-sum(b*a for b,a in zip(beta,xx)) for xx,yy in zip(X,yv)]
ssr=sum(e*e for e in res); m=sum(yv)/n; sst=sum((v-m)**2 for v in yv)
s2=ssr/(n-3)
# inverse for se
def inv(A):
    M=[row[:]+[1 if i==j else 0 for j in range(3)] for i,row in enumerate(A)]
    for i in range(3):
        p=max(range(i,3),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]
        piv=M[i][i]; M[i]=[v/piv for v in M[i]]
        for r in range(3):
            if r!=i:
                f=M[r][i]; M[r]=[a-f*b for a,b in zip(M[r],M[i])]
    return [row[3:] for row in M]
Iv=inv(XtX); se=[math.sqrt(s2*Iv[i][i]) for i in range(3)]
out['grav']={'b':[round(v,3) for v in beta],'se':[round(v,3) for v in se],'r2':round(1-ssr/sst,2),'n':n,
  'pts':[[i,names.get(i,i),round(ly-beta[1]*lg,2),round(math.exp(ld)),round(v/1e6)] for (i,ly,lg,ld,v) in pts]}
json.dump(out,open(os.path.join(ROOT,'data','data.json'),'w'),separators=(',',':'))
print(out['grav']['b'],out['grav']['se'],out['grav']['r2'],n); print(out['wgi']); print(out['gdp'][-3:],out['bal'][-3:],out['fdi'][-3:])
