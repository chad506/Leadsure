# -*- coding: utf-8 -*-
"""Leaderboard RV refresh, Sep 15 2026 01:10Z walk.
Re-marks every leaderboard candidate to the fresh CLOB mid, drops resolved markets,
re-ranks the top 50 and rewrites the tbody. Fairs are the tabs' own as-baked values."""
import re, json
from collections import Counter
REPO='/home/claude/Leadsure'
p=REPO+'/polymarket/index.html'; h=open(p).read()
js=open(REPO+'/polymarket/polymarket.js').read()
TOK=dict(re.findall(r"'([a-zA-Z0-9\-]+)':\s*'(\d{20,})'",js))
# ---- fresh books, keyed by token ----
LAB={l.split('|')[0]:l.strip().split('|')[1] for l in open('/tmp/lb/tokens.txt') if '|' in l}   # label -> token
BK={}
for line in open('/tmp/lb/books_sep15.csv'):
    f=line.strip().split(',')
    if len(f)<11: continue
    lab=f[0]; tok=LAB[lab]
    nb,na=f[2].split('/'); ub,ua=f[3].split('/'); p5b,p5a=f[4].split('/')
    bid=float(f[5]) if f[5] else 0.0; ask=float(f[7]) if f[7] else 100.0
    empty=(int(nb)==0 and int(na)==0)
    BK[tok]=dict(nb=int(nb),na=int(na),ub=float(ub),ua=float(ua),p5b=float(p5b),p5a=float(p5a),bid=bid,ask=ask,mid=(bid+ask)/2,empty=empty,
                 bidsz=float(f[6]) if f[6] else 0.0, asksz=float(f[8]) if f[8] else 0.0)
WALK='Sep 15 01:10Z'
RESOLVED_TOK=set(t for t,b in BK.items() if b['empty'])   # gamma: all closed=true, resolved YES (oman930 has no gamma market — no book either)
def cells(tr): return re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
def txt(c): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',c)).strip()
def num(s):
    try: return float(re.sub(r'[^\d.\-]','',txt(s)))
    except: return None
TABCLS={'IRAN':'pm-watch','TREASURIES':'pm-fair','ANALYSIS':'pm-rich','BITCOIN':'pm-cheap','OIL':'pm-fair'}
LIQCLS={'DEEP':'pm-cheap','OK':'pm-fair','THIN':'pm-watch','NO MARKET':'pm-rich','—':'pm-fair','WIDE':'pm-rich','TAIL':'pm-rich','PROPAGATED':'pm-rich'}
def vcls(v):
    v=v.upper()
    if any(x in v for x in ('TOP BET','CHEAP','SCENARIO BUY','PAYS','TRIGGER')): return 'pm-cheap'
    if any(x in v for x in ('TRAP','RICH','JUNK')): return 'pm-rich'
    if any(x in v for x in ('THIN','AMBIG','HIGH VAR','SLOW')): return 'pm-watch'
    return 'pm-fair'
def relift(pu,pc,mid):
    # the Oil / Treasuries tabs' odds-space update: odds_cond = odds_mid × [pc/(1-pc)] / [pu/(1-pu)], re-applied to tonight's mid
    pu_=min(max(pu,0.05),99.95)/100; pc_=min(max(pc,0.05),99.95)/100; m_=min(max(mid,0.05),99.95)/100
    LR=(pc_/(1-pc_))/(pu_/(1-pu_)); oc=(m_/(1-m_))*LR; return 100*oc/(1+oc)
def fmid(m): return f'{m:.2f}%' if m<1 else f'{m:.1f}%'
def row(tab,name,url,side,mid,fairtxt,rv,basis,liq,verdict):
    link=f'<a href="{url}" target="_blank" rel="noopener">{name}<span class="pm-ext">↗</span></a>' if url else name
    sb='<span class="dir-badge dir-long">YES</span>' if side=='YES' else '<span class="dir-badge dir-short">NO</span>'
    bcls='pm-fair' if basis=='MODEL' else 'pm-watch'
    rvc=' pm-pos' if rv>=1.15 else ''
    return f'<td><span class="pm-badge {TABCLS[tab]}">{tab}</span></td><td class="pm-co pm-mkt trs-mkt">{link}</td><td>{sb}</td><td class="col-num">{fmid(mid)}</td><td class="col-num">{fairtxt}</td><td class="col-num{rvc}">{rv:.2f}×</td><td><span class="pm-badge {bcls}">{basis}</span></td><td><span class="pm-badge {LIQCLS.get(liq,"pm-fair")}">{liq}</span></td><td><span class="pm-badge {vcls(verdict)}">{verdict}</span></td></tr>'
