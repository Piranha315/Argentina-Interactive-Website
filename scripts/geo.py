"""Project and simplify Natural Earth outlines into SVG paths for the map (writes data/geo.json).
Run scripts/fetch_naturalearth.sh first."""
import json,math,sys
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NE=os.path.join(ROOT,'data','raw','naturalearth')
# projection: equirectangular around lat -38
LON0,LON1,LAT0,LAT1=-76.5,-49.0,-20.0,-56.2
K=math.cos(math.radians(38))
W=1000
sx=W/((LON1-LON0)*K)
H=round((LAT0-LAT1)*sx)
def P(lon,lat): return ((lon-LON0)*K*sx,(LAT0-lat)*sx)
def dp(pts,eps):
    if len(pts)<3: return pts
    a,b=pts[0],pts[-1]; dmax=0; idx=0
    ax,ay=a; bx,by=b; L=math.hypot(bx-ax,by-ay) or 1e-9
    for i in range(1,len(pts)-1):
        px,py=pts[i]; d=abs((bx-ax)*(ay-py)-(ax-px)*(by-ay))/L
        if d>dmax: dmax=d; idx=i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [a,b]
def ring(r,eps,minA=0):
    pts=[P(x,y) for x,y in r]
    m=len(pts)//2
    s=dp(pts[:m+1],eps)[:-1]+dp(pts[m:],eps)
    if len(s)<4: return None
    A=0.5*abs(sum(s[i][0]*s[i+1][1]-s[i+1][0]*s[i][1] for i in range(len(s)-1)))
    if A<minA: return None
    return s
def polys(g):
    return g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
def path(rings):
    return ''.join('M'+' '.join(f'{x:.1f},{y:.1f}' for x,y in r[:-1])+'Z' for r in rings)
out={'W':W,'H':H,'lon0':LON0,'lat0':LAT0,'K':K,'sx':sx}
a0=json.load(open(f'{NE}/ne_50m_admin_0_countries.geojson'))
cs={}
for f in a0['features']:
    iso=f['properties']['ADM0_A3']
    if iso in('ARG','CHL','BOL','PRY','BRA','URY','FLK','PER'):
        rs=[]
        for poly in polys(f['geometry']):
            r=ring(poly[0],0.9 if iso=='ARG' else 1.4, 4)
            if r: rs.append(r)
        cs[iso]=path(rs)
        if iso=='ARG': out['argRings']=[[ [round(x,1),round(y,1)] for x,y in r] for r in rs]
out['countries']=cs
a1=json.load(open(f'{NE}/ne_10m_admin_1_states_provinces.geojson'))
prov={}
for f in a1['features']:
    p=f['properties']
    if p.get('adm0_a3')=='ARG':
        rs=[]
        for poly in polys(f['geometry']):
            r=ring(poly[0],1.0,6)
            if r: rs.append(r)
        prov[p['name']]=path(rs)
out['prov']=prov
rv=json.load(open(f'{NE}/ne_50m_rivers_lake_centerlines.geojson'))
rivers={}
for f in rv['features']:
    n=f['properties'].get('name') or ''
    g=f['geometry']; lines=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
    for l in lines:
        if not any(LON0<x<LON1 and LAT1<y<LAT0 for x,y in l): continue
        pts=dp([P(x,y) for x,y in l],0.8)
        rivers.setdefault(n,[]).append('M'+' '.join(f'{x:.1f},{y:.1f}' for x,y in pts))
out['rivers']={k:''.join(v) for k,v in rivers.items()}
lk=json.load(open(f'{NE}/ne_50m_lakes.geojson'))
lakes=[]
for f in lk['features']:
    for poly in polys(f['geometry']):
        if all(LON0<x<LON1 and LAT1<y<LAT0 for x,y in poly[0]):
            r=ring(poly[0],0.6,3)
            if r: lakes.append(r)
out['lakes']=path(lakes)
json.dump(out,open(os.path.join(ROOT,'data','geo.json'),'w'))
print(W,H,len(prov),list(rivers.keys()),len(lakes),{k:len(v) for k,v in cs.items()})
