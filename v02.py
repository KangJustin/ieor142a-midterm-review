from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b'};\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"

# ---------------------------------------------------------------- 0 intro
s0_js = C_JS + r"""
function init(){const m=document.getElementById('motif');const g=S('g',{opacity:0.9},m);
 const L=(x1,y1,x2,y2,c)=>S('line',{x1,y1,x2,y2,stroke:c||'#33445e','stroke-width':4},g);
 L(110,310,300,170);L(110,310,300,450);L(300,170,500,100);L(300,170,500,240);L(300,450,500,380);L(300,450,500,520);
 S('rect',{x:70,y:270,width:80,height:80,rx:6,fill:'#0c1320',stroke:C.hl,'stroke-width':5},g);
 [[300,170],[300,450]].forEach(([x,y])=>S('circle',{cx:x,cy:y,r:34,fill:'#0c1320',stroke:'#7d8ca3','stroke-width':5},g));
 [[100,C.bad],[240,C.good],[380,C.bad],[520,C.good]].forEach(([y,c])=>S('rect',{x:500,y:y-30,width:90,height:60,rx:10,fill:'#0c1320',stroke:c,'stroke-width':4},g));}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 2 of 8</div>
  <div class="t1">Decision analysis:<br>payoffs to a threshold</div>
  <div class="t2">One formula that shows up on every practice midterm</div>
  <div class="chips" style="max-width:1000px"><span>Decision trees</span><span>Expected value</span><span>Regret losses</span><span>p* = L_FP / (L_FP + L_FN)</span><span>Profit</span><span>Ensembles</span></div>
</div>
<svg class="motif" id="motif" width="620" height="620" viewBox="0 0 620 620"></svg>""", [
    Step("""Every practice midterm turns dollars into a probability threshold. In this video, you'll learn the one formula
that does it, why it works, and every way the exam uses it.""")], script=s0_js)

# ---------------------------------------------------------------- 1 the tree
s1_js = C_JS + r"""
function init(){
 const t=document.getElementById('tree');
 const line=(x1,y1,x2,y2,step)=>S('line',{x1,y1,x2,y2,stroke:'#5b6b85','stroke-width':4,'data-in':step},t);
 const lab=(x,y,txt,col,step,anchor,size)=>S('text',{x,y,'text-anchor':anchor||'middle',fill:col||C.text,'font-size':size||25,'data-in':step,style:"font-family:'Plex Sans'"},t,txt);
 line(108,310,404,165,0);line(108,310,404,455,0);
 S('rect',{x:52,y:282,width:56,height:56,rx:6,fill:'#0c1320',stroke:C.hl,'stroke-width':4},t);
 lab(80,380,'decide',C.muted,0,'middle',22);
 lab(262,192,'Keep the driver',C.text,0,'end',28);
 lab(236,452,'Reassign',C.vio,0,'middle',28);
 const node=(x,y,step)=>S('circle',{cx:x,cy:y,r:26,fill:'#0c1320',stroke:'#97a6bd','stroke-width':4,'data-in':step},t);
 const leaf=(y,txt,pay,col,step)=>{S('rect',{x:680,y:y-38,width:400,height:76,rx:14,fill:'#141e2e',stroke:'#2a3950','stroke-width':2,'data-in':step},t);
   lab(702,y+10,txt,C.text,step,'start',28);S('text',{x:1062,y:y+11,'text-anchor':'end',fill:col,'font-size':32,'font-weight':700,'data-in':step},t,pay);};
 line(456,165,680,95,1);line(456,165,680,235,1);node(430,165,1);
 lab(560,108,'p',C.pos,1,'middle',28);lab(560,232,'1 − p',C.neg,1,'middle',26);
 leaf(95,'Driver cancels','−$100',C.bad,1);leaf(235,'Driver shows up','+$25',C.good,1);
 line(456,455,680,385,2);line(456,455,680,525,2);node(430,455,2);
 lab(560,398,'0.001',C.muted,2,'middle',24);lab(560,522,'0.999',C.muted,2,'middle',24);
 leaf(385,'New driver cancels','−$110',C.bad,2);leaf(525,'New driver shows up','+$15',C.good,2);
}
"""
s1 = Scene("The YourCabs decision", "The YourCabs decision tree", r"""
<div class="row" style="gap:44px;align-items:center">
  <svg id="tree" width="1090" height="620" viewBox="0 0 1090 620"></svg>
  <div class="col" style="width:586px;gap:22px">
    <div class="card"><div class="lab">Practice midterm 1</div><div style="margin-top:8px">A booking comes in. The assigned driver cancels with probability <b class="pos">p</b>.</div></div>
    <div class="card" data-in="1"><div class="lab">Keep · expected payoff</div><span class="tex" data-d="1">-100p+25(1-p)=25-125p</span></div>
    <div class="card" data-in="2"><div class="lab">Reassign · expected payoff</div><span class="tex" data-d="1">0.001(-110)+0.999(15)=14.875</span></div>
  </div>
</div>""", [
    Step("""Here's the setup from practice midterm one. YourCabs gets a booking, and the assigned driver might cancel,
with probability p. YourCabs can keep the driver, or reassign the booking to a more reliable one."""),
    Step("""If they keep the driver and the driver cancels, they lose 100 dollars. If the driver shows up, they earn 25.
So keeping is worth 25 minus 125 p."""),
    Step("""If they reassign, the new driver almost never cancels: one time in a thousand, costing 110 dollars. Otherwise they earn 15.
That branch is worth 14.875 dollars, no matter what p is."""),
], script=s1_js, css=KX + ".card .katex{font-size:.86em}")

