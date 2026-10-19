from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b',panel:'#141e2e',line:'#2a3950'};\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"
TREE_JS = r"""
function tnode(svg,id,x,y,txt,kind,w){w=w||300;const g=S('g',{id:id},svg);
 S('rect',{x:x-w/2,y:y-34,width:w,height:68,rx:kind==='leaf'?34:12,fill:C.panel,stroke:C.line,'stroke-width':2.5,class:'nb'},g);
 S('text',{x:x,y:y+10,'text-anchor':'middle',fill:kind==='leaf'?(txt.startsWith('1')?C.bad:C.good):C.text,'font-size':28,style:"font-family:'Plex Mono'"},g,txt);return g;}
function tedge(svg,id,x1,y1,x2,y2,lab,side){const g=S('g',{id:id},svg);S('line',{x1,y1,x2,y2,stroke:'#4a5a74','stroke-width':4,class:'eb'},g);
 S('text',{x:(x1+x2)/2+(side==='l'?-16:16),y:(y1+y2)/2,'text-anchor':side==='l'?'end':'start',fill:C.muted,'font-size':23},g,lab);return g;}
function hl(ids,on){ids.forEach(i=>{const g=document.getElementById(i);if(!g)return;g.querySelectorAll('.nb,.eb').forEach(e=>{e.setAttribute('stroke',on?C.hl:(e.classList.contains('eb')?'#4a5a74':C.line));});});}
"""

# ---------------------------------------------------------------- 0 intro
s0_js = C_JS + TREE_JS + r"""
function init(){const m=document.getElementById('motif');
 const L=(x1,y1,x2,y2)=>S('line',{x1,y1,x2,y2,stroke:'#33445e','stroke-width':5},m);
 L(310,110,170,280);L(310,110,450,280);L(450,280,350,450);L(450,280,550,450);
 const N=(x,y,c)=>S('rect',{x:x-60,y:y-30,width:120,height:60,rx:12,fill:'#0c1320',stroke:c,'stroke-width':5},m);
 N(310,110,C.hl);N(450,280,'#7d8ca3');
 const Lf=(x,y,c)=>S('rect',{x:x-50,y:y-28,width:100,height:56,rx:28,fill:'#0c1320',stroke:c,'stroke-width':5},m);
 Lf(170,280,C.good);Lf(350,450,C.good);Lf(550,450,C.bad);}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 5 of 8</div>
  <div class="t1">CART:<br>decision trees</div>
  <div class="t2">The second-biggest topic: 47 of 300 points</div>
  <div class="chips" style="max-width:1000px"><span>Greedy splits</span><span>Impurity</span><span>Reading trees</span><span>Step functions</span><span>cp and R²</span><span>Choosing cp</span><span>Costs</span></div>
</div>
<svg class="motif" id="motif" width="620" height="560" viewBox="0 0 620 560"></svg>""", [
    Step("""CART is the second-biggest topic on these midterms. Every question comes down to a few ideas: how a split is chosen,
how to read a tree, what cp does, and how costs change the leaves.""")], script=s0_js)

# ---------------------------------------------------------------- 1 greedy splits
s1 = Scene("How CART chooses splits", "How CART grows a tree", r"""
<div class="row flow" style="gap:0;align-items:center">
 <div class="card fb"><div class="lab">At each node</div><div class="small" style="margin-top:6px">Try every variable and every cut point</div></div><div class="arr">→</div>
 <div class="card fb"><div class="lab">Keep the best cut</div><div class="small" style="margin-top:6px">Biggest drop in impurity: Gini, error rate, or RSS</div></div><div class="arr">→</div>
 <div class="card fb"><div class="lab">Recurse</div><div class="small" style="margin-top:6px">Repeat on each child</div></div><div class="arr">→</div>
 <div class="card fb"><div class="lab">Prune</div><div class="small" style="margin-top:6px">Drop splits that gain less than cp</div></div>
</div>
<div class="card hl" data-in="1" style="margin-top:34px"><div class="lab">PM3 · short answer 2c · why only AverageScore?</div>
 <div style="margin-top:10px">At each of those nodes, its best cut lowered RSS more than any cut on the other three variables.</div>
 <div class="small muted" style="margin-top:8px">Intuition: it's by far the strongest predictor (correlation −0.76 with Winnings). The rubric deducts if you skip how CART picks splits.</div></div>""", [
    Step("""CART grows a tree greedily. At each node, it tries every variable and every cut point, and keeps the single cut that lowers impurity the most:
Gini or error rate for classification, the residual sum of squares for regression. Then it repeats on each child.
Afterward, it prunes any split that improved the fit by less than cp."""),
    Step("""Practice midterm three asks why AverageScore was the only variable used in the golf tree. The precise answer: at each of those nodes,
its best cut lowered the RSS more than any cut on the other three variables. The intuition: it's by far the strongest predictor,
with a correlation of minus 0.76 with winnings. The rubric takes points off if you skip how CART picks splits."""),
], css=".fb{width:370px;min-height:170px}.arr{font-size:46px;color:var(--faint);padding:0 12px}")

