# -*- coding: utf-8 -*-
"""Conditional table for 'If Brent prints $130 by Oct 1' — Sep 10 2026 close basis, books walked Sep 10 22:17Z and 22:53Z."""
import json, re
MB=json.load(open('/tmp/oil/model_oil_base.json')); ML=json.load(open('/tmp/oil/model_oil_vol07.json'))
# two-regime mixture: 50/50 prior on the full-sample (68% ann) and 0.7x (48%) bootstrap regimes; conditional weights ∝ P(touch|regime)
wb=MB['p_touch']/(MB['p_touch']+ML['p_touch']); wl=1-wb
def PC(k): return 100*(wb*MB['cond'][k]+wl*ML['cond'][k])
def PU(k): return 100*0.5*(MB['uncond'][k]+ML['uncond'][k])
P_TOUCH=0.5*(MB['p_touch']+ML['p_touch']); P_CLOSE=0.5*(MB['p_close130']+ML['p_close130'])
def parse_books(path):
    B={}
    for line in open(path):
        line=line.strip()
        if not line or line.startswith('#'): continue
        f=line.split('|')
        if len(f)<7: continue
        def lv(s):
            s=s.strip()
            if ' ' not in s: return []
            s=s.split(' ',1)[1]
            return [(float(a),float(b)) for a,b in (p.split(':') for p in s.split(',') if p)]
        bids=lv(f[5]); asks=lv(f[6])
        nb,na=f[2].split('/'); sb,sa=f[3][1:].split('/'); pb,pa=f[3+1][4:].split('/')
        B[f[0]]=dict(ts=int(f[1]),nb=int(nb),na=int(na),usd_b=float(sb),usd_a=float(sa),p5b=float(pb),p5a=float(pa),bids=bids,asks=asks,
                     bid=bids[-1][0] if bids else 0.0, ask=asks[-1][0] if asks else 100.0)
    return B