# ---------------------------------------------------------------- 2 EV lines
s2_js = C_JS + r"""
const X=sc(0,0.2,120,1000),Y=sc(0,26,540,40);
function init(){
 const s=document.getElementById('ev');
 S('rect',{x:X(0.081),y:Y(26),width:X(0.2)-X(0.081),height:Y(0)-Y(26),fill:'rgba(180,156,255,.08)','data-in':1},s);
 axes(S('g',{},s),X,Y,0,0.2,0,26,[0,0.05,0.1,0.15,0.2],[0,5,10,15,20,25],'p = chance the driver cancels','Expected payoff ($)',v=>String(v));
 S('path',{d:P([[X(0),Y(25)],[X(0.2),Y(0)]]),stroke:C.text,'stroke-width':5,fill:'none'},s);
 S('path',{d:P([[X(0),Y(14.875)],[X(0.2),Y(14.875)]]),stroke:C.vio,'stroke-width':5,fill:'none'},s);
 S('text',{x:X(0.012),y:Y(25)-14,fill:C.text,'font-size':26},s,'Keep: 25 − 125p');
 S('text',{x:X(0.2)-8,y:Y(14.875)-16,'text-anchor':'end',fill:C.vio,'font-size':26},s,'Reassign: 14.875');
 S('line',{x1:X(0.081),x2:X(0.081),y1:Y(0),y2:Y(26),stroke:C.hl,'stroke-width':3,'stroke-dasharray':'9 7','data-in':1},s);
 S('circle',{cx:X(0.081),cy:Y(14.875),r:12,fill:C.hl,stroke:'#0c1320','stroke-width':3,'data-in':1},s);
 S('text',{x:X(0.081)+16,y:Y(26)+30,fill:C.hl,'font-size':26,'data-in':1},s,'p* = 0.081');
 S('text',{x:X(0.035),y:Y(7),'text-anchor':'middle',fill:C.text,'font-size':26,'data-in':1},s,'keep wins');
 S('text',{x:X(0.155),y:Y(21),'text-anchor':'middle',fill:C.vio,'font-size':26,'data-in':1},s,'reassign wins');
}
"""
s2 = Scene("Expected value as a function of p", "Set the two expected payoffs equal", r"""
<div class="row" style="gap:40px;align-items:center">
  <svg id="ev" width="1060" height="640" viewBox="0 0 1060 640"></svg>
  <div class="col" style="width:620px;gap:22px">
    <div class="card"><div class="lab">Keep vs reassign</div><span class="tex" data-d="1">25-125p \;\text{ vs }\; 14.875</span></div>
    <div class="card hl" data-in="1"><div class="lab">They cross at</div><span class="tex" data-d="1">p^*=\dfrac{25-14.875}{125}=0.081</span>
      <div class="small muted" style="margin-top:8px">Reassign whenever p &gt; 0.081</div></div>
  </div>
</div>""", [
    Step("""Now plot each action's expected payoff against p. Keeping starts at 25 dollars and falls as cancellations get likelier.
Reassigning is flat at 14.875."""),
    Step("""Set them equal: 25 minus 125 p equals 14.875 gives p* equals 0.081. Below that, keeping the driver pays more.
Above it, reassign. That's the whole decision rule."""),
], script=s2_js, css=KX)