# ---------------------------------------------------------------- 2 impurity
s2_js = C_JS + r"""
function init(){const s=document.getElementById('imp');const X=sc(0,1,90,640),Y=sc(0,0.55,420,40);
 axes(S('g',{},s),X,Y,0,1,0,0.55,[0,0.25,0.5,0.75,1],[0,0.25,0.5],'p = share of one class in the node',null,v=>String(v));
 S('path',{d:P(range(0,1,200).map(p=>[X(p),Y(2*p*(1-p))])),fill:'none',stroke:C.hl,'stroke-width':5},s);
 S('path',{d:P(range(0,1,200).map(p=>[X(p),Y(Math.min(p,1-p))])),fill:'none',stroke:C.text,'stroke-width':4,'stroke-dasharray':'12 8'},s);
 S('text',{x:X(0.5),y:Y(0.5)-14,'text-anchor':'middle',fill:C.text,'font-size':24},s,'both peak at 0.5');
 const sh=document.getElementById('shapes');const shapes=[['A',p=>0.45*Math.sin(2*Math.PI*p)**2],
  ['B',p=>0.5-Math.abs(p-0.5)],['C',p=>Math.sin(Math.PI*p)*0.5],['D',p=>2*(p-0.5)**2]];
 shapes.forEach(([n,f],i)=>{const ox=i*190;const x=sc(0,1,ox+20,ox+170),y=sc(0,0.55,150,20);const ok=(n==='B'||n==='C');
  S('rect',{x:ox+6,y:6,width:178,height:186,rx:14,fill:C.panel,stroke:ok?C.good:C.line,'stroke-width':3},sh);
  S('path',{d:P(range(0,1,80).map(p=>[x(p),y(f(p))])),fill:'none',stroke:ok?C.good:C.muted,'stroke-width':4},sh);
  S('text',{x:ox+95,y:180,'text-anchor':'middle',fill:ok?C.good:C.muted,'font-size':24,'font-weight':600},sh,n+(ok?'  ✓':'  ✗'));});}
"""
s2 = Scene("Impurity functions", "What makes a good impurity function", r"""
<div class="row" style="gap:46px;align-items:center">
 <div><svg id="imp" width="680" height="500" viewBox="0 0 680 500"></svg><div class="small" style="margin-left:90px"><span class="yel">━</span> Gini 2p(1−p) &nbsp;&nbsp; <span>┅</span> error min(p, 1−p)</div></div>
 <div class="col" style="flex:1;gap:20px">
  <div class="card"><div class="small">Zero for a pure node, highest at a 50/50 mix, and <b class="yel">concave</b> (an upside-down bowl).</div></div>
  <div class="card" data-in="1"><div class="lab">PM2 · Q13 · answer C: only B and C</div>
   <svg id="shapes" width="760" height="200" viewBox="0 0 760 200" style="margin-top:10px"></svg>
   <div class="small muted" style="margin-top:6px">Concave means a split never raises total impurity.</div></div>
  <div class="card" data-in="2"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">PM3 · Q6 · "always strictly decreases"</div><span class="verdict f">FALSE</span></div>
   <div class="small" style="margin-top:6px">It can stay the same, e.g. both children keep the parent's majority class.</div></div>
 </div>
</div>""", [
    Step("""To score a cut, CART uses an impurity function of the class mix in a node. A good one is zero for a pure node,
highest at a fifty-fifty mix, and concave, shaped like an upside-down bowl. Gini and error rate both qualify."""),
    Step("""Why concave? A parent's mix is a weighted average of its children's mixes, and for a concave function, the children's average impurity
can't exceed the parent's. So a split never increases total impurity. On practice midterm two, question thirteen,
the tent and the dome work, but the dip and the U-shape don't. The answer is only B and C."""),
    Step("""But never increasing isn't the same as always decreasing. A split can leave impurity unchanged, for example under error rate
when both children keep the parent's majority class. So the claim that impurity strictly decreases after every split is false."""),
], script=s2_js)