cands=[]; log=[]; dropped=[]; remarked=0
# ---- 1. the four Every-Market tables (Analysis / Treasuries MODEL / Bitcoin / Iran) ----
C=json.load(open('/tmp/lb/cands.json'))
ANAME={'dec-NVDA':'NVIDIA largest company · Dec 31','dec-AAPL':'Apple largest company · Dec 31','dec-GOOGL':'Alphabet largest company · Dec 31','dec-MSFT':'Microsoft largest company · Dec 31','dec-AMZN':'Amazon largest company · Dec 31','sep-sep3NVDA':'NVIDIA 3rd place · Sep 30'}
for r in C:
    tok=r.get('tok'); key=r['key']
    if r.get('resolved') or key in ('wti-100','wti-90'):   # WTI HIGH $100 / $90 in September resolved YES (Sep 10 / earlier)
        dropped.append((r['tab'],r['name'],'resolved YES')); continue
    if not tok or tok not in BK: log.append(('NOBOOK',r['tab'],key)); continue
    b=BK[tok]
    if b['empty']: dropped.append((r['tab'],r['name'],'resolved / no book')); continue
    fair=r['fair']
    if fair is None or fair<=0: continue
    mid=b['mid']; px=mid if r['side']=='YES' else 100-mid
    if px<=0: continue
    rv=fair/px
    name=ANAME.get(key,r['name']); url=r['url']
    if r['tab']=='IRAN': fairtxt=f'{fair:.0f}¢'+(' (NO)' if r['side']=='NO' else '')
    elif r['tab']=='ANALYSIS': fairtxt=f'{fair:.2f}%'
    else: fairtxt=f'{fair:.1f}%'
    liq=r['mkt']; verdict=r['verdict']
    if r['tab']=='IRAN' and liq not in LIQCLS: liq='—'
    cands.append((rv,1,row(r['tab'],name,url,r['side'],mid,fairtxt,rv,r['basis'],liq,verdict),r['tab'],r['basis'],name,mid,fair,r['side'],key,r['mid'],fair))
    remarked+=1
# ---- 2. Oil tab conditional book (IF BRENT 130) ----
TJ=json.load(open('/tmp/oil/table_oil.json')); T=TJ['rows']; PT=TJ['p_touch']*100
lbo=0
for r in T:
    if r['method']=='NONE' or r.get('tok') is None or r['tok'] not in BK: continue
    b=BK[r['tok']]
    if b['empty']: dropped.append(('OIL',r['label'],'resolved / no book')); continue
    if r['cap'] is None or r['cap']<100 or r['liq'] in ('WIDE','TAIL','PROPAGATED'): continue
    if b['ask']-b['bid']>15: continue   # WIDE on tonight's book
    pu_,pc_=r['p_unc'],r['p_cond']
    if pu_ is None or pc_ is None: continue
    slift=(pc_/pu_) if r['side']=='YES' else ((100-pc_)/(100-pu_))
    if slift<1.1: continue
    mid=b['mid']; smid=mid if r['side']=='YES' else 100-mid
    if smid<=0: continue
    if r['method'] in ('LIFT','INPUT'):
        cy=relift(pu_,pc_,mid); fair=cy if r['side']=='YES' else 100-cy
        slift=(cy/mid) if r['side']=='YES' else ((100-cy)/(100-mid))
        if slift<1.1: continue
    else: fair=r['fair']
    rvm=fair/smid
    if rvm<1.15: continue
    lab=r['label']+(' · no add above 25¢' if r['key']=='w120' else '')
    cands.append((rvm,2,row('OIL',lab,r['url'],r['side'],mid,f'{fair:.1f}%',rvm,'IF BRENT 130',r['liq'],f'SCENARIO BUY · {r["method"]}'),'OIL','IF BRENT 130',lab,mid,fair,r['side'],r['key'],r['mid'],r['fair'])); lbo+=1