# ---------------------------------------------------------------- 3 regrets
s3 = Scene("Losses are regrets", "The shortcut: losses are regrets", r"""
<div class="lab" data-in="0" style="margin-bottom:22px">Positive = driver cancels &nbsp;·&nbsp; predict positive = reassign</div>
<div class="row" style="gap:40px">
  <div class="card" data-in="1" style="flex:1">
    <div class="lab pos">If the driver would cancel</div>
    <table class="t" style="width:100%;margin-top:10px"><tr><td>Reassign <span class="muted small">(right call)</span></td><td class="num">14.875</td></tr>
    <tr><td>Keep <span class="muted small">(a false negative)</span></td><td class="num">−100</td></tr>
    <tr class="hl"><td><b>Regret = L_FN</b></td><td class="num yel">114.875</td></tr></table>
  </div>
  <div class="card" data-in="2" style="flex:1">
    <div class="lab neg">If the driver would show up</div>
    <table class="t" style="width:100%;margin-top:10px"><tr><td>Keep <span class="muted small">(right call)</span></td><td class="num">25</td></tr>
    <tr><td>Reassign <span class="muted small">(a false positive)</span></td><td class="num">14.875</td></tr>
    <tr class="hl"><td><b>Regret = L_FP</b></td><td class="num yel">10.125</td></tr></table>
  </div>
</div>
<div class="card hl" data-in="3" style="margin-top:28px"><span class="tex" data-d="1">p^*=\dfrac{L_{FP}}{L_{FP}+L_{FN}}=\dfrac{10.125}{10.125+114.875}=\dfrac{10.125}{125}=0.081</span></div>
""", [
    Step("""There's a faster way that works on every exam: think in regrets. First, name the positive class. Here, it's a cancellation.
Predicting positive means taking the action you'd want for a positive, which is reassigning."""),
    Step("""If the driver really would cancel, reassigning beats keeping by 14.875 minus minus 100, which is 114.875.
Keeping in that world is a false negative, so that regret is L_FN."""),
    Step("""If the driver would show up, keeping beats reassigning by 25 minus 14.875, which is 10.125.
Reassigning in that world is a false positive, so that's L_FP."""),
    Step("Then the threshold is L_FP over L_FP plus L_FN: 10.125 over 125, which is 0.081. Same answer, no algebra."),
], css=KX)

# ---------------------------------------------------------------- 4 why it works
s4 = Scene("Why the formula works", "Why the formula works", r"""
<div class="col" style="gap:24px">
  <div class="card"><div class="row" style="gap:30px;align-items:center"><div style="width:520px"><b>Predict positive</b><div class="small muted">wrong only if actually negative</div></div>
    <div class="tex" style="font-size:44px">\text{expected loss}=(1-p)\,L_{FP}</div></div></div>
  <div class="card" data-in="1"><div class="row" style="gap:30px;align-items:center"><div style="width:520px"><b>Predict negative</b><div class="small muted">wrong only if actually positive</div></div>
    <div class="tex" style="font-size:44px">\text{expected loss}=p\,L_{FN}</div></div></div>
  <div class="card hl" data-in="2"><span class="tex" data-d="1" style="font-size:42px">(1-p)\,L_{FP}&lt;p\,L_{FN}\iff p&gt;\dfrac{L_{FP}}{L_{FP}+L_{FN}}=p^*</span></div>
  <div data-in="3" class="small"><b class="yel">Only the ratio matters.</b> 114.875 : 10.125 = 11.35 : 1, so PM1 can give CART the losses 11.35 and 1.</div>
</div>""", [
    Step("""Why does it work? If you predict positive, you're only wrong when the case is actually negative.
So your expected loss is one minus p, times L_FP."""),
    Step("If you predict negative, you're only wrong when the case is actually positive. Your expected loss is p times L_FN."),
    Step("""Predict positive when that first loss is smaller. Solve for p, and you get exactly p greater than L_FP over L_FP plus L_FN."""),
    Step("""Notice that multiplying both losses by the same number cancels out. Only the ratio matters. That's why practice midterm one
can give CART losses of 11.35 and 1 instead of the dollar amounts."""),
], css=KX)