# ---------------------------------------------------------------- 3 reading a tree, missing values
s3_js = C_JS + TREE_JS + r"""
function init(){const t=document.getElementById('lt');
 tedge(t,'e1',330,94,170,206,'yes','l');tedge(t,'e2',530,94,690,206,'no','r');
 tedge(t,'e3',610,244,470,326,'yes','l');tedge(t,'e4',770,244,910,326,'no','r');
 tedge(t,'e5',400,394,330,466,'yes','l');tedge(t,'e6',540,394,610,466,'no','r');
 tnode(t,'n1',430,60,'fico ≥ 740','node',300);tnode(t,'l1',170,240,'0 · good','leaf',220);
 tnode(t,'n2',690,240,'inquiries < 3','node',300);tnode(t,'n3',470,360,'fico ≥ 665','node',300);
 tnode(t,'l2',910,360,'1 · bad','leaf',200);tnode(t,'l3',330,500,'0 · good','leaf',220);tnode(t,'l4',610,500,'1 · bad','leaf',200);}
function onStep(k){hl(['n1','n2','n3','e1','e2','e3','e4','e5','e6','l1','l2','l3','l4'],false);
 if(k===1)hl(['n1','e2','n2','e3','e4','n3','e6','l4','l2'],true);
 if(k===2)hl(['n1','e1','l1','e2','n2','e4','l2'],true);}
"""
s3 = Scene("Reading a tree", "Reading a tree, even with a missing value", r"""
<div class="row" style="gap:40px;align-items:center">
 <div><div class="lab" style="margin-bottom:8px">PM2 · Lending Club tree · 1 = bad risk · go left when true</div>
  <svg id="lt" width="1060" height="560" viewBox="0 0 1080 560"></svg></div>
 <div class="col" style="flex:1;gap:20px">
  <div class="card" data-in="1" data-hl="1"><div class="lab">FICO 650, inquiries unknown</div><div class="small" style="margin-top:6px">Every possible branch ends in 1.</div><div class="mono yel" style="margin-top:6px">bad risk</div></div>
  <div class="card" data-in="2" data-hl="2"><div class="lab">4 inquiries, FICO unknown</div><div class="small" style="margin-top:6px">FICO ≥ 740 gives good; below gives bad.</div><div class="mono yel" style="margin-top:6px">need the FICO score</div></div>
  <div class="card" data-in="3" data-hl="3"><div class="lab">PM1 tip</div><div class="small" style="margin-top:6px">On a 0/1 variable, "X &lt; 0.5" means X = 0. PM1's tree predicts a cancellation only for vehicle 12 booked on the mobile site.</div></div>
 </div>
</div>""", [
    Step("""Reading a tree: at each node, go left when the condition is true. Here's the Lending Club tree from practice midterm two,
where 1 means a bad risk."""),
    Step("""Part b: FICO is 650, and the number of inquiries is unknown. 650 is below 740, so go right. If inquiries are under 3,
we check whether FICO is at least 665. It isn't, so bad risk. If inquiries are 3 or more, also bad risk.
Every branch you can't rule out ends in bad risk, so that's the answer."""),
    Step("""Part c: 4 inquiries, FICO unknown. If FICO is at least 740, the tree says good risk. If not, 4 inquiries fails the under-3 check,
so bad risk. The branches disagree, so the answer is: you need the FICO score, and here's what each value gives."""),
    Step("""One more reading tip from midterm one: on a zero-one variable, X less than 0.5 just means X equals zero. That tree predicts a cancellation
only for vehicle model 12, booked on the mobile site."""),
], script=s3_js)