B=parse_books('/tmp/oil/books2.txt')
S={l.split('|')[0]:l.strip().split('|') for l in open('/tmp/oil/shortlist.txt') if '|' in l}
def url(k): return 'https://polymarket.com/event/'+S[k][3]
# key, book, label, group, method, model key or (unc,cond), note
ROWS=[
 ('w105','k144','WTI touches $105 in September','WTI Sep ladder','MODEL','wti_hi_105','Pyth 1-min high of the CME active month ≥ 105 (Oct CL high 104.44 Sep 10)'),
 ('w110','k155','WTI touches $110 in September','WTI Sep ladder','MODEL','wti_hi_110','active-month high ≥ 110'),
 ('w115','k173','WTI touches $115 in September (held 428.28 sh)','WTI Sep ladder','MODEL','wti_hi_115','active-month high ≥ 115 · HELD — the one rung with an unconditional edge; no add above 34'),
 ('w120','k169','WTI touches $120 in September (held 4,473.62 sh)','WTI Sep ladder','MODEL','wti_hi_120','active-month high ≥ 120 · Nov CL is the active month from the Sep 18 session · HELD — no add above 25¢ (card #1): $58 rests at or under 25'),
 ('w125','k385','WTI touches $125 in September (held 788.25 sh)','WTI Sep ladder','MODEL','wti_hi_125','active-month high ≥ 125'),
 ('w130','k210','WTI touches $130 in September','WTI Sep ladder','MODEL','wti_hi_130','active-month high ≥ 130'),
 ('w140','k196','WTI touches $140 in September','WTI Sep ladder','MODEL','wti_hi_140','active-month high ≥ 140'),
 ('w150','k214','WTI touches $150 in September','WTI Sep ladder','MODEL','wti_hi_150','active-month high ≥ 150'),
 ('wl100','k433','WTI touches $100 (LOW) in September','WTI Sep ladder','MODEL','wti_lo_100','active-month low ≤ 100 · Nov CL settled 99.51 on Sep 10 — the roll itself can print it'),
 ('wl95','k302','WTI touches $95 (LOW) in September','WTI Sep ladder','MODEL','wti_lo_95','active-month low ≤ 95'),
 ('wl90','k262','WTI touches $90 (LOW) in September','WTI Sep ladder','MODEL','wti_lo_90','active-month low ≤ 90'),
 ('wl85','k256','WTI touches $85 (LOW) in September','WTI Sep ladder','MODEL','wti_lo_85','active-month low ≤ 85'),
 ('athsep','k52','Crude oil new all-time high by Sep 30 (held 34.93 sh)','Crude ATH','MODEL','ath_sep','CME CL active-month daily high > 147.27'),
 ('athdec','k71','Crude oil new all-time high by Dec 31 (held 1,687.18 sh)','Crude ATH','LIFT','ath_dec','CL daily high > 147.27 by Dec 31'),
 ('s497','k587','10Y hits 4.97% in September','10Y Sep ladder','MODEL','y10_sep_4.97','Treasury.gov par print ≥ 4.97 (4.95 on Sep 10)'),
 ('s500','k609','10Y hits 5.00% in September (held 260 sh)','10Y Sep ladder','MODEL','y10_sep_5.00','print ≥ 5.00 by Sep 30'),
 ('s505','k593','10Y hits 5.05% in September (held 215.44 sh)','10Y Sep ladder','MODEL','y10_sep_5.05','print ≥ 5.05'),
 ('s510','k456','10Y hits 5.10% in September','10Y Sep ladder','MODEL','y10_sep_5.10','print ≥ 5.10'),
 ('d476','k424','10Y dips below 4.76% in September','10Y Sep dips','MODEL','y10_sep_lo_4.76','Sep print < 4.76'),
 ('d473','k623','10Y dips below 4.73% in September','10Y Sep dips','MODEL','y10_sep_lo_4.73','Sep print < 4.73'),
 ('d470','k493','10Y dips below 4.70% in September','10Y Sep dips','MODEL','y10_sep_lo_4.70','Sep print < 4.70'),
 ('10y50','k231','10Y hits 5.0% before 2027 (held 10,544.07 sh)','10Y ladder','LIFT','y10_2026_5.00','print ≥ 5.00 by Dec 31'),
 ('10y52','k293','10Y hits 5.2% before 2027 (held 3,168.23 sh)','10Y ladder','LIFT','y10_2026_5.20','print ≥ 5.20'),
 ('10y55','k402','10Y hits 5.5% before 2027 (held 1,867.22 sh)','10Y ladder','LIFT','y10_2026_5.50','print ≥ 5.50'),
 ('10y57','k476','10Y hits 5.7% before 2027','10Y ladder','LIFT','y10_2026_5.70','print ≥ 5.70'),
 ('t540s','k588','30Y hits 5.40% in September','30Y / 5Y','MODEL','y30_sep_5.40','30Y print ≥ 5.40 (5.37 on Sep 10)'),
 ('t540','k599','30Y hits 5.40% before 2027','30Y / 5Y','LIFT','y30_2026_5.40','30Y print ≥ 5.40 by Dec 31'),
 ('b515','k618','30Y dips below 5.15% in September','30Y / 5Y','MODEL','y30_sep_lo_5.15','Sep 30Y print < 5.15'),
 ('f478','k545','5Y hits 4.78% in September','30Y / 5Y','MODEL','y5_sep_4.78','Sep 5Y print ≥ 4.78 (4.75 on Sep 10)'),
 ('f483','k536','5Y hits 4.83% in September','30Y / 5Y','MODEL','y5_sep_4.83','Sep 5Y print ≥ 4.83'),
 ('sephike','k6','Fed hikes 25 bp at the Sep 15–16 FOMC','Fed','INPUT',(64.5,68),'FOMC statement'),
 ('sepnc','k3','Fed no change at the Sep FOMC','Fed','INPUT',(35.5,32),'FOMC statement'),
 ('hikeoct','k89','Fed rate hike by the Oct meeting','Fed','INPUT',(72,82),'any hike at Sep or Oct'),
 ('octhike','k142','Fed hikes 25 bp at the Oct FOMC','Fed','INPUT',(33.5,38),'FOMC statement'),
 ('dechike','k192','Fed hikes 25 bp at the Dec FOMC','Fed','INPUT',(59,60),'FOMC statement'),
 ('hike26','k12','Any Fed hike in 2026','Fed','INPUT',(77.5,89),'federalreserve.gov'),
 ('nohike','k225','No Fed hikes in 2026','Fed','INPUT',(22.5,11),'exactly 0 hikes'),
 ('hike1','k278','Exactly 1 Fed hike in 2026','Fed','INPUT',(43.5,29),'exactly 1 × 25 bp'),
 ('hike2','k257','Exactly 2 Fed hikes in 2026','Fed','INPUT',(27,43),'exactly 2 × 25 bp'),
 ('hike3','k298','Exactly 3 Fed hikes in 2026','Fed','INPUT',(4.7,17),'exactly 3 × 25 bp · propagated from the meeting marginals, not a view — NO TICKET'),
 ('up425','k217','Fed upper bound reaches 4.25%+ before 2027','Fed','INPUT',(42,60),'two hikes from 3.75 — must not exceed P(≥2 hikes) = 43 by more than timing'),
 ('up450','k304','Fed upper bound reaches 4.50%+ before 2027','Fed','INPUT',(12.4,17),'three hikes · propagated — NO TICKET'),
 ('end425','k117','Fed upper bound 4.25% at end-2026','Fed','INPUT',(23,43),'two net hikes'),
 ('end400','k61','Fed upper bound 4.00% at end-2026','Fed','INPUT',(44.4,29),'one net hike'),
 ('end375','k101','Fed upper bound 3.75% at end-2026','Fed','INPUT',(21,11),'no net change'),
 ('nocuts','k14','No Fed cuts in 2026 (held 68.78 sh)','Fed','INPUT',(92.65,94),'zero cuts'),
 ('emerg','k171','Fed emergency cut before 2027 (held 250 sh)','Fed','INPUT',(6.8,5),'unscheduled cut — the crash-risk leg of an oil shock'),
 ('ppp','k394','Fed Pause–Pause–Pause (Sep–Oct–Dec)','Fed','INPUT',(20.5,9),'no change at all three'),
 ('hhp','k620','Fed Hike–Hike–Pause (Sep–Oct–Dec)','Fed','INPUT',(21.5,10),'hike, hike, pause'),
 ('y750','k370','SPY touches $750 in September','S&P 500','MODEL','spy_lo_750','Sep RTH 1-min low ≤ 750 (SPY ≈ 759)'),
 ('y740','k332','SPY touches $740 in September','S&P 500','MODEL','spy_lo_740','Sep low ≤ 740'),
 ('y730','k430','SPY touches $730 in September','S&P 500','MODEL','spy_lo_730','Sep low ≤ 730'),
 ('y720','k469','SPY touches $720 in September','S&P 500','MODEL','spy_lo_720','Sep low ≤ 720'),
 ('y710','k505','SPY touches $710 in September','S&P 500','MODEL','spy_lo_710','Sep low ≤ 710'),
 ('y700','k455','SPY touches $700 in September','S&P 500','MODEL','spy_lo_700','Sep low ≤ 700'),
 ('x7000','x7000','SPX touches 7,000 in December (held 200.18 sh)','S&P 500','NONE',None,'touch 30 / 36 at 23:1xZ (levels not walked) — bought Sep 10 at 33–36.6¢; the SPY September lows are the tab’s expression of the same view'),
 ('spx6200','k281','SPX touches 6,200 in December (held 65.56 sh)','S&P 500','INPUT',(20.95,27),'Dec-only low ≤ 6,200 (−18%) · input: a $130 oil shock roughly doubles the model’s unconditional 9 → 18; the market’s 21 is lifted 1.3'),
 ('x5800','k296','SPX touches 5,800 in December','S&P 500','INPUT',(9.5,12),'Dec low ≤ 5,800 · lifted 1.25'),
 ('x8200','k333','SPX touches 8,200 in December','S&P 500','INPUT',(26.5,20),'Dec high ≥ 8,200 (+8%) · scenario loser, lifted 0.75'),
 ('a4300','k483','Gold (XAU) touches $4,300 in September','Gold / silver','MODEL','xau_lo_4300','1-min low ≤ 4,300 (spot ≈ 4,320)'),
 ('a4200','k434','Gold (XAU) touches $4,200 in September','Gold / silver','MODEL','xau_lo_4200','1-min low ≤ 4,200'),
 ('a4100','k421','Gold (XAU) touches $4,100 in September','Gold / silver','MODEL','xau_lo_4100','1-min low ≤ 4,100'),
 ('a4000','k375','Gold (XAU) touches $4,000 in September','Gold / silver','MODEL','xau_lo_4000','1-min low ≤ 4,000'),
 ('a4500','k530','Gold (XAU) touches $4,500 in September','Gold / silver','MODEL','xau_hi_4500','1-min high ≥ 4,500'),
 ('a4600','k507','Gold (XAU) touches $4,600 in September','Gold / silver','MODEL','xau_hi_4600','1-min high ≥ 4,600'),
 ('gold6k','k72','Gold (GC) hits $6,000 by Dec (held 153.85 sh)','Gold / silver','INPUT',(9.5,7),'GC settle ≥ 6,000 · scenario loser, lifted 0.75'),
 ('g62','k523','Silver (XAG) touches $62 in September','Gold / silver','MODEL','xag_lo_62','1-min low ≤ 62 (spot ≈ 63.5)'),
 ('g60','k484','Silver (XAG) touches $60 in September','Gold / silver','MODEL','xag_lo_60','1-min low ≤ 60'),
 ('g58','k561','Silver (XAG) touches $58 in September','Gold / silver','MODEL','xag_lo_58','1-min low ≤ 58'),
 ('g56','k438','Silver (XAG) touches $56 in September','Gold / silver','MODEL','xag_lo_56','1-min low ≤ 56'),
 ('g70','k529','Silver (XAG) touches $70 in September','Gold / silver','MODEL','xag_hi_70','1-min high ≥ 70'),
 ('k995','k589','DXY touches 99.50 in September','Dollar','MODEL','dxy_hi_99.5','1-min high ≥ 99.50 (99.09)'),
 ('k100','k581','DXY touches 100.00 in September','Dollar','MODEL','dxy_hi_100.0','1-min high ≥ 100'),
 ('k1005','k602','DXY touches 100.50 in September','Dollar','MODEL','dxy_hi_100.5','1-min high ≥ 100.5'),
 ('k985','k491','DXY touches 98.50 in September','Dollar','MODEL','dxy_lo_98.5','1-min low ≤ 98.50'),
 ('k98','k533','DXY touches 98.00 in September','Dollar','MODEL','dxy_lo_98.0','1-min low ≤ 98'),
 ('cease930','k49','Israel × Iran ceasefire holds through Sep 30','Iran — ceasefire','INPUT',(84,62),'no qualifying strike on either’s territory · scenario weights 40/30/15/15 (Gulf-infrastructure war / US–Iran escalation / Israel–Iran collapse / non-Iran)'),
 ('cease1031','k103','Israel × Iran ceasefire holds through Oct 31','Iran — ceasefire','INPUT',(73,50),'through Oct 31'),
 ('cease1130','k189','Israel × Iran ceasefire holds through Nov 30','Iran — ceasefire','INPUT',(63,42),'through Nov 30'),
 ('cease1231','k105','Israel × Iran ceasefire holds through Dec 31','Iran — ceasefire','INPUT',(58.5,38),'through Dec 31'),
 ('uscease930','k186','US × Iran effective ceasefire by Sep 30','Iran — ceasefire','INPUT',(75,65),'a 14-day stretch with no US strike on Iranian territory, starting by Sep 30 — tanker/ship strikes do not count'),
 ('uscease918','k280','US × Iran effective ceasefire by Sep 18','Iran — ceasefire','INPUT',(70.5,62),'the 14-day stretch must start by Sep 18'),
 ('airsp930','k85','Iran full airspace closure by Sep 30','Iran — escalation','INPUT',(9.5,35),'general closure of the Tehran FIR (Feb 28 and Jan 2026 precedents) — likely, not certain, under strikes on Iranian territory'),
 ('airsp1231','k139','Iran full airspace closure by Dec 31','Iran — escalation','INPUT',(31.5,44),'general closure by Dec 31'),
 ('saudi930','k477','Iran targets Saudi Arabia by Sep 30','Iran — escalation','INPUT',(21.5,37),'Iranian strike on Saudi territory'),
 ('saudi915','k279','Iran targets Saudi Arabia by Sep 15','Iran — escalation','INPUT',(9.5,14),'by Sep 15'),
 ('qatar930','k365','Iran targets Qatar by Sep 30','Iran — escalation','INPUT',(20,30),'Iranian strike on Qatari territory'),
 ('oman930','k324','Iran targets Oman by Sep 30','Iran — escalation','INPUT',(5,8),'Iranian strike on Omani territory'),
 ('bab930','k38','Bab el-Mandeb effectively closed by Sep 30','Iran — escalation','INPUT',(8.85,18),'IMF PortWatch 7-day avg ≤ 10 transits'),
 ('bab1031','k183','Bab el-Mandeb effectively closed by Oct 31','Iran — escalation','INPUT',(19.5,28),'by Oct 31'),
 ('bab1231','k93','Bab el-Mandeb effectively closed by Dec 31','Iran — escalation','INPUT',(23.5,33),'by Dec 31'),
 ('houthi930','k503','Houthi military action against Israel by Sep 30','Iran — escalation','INPUT',(6.35,15),'credible reporting'),
 ('invade','k0','US invades Iran before 2027','Iran — escalation','INPUT',(15.5,21),'offensive to hold Iranian territory'),
 ('kharg930','k66','Kharg Island no longer Iranian by Sep 30','Iran — escalation','INPUT',(1.15,3.3),'established control by another force'),
 ('kharg1231','k145','Kharg Island no longer Iranian by Dec 31 (held 125 sh)','Iran — escalation','INPUT',(7.5,13),'by Dec 31'),
 ('isl930','k246','Farsi/Hengam/Hormuz/Kharg no longer Iranian by Sep 30 (held 296.93 sh)','Iran — escalation','INPUT',(2.05,5),'any of four islands'),
 ('ground','k291','Israel ground operation in Iran by Dec 31','Iran — escalation','INPUT',(12.5,16),'confirmed ground op'),
 ('regime','k5','Iranian regime falls before 2027','Iran — escalation','INPUT',(6.5,8.3),'consensus of credible reporting'),
 ('lead1231','k20','Iran leadership change by Dec 31','Iran — escalation','INPUT',(13.5,15.6),'Supreme Leader / president change'),
 ('coup','k249','Iran coup attempt by Dec 31','Iran — escalation','INPUT',(9.5,11.3),'credible reporting'),
 ('warcong','k80','US officially declares war on Iran by Dec 31','Iran — escalation','INPUT',(2,3.2),'Congressional declaration'),
 ('kuwait','k443','Iran invades Kuwait by Oct 31','Iran — escalation','INPUT',(1.3,2.6),'ground incursion'),
 ('euro','k604','European country takes military action on Iran by Oct 31','Iran — escalation','INPUT',(3,4.65),'strike or deployment'),
 ('normdec','k10','Hormuz traffic returns to normal by Dec 31','Iran — Hormuz','INPUT',(15.5,8.2),'PortWatch 7-day avg ≥ 60 transits'),
 ('normnov','k140','Hormuz traffic returns to normal by Nov 30','Iran — Hormuz','INPUT',(9.5,5),'by Nov 30'),
 ('normoct','k95','Hormuz traffic returns to normal by Oct 31','Iran — Hormuz','INPUT',(6,3),'by Oct 31'),
 ('normsep','k13','Hormuz traffic returns to normal by Sep 30','Iran — Hormuz','INPUT',(1.5,0.7),'by Sep 30'),
 ('notnorm','k147','Hormuz traffic does NOT return to normal in 2026','Iran — Hormuz','INPUT',(85.5,92),'no month ≥ 60'),
 ('zero930','k283','0 ships transit Hormuz on any date by Sep 30','Iran — Hormuz','INPUT',(25,33),'PortWatch daily = 0'),
 ('ships20','k579','≥ 20 ships transit Hormuz on any day by Sep 30','Iran — Hormuz','INPUT',(12.5,8),'PortWatch daily ≥ 20'),
 ('oman930a','k110','Iran–Oman Hormuz agreement by Sep 30','Iran — Hormuz','INPUT',(26,14),'announced management agreement'),
 ('oman1031a','k237','Iran–Oman Hormuz agreement by Oct 31','Iran — Hormuz','INPUT',(45.5,28),'by Oct 31'),
 ('usirh930','k181','US–Iran Hormuz agreement by Sep 30','Iran — Hormuz','INPUT',(4.25,2.5),'by Sep 30'),
 ('fees1031','k115','Iran charges Hormuz fees by Oct 31','Iran — Hormuz','INPUT',(12.5,14),'announced and collected'),
 ('fees1231','k179','Iran charges Hormuz fees by Dec 31','Iran — Hormuz','INPUT',(27,29),'by Dec 31'),
 ('lifted','k447','Iran blockade lifted before an Iran–Oman agreement','Iran — Hormuz','INPUT',(22.5,20),'ordering of two events'),
 ('sanc930','k397','US reissues Iran oil sanction relief by Sep 30','Iran — diplomacy','INPUT',(5,3),'waiver / license'),
 ('sanc1031','k497','US reissues Iran oil sanction relief by Oct 31','Iran — diplomacy','INPUT',(13,10.6),'by Oct 31'),
 ('meet1231','k156','US × Iran diplomatic meeting by Dec 31','Iran — diplomacy','INPUT',(34.5,30),'by Dec 31'),
 ('deal1231','k37','US–Iran final nuclear deal by Dec 31','Iran — diplomacy','INPUT',(9.5,7),'signed deal'),
 ('nuke','k62','Iran nuke before 2027','Iran — diplomacy','INPUT',(4.75,5.5),'credible confirmation'),
 ('spr280','k312','US SPR crude ≤ 280M bbl by Sep 25','Oil — other','INPUT',(77.6,85),'EIA weekly SPR stocks (draws accelerate under $130)'),
 ('gastax','k376','Federal gas tax suspended by Nov 2','Oil — other','INPUT',(3.2,9),'pre-midterm relief becomes live at $130'),
 ('opecleave','k190','Another country leaves OPEC in 2026','Oil — other','INPUT',(36,36),'flat — not an oil-price event'),
]
out=[]
for key,bk,label,grp,meth,mk,note in ROWS:
    b=B.get(bk)
    if b is None:
        out.append(dict(key=key,book=bk,label=label,group=grp,method='NONE',url='https://polymarket.com/event/spx-hit-dec-2026',note=note,bid=None,ask=None,mid=None,p_unc=None,p_cond=None,lift=None,cond_yes=None,cond_no=None,side='—',fair=None,px=None,rv=None,cap=0,capsh=0,uedge=None,usd_b=0,usd_a=0,liq='NO BOOK',p5b=0,p5a=0)); continue
    bid,ask=b['bid'],b['ask']; mid=(bid+ask)/2
    if meth=='MODEL':
        pu=PU(mk); pc=PC(mk); lift=pc/pu if pu>0 else None; cy=pc; cn=100-pc; uy=pu
    elif meth=='LIFT':
        pu=PU(mk); pc=PC(mk)
        # odds-space (likelihood-ratio) update of the market mid: odds_cond = odds_mid × [pc/(1-pc)] / [pu/(1-pu)] — normalised by construction, well-behaved in the tails
        pu_=min(max(pu,0.05),99.95)/100; pc_=min(max(pc,0.05),99.95)/100; m_=min(max(mid,0.05),99.95)/100
        LR=(pc_/(1-pc_))/(pu_/(1-pu_)); oc=(m_/(1-m_))*LR; cy=100*oc/(1+oc); cn=100-cy
        lift=cy/mid if mid>0 else None; uy=mid
        if pu<5.0 or pu>95.0: note=note+' · TAIL — model P outside 5–95, the odds update rests on a tail estimate; no ticket'
        tail=pu<5.0 or pu>95.0
    elif meth=='INPUT':
        pu0,pc=mk; pu=mid; lift=pc/pu if pu>0 else None; cy=pc; cn=100-pc; uy=pu
    yes_ask=ask; no_ask=100-bid
    rv_y=cy/yes_ask if yes_ask>0 else 0; rv_n=cn/no_ask if no_ask>0 else 0
    side='YES' if rv_y>=rv_n else 'NO'
    fair=cy if side=='YES' else cn; px=yes_ask if side=='YES' else no_ask; rv=fair/px
    # capturable dollars: levels of the chosen side priced under fair
    cap=0.0; capsh=0.0
    if side=='YES':
        for p,sz in b['asks']:
            if p<fair: cap+=p*sz/100; capsh+=sz
    else:
        for p,sz in b['bids']:
            if (100-p)<fair: cap+=(100-p)*sz/100; capsh+=sz
    uedge=(mid-uy) if meth in('MODEL','INPUT') else None
    depth=min(b['usd_b'],b['usd_a'])
    liq='NO MARKET' if depth<25 else 'THIN' if depth<250 else 'OK' if depth<2500 else 'DEEP'
    if ask-bid>15: liq='WIDE'
    if meth=='LIFT' and (pu<5.0 or pu>95.0): liq='TAIL'
    if key in ('hike3','up450'): liq='PROPAGATED'
    out.append(dict(key=key,book=bk,label=label,group=grp,method=meth,url=url(bk),note=note,bid=bid,ask=ask,mid=mid,
                    p_unc=pu,p_cond=pc,lift=lift,cond_yes=cy,cond_no=cn,side=side,fair=fair,px=px,rv=rv,cap=cap,capsh=capsh,
                    uedge=uedge,usd_b=b['usd_b'],usd_a=b['usd_a'],liq=liq,p5b=b['p5b'],p5a=b['p5a'],q=S[bk][1],tok=S[bk][5],nb=b['nb'],na=b['na']))
json.dump({'rows':out,'p_touch':P_TOUCH,'p_close':P_CLOSE,'wb':wb,'wl':wl},open('/tmp/oil/table_oil.json','w'),indent=1)
print('P(touch) mixture',round(P_TOUCH*100,1),'base',round(MB['p_touch']*100,1),'vol07',round(ML['p_touch']*100,1),'wb',round(wb,3))
print(f"{'key':10s} {'grp':16s} {'bid':>5s} {'ask':>5s} {'Punc':>6s} {'P|C':>6s} {'lift':>5s} side {'fair':>6s} {'px':>5s} {'RV':>5s} {'cap$':>6s} liq")
for r in sorted(out,key=lambda r:-(r['rv'] or 0)):
    if r['rv'] is None: continue
    print(f"{r['key']:10s} {r['group'][:16]:16s} {r['bid']:5.1f} {r['ask']:5.1f} {(r['p_unc'] if r['p_unc'] is not None else -1):6.1f} {(r['p_cond'] if r['p_cond'] is not None else -1):6.1f} {(r['lift'] or 0):5.2f} {r['side']:3s} {r['fair']:6.1f} {r['px']:5.1f} {r['rv']:5.2f} {r['cap']:6.0f} {r['liq']}")