# ---------------------------------------------------------------- 5 table across exams
s5 = Scene("One formula, every exam", "One formula, every exam", r"""
<table class="t" style="font-size:33px;width:100%">
  <tr><th>Question</th><th>Positive</th><th>Predict positive</th><th class="num">L_FN</th><th class="num">L_FP</th><th class="num">p*</th></tr>
  <tr><td>PM1 · Q7</td><td class="muted">given</td><td class="muted">given</td><td class="num">2</td><td class="num">1</td><td class="num">1/3</td></tr>
  <tr><td>PM1 · YourCabs</td><td>driver cancels</td><td>reassign</td><td class="num">114.875</td><td class="num">10.125</td><td class="num">0.081</td></tr>
  <tr data-in="1" data-hl="1"><td>PM2 · Lending Club</td><td>borrower defaults</td><td>don't fund</td><td class="num">4,000</td><td class="num">1,000</td><td class="num">0.20</td></tr>
  <tr data-in="2" data-hl="2"><td>PM3 · golf bet</td><td>winnings &gt; $2.5M</td><td>take the bet</td><td class="num">50</td><td class="num">100</td><td class="num">2/3</td></tr>
</table>""", [
    Step("""Here's the formula across all three practice midterms. Question seven on midterm one gives L_FN of 2 and L_FP of 1,
so p* is one third. YourCabs, as we just saw, is 0.081."""),
    Step("""For Lending Club, the positive class is a default. Funding a loan that defaults costs 4,000 dollars, and rejecting a good loan
gives up 1,000. So p* is 1,000 over 5,000, which is 0.2."""),
    Step("And for the golf bet on midterm three, p* is two thirds. That one has a twist."),
])

# ---------------------------------------------------------------- 6 golf bet
s6_js = C_JS + r"""
const X=sc(0,5.5,60,1000),Y=sc(0,0.5,300,30);
function init(){
 const s=document.getElementById('gc');const m=2.635,sd=0.89;
 const xs=range(0,5.5,300);
 const pts=[[X(2.5),Y(0)]];range(2.5,5.5,200).forEach(x=>pts.push([X(x),Y(npdf(x,m,sd))]));pts.push([X(5.5),Y(0)]);
 S('path',{d:P(pts)+'Z',fill:'rgba(255,154,61,.45)'},s);
 S('path',{d:P(xs.map(x=>[X(x),Y(npdf(x,m,sd))])),fill:'none',stroke:C.pos,'stroke-width':4},s);
 S('line',{x1:X(0),x2:X(5.5),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);
 [0,1,2,3,4,5].forEach(v=>S('text',{x:X(v),y:Y(0)+34,'text-anchor':'middle',class:'tick'},s,'$'+v+'M'));
 S('line',{x1:X(2.5),x2:X(2.5),y1:Y(0),y2:Y(0.5),stroke:C.hl,'stroke-width':3,'stroke-dasharray':'9 7'},s);
 S('text',{x:X(2.5)-12,y:Y(0.5)+18,'text-anchor':'end',fill:C.hl,'font-size':24},s,'$2.5M bar');
 S('line',{x1:X(2.635),x2:X(2.635),y1:Y(0),y2:Y(0.5),stroke:C.text,'stroke-width':2.5},s);
 S('text',{x:X(2.635)+14,y:Y(0.5)+18,fill:C.text,'font-size':24},s,'prediction $2.64M');
 const pr=1-ncdf(2.5,m,sd);
 S('text',{x:X(4.05),y:Y(0.27),fill:C.pos,'font-size':28},s,'P(win > 2.5) ≈ '+pr.toFixed(2));
}
"""
s6 = Scene("The golf bet", "The golf bet: is a prediction enough?", r"""
<div class="row" style="gap:30px;align-items:stretch">
  <div class="card" style="flex:1"><div class="lab">The bet · PM3</div><div style="margin-top:8px">Pay $100, get $150 back if winnings &gt; $2.5M. Net <b class="good">+$50</b> or <b class="bad">−$100</b>.</div>
    <div class="mono yel" style="margin-top:10px">bet when p &gt; 2/3</div></div>
  <div class="card" data-in="1" style="flex:1"><div class="lab">The regression says</div><div style="margin-top:8px">Predicted winnings ≈ <b>$2.64M</b></div>
    <div class="bad" style="margin-top:10px">An amount, not a probability</div></div>
  <div class="card hl" data-in="2" style="flex:1"><div class="lab">What you need</div><div style="margin-top:8px">A classifier for <b>P(winnings &gt; $2.5M)</b>, like logistic regression on a new 0/1 column.</div></div>
</div>
<div data-in="3" style="margin-top:20px"><svg id="gc" width="1060" height="350" viewBox="0 0 1060 350"></svg>
  <div class="abs small" style="right:0;bottom:60px;width:600px">Winnings scatter about $0.89M around the prediction, so p ≈ 0.56, below 2/3. <span class="muted">(normal approximation, for intuition)</span></div></div>
""", [
    Step("""On practice midterm three, you pay 100 dollars for a bet that returns 150 if a golfer wins more than 2.5 million dollars.
So you gain 50 or lose 100. Betting pays off on average when 50 p is bigger than 100 times one minus p, which means p above two thirds."""),
    Step("""The regression from that exam predicts about 2.64 million for this golfer, above the bar. But that's a predicted amount,
not a probability. You can't compare it with two thirds, so you can't decide yet."""),
    Step("""To decide, build a classifier, like a logistic regression on a new column: did winnings exceed 2.5 million?
Estimate p for this golfer, and bet only if p is above two thirds."""),
    Step("""For intuition: actual winnings scatter around the prediction by about 0.89 million. So the chance of clearing 2.5 million
is only around 0.56, below two thirds. A prediction above the bar is not a probability above the threshold."""),
], script=s6_js)