# ---------------------------------------------------------------- 4 regression tree = step function
s4_js = C_JS + TREE_JS + r"""
const rows=[[69,70.02,5.145],[70.02,70.52,2.897],[70.52,71.12,1.506],[71.12,72,0.8197]];
function init(){const t=document.getElementById('gt');
 tedge(t,'a1',250,94,140,196,'yes','l');tedge(t,'a2',350,94,470,196,'no','r');
 tedge(t,'a3',100,264,70,336,'yes','l');tedge(t,'a4',180,264,220,336,'no','r');
 tedge(t,'a5',430,264,390,336,'yes','l');tedge(t,'a6',510,264,550,336,'no','r');
 tnode(t,'g1',300,60,'score ≥ 70.52','node',280);tnode(t,'g2',140,230,'≥ 71.12','node',200);tnode(t,'g3',470,230,'≥ 70.02','node',200);
 const lf=(x,v)=>{const g=S('g',{},t);S('rect',{x:x-62,y:336,width:124,height:64,rx:32,fill:C.panel,stroke:C.line,'stroke-width':2.5},g);S('text',{x:x,y:378,'text-anchor':'middle',fill:C.hl,'font-size':26},g,v);};
 lf(70,'0.8197');lf(220,'1.506');lf(390,'2.897');lf(550,'5.145');
 const s=document.getElementById('sf');const X=sc(69,72,80,940),Y=sc(0,5.6,400,40);
 S('line',{x1:X(69),x2:X(72),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);S('line',{x1:X(69),x2:X(69),y1:Y(0),y2:Y(5.6),stroke:C.axis,'stroke-width':2},s);
 [69,70.02,70.52,71.12,72].forEach(v=>S('text',{x:X(v),y:Y(0)+34,'text-anchor':'middle',class:'tick'},s,String(v)));
 S('text',{x:X(70.5),y:Y(0)+74,'text-anchor':'middle',class:'axl'},s,'AverageScore');
 S('text',{x:0,y:0,'text-anchor':'middle',class:'axl',transform:`translate(30,${Y(2.8)}) rotate(-90)`},s,'Predicted winnings ($M)');
 rows.forEach(([a,b,v],i)=>{if(i>0)S('line',{x1:X(a),x2:X(a),y1:Y(0),y2:Y(v),stroke:'#223047','stroke-width':2,'stroke-dasharray':'5 6'},s);
  S('line',{x1:X(a),x2:b<72?X(b)-6:X(b),y1:Y(v),y2:Y(v),stroke:C.hl,'stroke-width':5},s);
  if(a>69)S('circle',{cx:X(a),cy:Y(v),r:8,fill:C.hl,class:'dot'},s);
  if(b<72)S('circle',{cx:X(b),cy:Y(v),r:8,fill:'#0c1320',stroke:C.hl,'stroke-width':3,class:'dot'},s);
  S('text',{x:(X(a)+X(b))/2,y:Y(v)-16,'text-anchor':'middle',fill:C.text,'font-size':26,'font-weight':600},s,String(v));});}
"""
s4 = Scene("Regression trees", "Regression trees are step functions", r"""
<div class="row" style="gap:30px;align-items:center">
 <div><div class="lab" style="margin-bottom:8px">PM3 · golf tree · leaves in $M</div><svg id="gt" width="640" height="420" viewBox="0 0 640 420"></svg></div>
 <div data-in="1"><svg id="sf" width="1000" height="500" viewBox="0 0 1000 500"></svg></div>
</div>
<div class="card" data-in="2" style="margin-top:10px"><div class="small"><b class="yel">Rubric:</b> label both axes · flat steps, not a continuous line ·
 filled dot where the split uses ≥ (the left end of each step), open dot at the right end</div></div>""", [
    Step("""Regression trees predict a number. Each leaf predicts the average of its training points.
Here's the golf tree from practice midterm three, where every split is on average score."""),
    Step("""So the prediction, as a function of average score, is a step function: flat inside each region, jumping at each cut.
Below 70.02, it predicts 5.145 million. Then 2.897, then 1.506, and from 71.12 up, 0.8197."""),
    Step("""The rubric checks the details. Label both axes, and draw flat steps, not a continuous line. Because the splits use greater than or equal,
each cut value belongs to the step on its right: a filled dot at the left end of each step, and an open dot at its right end."""),
], script=s4_js)