# ---- 3. Treasuries conditional book (IF 10Y 5.00) ----
t5=re.search(r'<tbody id="trs5-table-body">(.*?)</tbody>',h,re.S).group(1)
lbt=0
for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',t5,re.S):
    c=cells(tr)
    if len(c)<15: continue
    key=re.search(r'data-odds="(trs-[^"]+)"',tr);
    if not key: continue
    key=key.group(1); tok=TOK.get(key)
    if not tok or tok not in BK: log.append(('NOBOOK','TRS5',key)); continue
    b=BK[tok]
    name=txt(c[1]).split('↗')[0].strip(); url=re.search(r'href="([^"]+)"',c[1]); url=url.group(1) if url else ''
    method=txt(c[2]); side=txt(c[8]); fair=num(c[9]); cap=num(c[12]); liq=txt(c[13]); verdict=txt(c[14]); pu_=num(c[5]); pc_=num(c[6])
    if b['empty']: dropped.append(('TREASURIES',name,'resolved / no book')); continue
    if method=='NONE' or fair is None or cap is None or cap<20 or liq in ('WIDE','TAIL','PROPAGATED') or pu_ is None or pc_ is None: continue
    if b['ask']-b['bid']>15: continue
    slift=(pc_/pu_) if side=='YES' and pu_>0 else (((100-pc_)/(100-pu_)) if side=='NO' and pu_<100 else 0)
    if slift<1.1: continue
    mid=b['mid']; smid=mid if side=='YES' else 100-mid
    if smid<=0: continue
    fair0=fair
    if method in ('LIFT','INPUT'):
        cy=relift(pu_,pc_,mid); fair=cy if side=='YES' else 100-cy
        slift=(cy/mid) if side=='YES' else ((100-cy)/(100-mid))
        if slift<1.1: continue
    rvm=fair/smid
    if rvm<1.15: continue
    cands.append((rvm,3,row('TREASURIES',name,url,side,mid,f'{fair:.1f}%',rvm,'IF 10Y 5.00',liq,f'SCENARIO BUY · {method}'),'TREASURIES','IF 10Y 5.00',name,mid,fair,side,key,num(c[4]) if False else None,fair0)); lbt+=1
# ---- rank ----
cands.sort(key=lambda x:(-x[0],x[1]))
top=cands[:50]
outl=[f'              <tr data-lb-row="{i}"><td class="col-num"><strong>#{i}</strong></td>{c[2]}' for i,c in enumerate(top,1)]
lb_full=re.search(r'(<tbody id="lb-table-body">)(.*?)(</tbody>)', h, re.S)
old=re.findall(r'<tr data-lb-row="\d+">.*?</tr>', lb_full.group(2), re.S)
h=h[:lb_full.start(2)]+'\n'+'\n'.join(outl)+'\n            '+h[lb_full.end(2):]
open(p,'w').write(h)
cnt=Counter(c[3] for c in top); basis=Counter(c[4] for c in top)
n_univ=sum(len(re.findall(r'<tr', m)) for tb,m in re.findall(r'<tbody id="([a-z0-9-]+-table-body)">(.*?)</tbody>', h, re.S) if tb!='lb-table-body')
model=[c for c in cands if c[4]=='MODEL']; model.sort(key=lambda x:-x[0])
print('cands',len(cands),'oil',lbo,'trs5',lbt,'four-table rows re-marked',remarked,'dropped',len(dropped),'univ',n_univ)
print('cut',round(top[-1][0],2),dict(cnt),dict(basis))
for i,c in enumerate(top,1): print(i,round(c[0],2),c[3],c[4],c[5][:60],c[7],'mid',round(c[6],2),'fair',c[7] if False else c[7],'old mid',c[10])
print('best MODEL:',[(round(c[0],2),c[5],round(c[6],2),c[7]) for c in model[:6]])
print('dropped:',dropped); print('log:',log)
json.dump({'cut':top[-1][0],'cnt':dict(cnt),'basis':dict(basis),'ncands':len(cands),'oil':lbo,'trs5':lbt,'remarked':remarked,'dropped':dropped,'univ':n_univ,
           'top':[(round(c[0],2),c[3],c[4],c[5],round(c[6],2),c[7],c[8],c[9]) for c in top],'model':[(round(c[0],2),c[5],round(c[6],2),c[7],c[9]) for c in model[:8]],'all':[(round(c[0],2),c[3],c[4],c[5],round(c[6],2),round(c[7],2),c[9]) for c in cands]},
          open('/tmp/lb/lb_sep15.json','w'),indent=0)