# ---------------------------------------------------------------- 7 profit
s7 = Scene("Profit from a confusion matrix", "Score the model in dollars, not accuracy", r"""
<div class="lab" style="margin-bottom:16px">PM1 · YourCabs test set · reassigned bookings are worth the expected $14.875</div>
<table class="t" style="font-size:34px;width:100%">
  <tr><th>Outcome</th><th class="num">Count</th><th class="num">Payoff each</th><th class="num">Total</th></tr>
  <tr><td>Kept, driver showed up <span class="muted small">(TN)</span></td><td class="num">909</td><td class="num">$25</td><td class="num">$22,725.00</td></tr>
  <tr><td>Kept, driver cancelled <span class="muted small">(FN)</span></td><td class="num">26</td><td class="num">−$100</td><td class="num">−$2,600.00</td></tr>
  <tr><td>Reassigned <span class="muted small">(FP + TP = 69 + 9)</span></td><td class="num">78</td><td class="num">$14.875</td><td class="num">$1,160.25</td></tr>
  <tr class="hl"><td><b>Model total</b></td><td class="num">1,013</td><td></td><td class="num yel">$21,285.25</td></tr>
</table>
<div class="card" data-in="1" style="margin-top:26px"><div class="row" style="gap:40px;align-items:center">
  <div style="flex:1">Never reassign: <span class="mono">978 × 25 − 35 × 100 = $20,950</span></div>
  <div class="mono yel">model +$335</div></div>
  <div class="small muted" style="margin-top:8px">The model wins on profit despite lower accuracy (0.906 vs 0.965).</div></div>
""", [
    Step("""To score a model in dollars, multiply each cell's count by its payoff and add. The model keeps 909 bookings that go fine,
at 25 dollars each. It keeps 26 that cancel, losing 100 each. And it reassigns 78, worth 14.875 each.
The total is 21,285 dollars and 25 cents."""),
    Step("""The baseline that never reassigns earns 978 times 25, minus 35 times 100: 20,950 dollars. So the model earns 335 dollars more,
even though its accuracy is lower. Accuracy is the wrong yardstick when errors cost different amounts."""),
])