# ---------------------------------------------------------------- 5 cp and R2 bounds
s5_js = C_JS + r"""
function init(){const s=document.getElementById('nl');const X=sc(0.66,0.73,60,1540);const y=120;
 S('line',{x1:X(0.66),x2:X(0.73),y1:y,y2:y,stroke:C.axis,'stroke-width':3},s);
 [0.67,0.68,0.69,0.70,0.71,0.72].forEach(v=>{S('line',{x1:X(v),x2:X(v),y1:y-8,y2:y+8,stroke:C.axis,'stroke-width':2},s);S('text',{x:X(v),y:y+44,'text-anchor':'middle',class:'tick'},s,v.toFixed(2));});
 S('rect',{x:X(0.704),y:y-18,width:X(0.714)-X(0.704),height:36,rx:8,fill:'rgba(79,209,139,.25)',stroke:C.good,'stroke-width':3,'data-in':1},s);
 S('text',{x:(X(0.704)+X(0.714))/2,y:y-44,'text-anchor':'middle',fill:C.good,'font-size':26,'data-in':1},s,'add a split: [0.704, 0.714]');
 S('rect',{x:X(0.66),y:y-18,width:X(0.694)-X(0.66),height:36,rx:8,fill:'rgba(255,107,107,.18)',stroke:C.bad,'stroke-width':3,'data-in':2},s);
 S('text',{x:X(0.672),y:y-44,'text-anchor':'middle',fill:C.bad,'font-size':26,'data-in':2},s,'remove a kept split: [0, 0.694] ←');
 S('circle',{cx:X(0.704),cy:y,r:12,fill:C.hl},s);S('text',{x:X(0.704),y:y+86,'text-anchor':'middle',fill:C.hl,'font-size':26},s,'current R² = 0.704');}
"""
s5 = Scene("cp and the R² bounds", "cp sets hard bounds on training R²", r"""
<div class="card"><div class="lab">The rule</div><div style="margin-top:8px">A split survives pruning only if it raises training R² by <b class="yel">at least cp</b>. Bigger cp → smaller tree. cp = 0 keeps everything.</div></div>
<div class="lab" style="margin:30px 0 4px">PM3 · golf tree · R² = 0.704 · cp = 0.01</div>
<svg id="nl" width="1720" height="230" viewBox="0 0 1600 230"></svg>
<div class="row" style="gap:24px">
 <div class="card" data-in="1" style="flex:1"><div class="small"><b>Add a split:</b> R² can't fall, and a gain above 0.01 would have been kept.</div></div>
 <div class="card" data-in="2" style="flex:1"><div class="small"><b>Remove the bottom-right split:</b> it was kept, so it added ≥ 0.01.</div></div>
</div>""", [
    Step("""Now cp, the complexity parameter. In the pruning phase, a split survives only if it improves the fit by at least cp.
For a regression tree, that means raising training R squared by at least cp. A bigger cp gives a smaller tree,
and a cp of zero keeps everything and overfits."""),
    Step("""Practice midterm three: the tree has a training R squared of 0.704, with cp equal to 0.01. Add one more split to a leaf.
Splits never lower training R squared, so it's at least 0.704. And if the new split had added more than 0.01, pruning would have kept it.
So the most definitive answer is the interval from 0.704 to 0.714."""),
    Step("""Now remove the bottom right split instead. That split was kept, so it must have added at least 0.01.
Removing it drops R squared to at most 0.694. The answer is the interval from 0 to 0.694."""),
], script=s5_js)

# ---------------------------------------------------------------- 6 choosing cp by CV
s6_js = C_JS + r"""
const cps=[],loss=[],acc=[];
const L=[[0,0,0.3633967,0.9212705],[1,11,0.3617089,0.9229582],[12,15,0.3723178,0.9255006],[16,16,0.3785430,0.9280430],[17,17,0.3892983,0.9348226],
 [18,19,0.3938286,0.9390599],[20,21,0.3962402,0.9454159],[22,23,0.3959629,0.9500769],[24,39,0.3944210,0.9559841],[40,40,0.3897600,0.9606451]];
L.forEach(([a,b,l,c])=>{for(let i=a;i<=b;i++){cps.push(i/1000);loss.push(l);acc.push(c);}});
function chart(id,vals,y0,y1,lab,fmt,pick,col){const s=document.getElementById(id);const X=sc(0,0.04,110,960),Y=sc(y0,y1,250,40);
 axes(S('g',{},s),X,Y,0,0.04,y0,y1,[0,0.01,0.02,0.03,0.04],[y0,(y0+y1)/2,y1],null,null,fmt);
 S('text',{x:X(0),y:20,fill:C.text,'font-size':23},s,lab);
 S('path',{d:P(cps.map((c,i)=>[X(c),Y(vals[i])])),fill:'none',stroke:col,'stroke-width':4},s);
 cps.forEach((c,i)=>S('circle',{cx:X(c),cy:Y(vals[i]),r:4,fill:col},s));
 S('circle',{cx:X(pick),cy:Y(vals[Math.round(pick*1000)]),r:13,fill:'none',stroke:C.hl,'stroke-width':4,'data-in':id==='cl'?1:2},s);}
function init(){chart('cl',loss,0.355,0.40,'Average loss (lower is better)',v=>v.toFixed(3),0.011,C.text);chart('ca',acc,0.915,0.965,'Accuracy (higher is better)',v=>v.toFixed(3),0.040,C.muted);
 const s=document.getElementById('cl');const X=sc(0,0.04,110,960),Y=sc(0.355,0.40,250,40);
 S('rect',{x:X(0.001)-8,y:Y(0.3617089)-16,width:X(0.011)-X(0.001)+16,height:32,rx:8,fill:'rgba(255,216,74,.12)','data-in':1},s);
 [0,0.01,0.02,0.03,0.04].forEach(v=>S('text',{x:X(v),y:Y(0.355)+34,'text-anchor':'middle',class:'tick'},document.getElementById('ca'),''));}
"""
s6 = Scene("Choosing cp by cross-validation", "Choosing cp with cross-validation", r"""
<div class="row" style="gap:36px;align-items:center">
 <div class="col" style="gap:0">
  <div class="lab">PM1 · 10-fold CV · L_FN = 11.35, L_FP = 1</div>
  <svg id="cl" width="1000" height="300" viewBox="0 0 1000 300"></svg>
  <svg id="ca" width="1000" height="300" viewBox="0 0 1000 300"></svg>
  <div class="axl mono muted" style="margin-left:470px;font-size:23px">cp</div>
 </div>
 <div class="col" style="flex:1;gap:20px">
  <div class="card" data-in="1" data-hl="1"><div class="lab">By average loss</div><div class="mono" style="font-size:34px;margin-top:6px">cp = <span class="yel">0.011</span></div>
   <div class="small muted" style="margin-top:6px">Lowest loss 0.3617 is tied from 0.001 to 0.011. Ties go to the larger cp: the simpler tree.</div></div>
  <div class="card" data-in="2" data-hl="2"><div class="lab">By accuracy</div><div class="mono" style="font-size:34px;margin-top:6px">cp = 0.040</div>
   <div class="small muted" style="margin-top:6px">Highest accuracy 0.9606. With unequal costs, trust the loss.</div></div>
 </div>
</div>""", [
    Step("""Practice midterm one tuned cp with ten-fold cross-validation, using losses of 11.35 and 1.
The output reports both the average loss and the accuracy for each value of cp."""),
    Step("""By average loss, the lowest value, 0.3617, is tied from cp 0.001 all the way to 0.011. When there's a tie,
pick the largest cp, since it gives the simplest tree. So cp is 0.011."""),
    Step("""By accuracy, the best is 0.9606, at cp 0.040. But with imbalanced classes and unequal costs, trust the loss.
Chasing accuracy drifts toward the baseline: a tree that almost never predicts a cancellation."""),
], script=s6_js)