# ---------------------------------------------------------------- 8 weighted errors = profit
s8 = Scene("Weighted errors and profit", "Why minimizing weighted errors maximizes profit", r"""
<div class="lab" style="margin-bottom:16px">PM2 · Lending Club · positive = default · fund good loan +$1,000 · fund default −$4,000 · reject $0</div>
<div class="col" style="gap:22px">
  <div class="card"><span class="tex" data-d="1">\text{Profit}=1000\cdot TN-4000\cdot FN</span></div>
  <div class="card" data-in="1"><span class="tex" data-d="1">TN=N_{neg}-FP\;\Longrightarrow\;\text{Profit}=1000\,N_{neg}-\left(4000\cdot FN+1000\cdot FP\right)</span></div>
  <div class="card hl" data-in="2"><b>N<sub>neg</sub> is fixed by the data.</b> Maximizing profit = minimizing 4000·FN + 1000·FP, so <span class="mono yel">L_FN = 4,000</span> and <span class="mono yel">L_FP = 1,000</span>.</div>
</div>""", [
    Step("""Practice midterm two asks you to justify the losses for Lending Club. A funded good loan earns 1,000 dollars,
a funded default loses 4,000, and a rejected loan earns nothing. Funded good loans are true negatives, and funded defaults are false negatives.
So profit is 1,000 TN minus 4,000 FN."""),
    Step("""Every actual negative is either a true negative or a false positive, so TN equals N negative minus FP.
Substitute, and profit becomes 1,000 times N negative, minus the quantity 4,000 FN plus 1,000 FP."""),
    Step("""N negative is fixed by the data. So maximizing profit is exactly the same as minimizing 4,000 FN plus 1,000 FP.
That's why L_FN is 4,000 and L_FP is 1,000."""),
], css=KX)

# ---------------------------------------------------------------- 9 ensembles
s9 = Scene("Thresholds with ensembles", "Thresholds when you combine trees", r"""
<div class="row" style="gap:40px;align-items:stretch">
  <div class="card" style="flex:1"><div class="lab">Each tree outputs a probability</div>
    <div style="margin-top:12px">Trained with equal losses.</div>
    <div style="margin-top:18px">Average the B probabilities, then compare with <b class="yel">p* = 0.2</b>.</div></div>
  <div class="card" data-in="1" style="flex:1"><div class="lab">Each tree outputs a 0/1 vote</div>
    <div style="margin-top:12px">Trained with L_FN = 4,000 and L_FP = 1,000.</div>
    <div style="margin-top:18px">Take a majority vote at <b class="yel">0.5</b>.</div>
    <div class="small bad" style="margin-top:14px">Using 0.2 here counts the costs twice.</div></div>
</div>
<div class="small muted" style="margin-top:26px">PM2 short answers 3d and 3e</div>""", [
    Step("""Last, ensembles. If each tree outputs a probability, average the B probabilities, then compare the average with p*,
0.2 for Lending Club."""),
    Step("""But if each tree was trained with the losses 4,000 and 1,000, its zero or one vote already includes the costs.
So take a simple majority at 0.5. Using 0.2 there would count the costs twice."""),
])

# ---------------------------------------------------------------- 10 recap
s10 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:36px;gap:24px">
  <li><div>A loss is a <b>regret</b>: the right action's payoff minus the wrong one's, in the outcome that happens.</div></li>
  <li><div><span class="mono yel">p* = L_FP / (L_FP + L_FN)</span>. Predict positive when p &gt; p*.</div></li>
  <li><div>Only the ratio of the losses matters.</div></li>
  <li><div>A predicted amount isn't a probability. Build a classifier for P(event).</div></li>
  <li><div>Profit = Σ count × payoff. Lower accuracy can still earn more.</div></li>
  <li><div>Average probabilities, then apply p*. Cost-trained 0/1 votes: majority at 0.5.</div></li>
</ol>
<div class="next">Next · Video 3: Linear regression and R output</div>""", [
    Step("""To recap. A loss is a regret: how much better the right action pays than the wrong one, in the world that actually happens.
The threshold is L_FP over L_FP plus L_FN, and only their ratio matters. A predicted amount is not a probability.
Score models by profit, not accuracy. And when you combine trees, apply p* to averaged probabilities,
but use a simple majority for cost-trained votes. Next up: linear regression.""", hold=1.5),
])

VIDEO = Video(2, "v02-decision", "Decision analysis - payoffs to a threshold", "Decision analysis",
              [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