# ---------------------------------------------------------------- 7 costs in leaves + region plot
s7_js = C_JS + r"""
function init(){const s=document.getElementById('rg');
 S('rect',{x:20,y:20,width:560,height:400,fill:'none',stroke:C.axis,'stroke-width':3},s);
 [[220,20,220,420],[220,200,580,200],[400,200,400,420],[20,300,220,300]].forEach(([a,b,c,d])=>S('line',{x1:a,y1:b,x2:c,y2:d,stroke:C.muted,'stroke-width':3,'stroke-dasharray':'9 7'},s));
 const pt=(x,y,c)=>S('circle',{cx:x,cy:y,r:14,fill:c},s);
 pt(110,150,C.pos);pt(120,360,C.neg);pt(390,110,C.neg);pt(310,320,C.pos);pt(480,280,C.neg);pt(500,360,'#97a6bd');
 S('text',{x:500,y:368,'text-anchor':'middle',fill:'#0c1320','font-size':20,'font-weight':700},s,'?');
 S('rect',{x:404,y:204,width:172,height:212,fill:'rgba(255,216,74,.10)'},s);
 S('text',{x:490,y:240,'text-anchor':'middle',fill:C.hl,'font-size':22},s,'2 points');}
"""
s7 = Scene("Costs and region plots", "Costs in the leaves, and a region plot", r"""
<div class="row" style="gap:40px;align-items:stretch">
 <div class="card" style="flex:1"><div class="lab">A leaf predicts positive when</div>
  <span class="tex" data-d="1">\text{share of positives}&gt;\dfrac{L_{FP}}{L_{FP}+L_{FN}}=p^*</span>
  <div class="small" style="margin-top:12px">Same p* as decision analysis. With losses 11.35 and 1: <span class="mono yel">1 / 12.35 ≈ 0.081</span>.</div></div>
 <div class="card" data-in="1" style="flex:1.15"><div class="lab">PM3 · Q15 · 6 points, 5 regions</div>
  <div class="row" style="gap:20px;align-items:center;margin-top:8px"><svg id="rg" width="500" height="367" viewBox="0 0 600 440"></svg>
   <div class="small">One-point regions are always right. Only the two-point region can miss one.<div class="mono yel" style="margin-top:10px">5/6 ≤ A ≤ 1 (C)</div></div></div></div>
</div>""", [
    Step("""Costs also change what a leaf predicts. With losses L_FN and L_FP, a leaf predicts positive when its share of positives is above
L_FP over L_FP plus L_FN, the same p* as in decision analysis. With losses of 11.35 and 1, that's about 0.081."""),
    Step("""And a quick one from practice midterm three: six training points, five regions. A region with one point always classifies it correctly.
Only the region with two points could hold a mistake, and at worst it gets one wrong. So training accuracy is between five sixths and one: answer C."""),
], script=s7_js, css=KX)

# ---------------------------------------------------------------- 8 recap
s8 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:34px;gap:20px">
  <li><div>Greedy: at each node, the best cut over every variable and value. Then prune with cp.</div></li>
  <li><div>Impurity: 0 when pure, max at 50/50, concave. Splits never raise it, but may not lower it.</div></li>
  <li><div>Go left when true. Missing value: follow every branch you can't rule out.</div></li>
  <li><div>Regression tree = step function. Filled dot where the split uses ≥.</div></li>
  <li><div>Add a split: [R², R² + cp]. Remove a kept split: [0, R² − cp].</div></li>
  <li><div>Pick cp by CV loss, ties toward the larger cp. Leaves use the same p*.</div></li>
</ol>
<div class="next">Next · Video 6: Cross-validation and the bootstrap</div>""", [
    Step("""To recap. CART picks the best cut at each node, over every variable and value, then prunes with cp. A good impurity function is zero when pure,
peaks at fifty-fifty, and is concave, so splits never raise it, though they may not lower it. Go left when the condition is true, and with a missing value,
follow every branch you can't rule out. A regression tree is a step function. Adding a split keeps R squared within cp of where it was, and removing a kept split
drops it by at least cp. Pick cp by cross-validated loss. Next: cross-validation and the bootstrap.""", hold=1.5),
])

VIDEO = Video(5, "v05-cart", "CART decision trees", "CART",
              [s0, s1, s2, s3, s4, s5, s6, s7, s8])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
