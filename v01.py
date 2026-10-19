from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63'};\n"

# ---------------------------------------------------------------- 0 intro
s0_js = C_JS + r"""
function init(){const m=document.getElementById('motif');const X=sc(0,1,40,580),Y=sc(0,1,580,40);
 const g=S('g',{opacity:0.9},m);[0,0.25,0.5,0.75,1].forEach(v=>{S('line',{x1:X(v),x2:X(v),y1:Y(0),y2:Y(1),stroke:'#1c2a40','stroke-width':2},g);S('line',{x1:X(0),x2:X(1),y1:Y(v),y2:Y(v),stroke:'#1c2a40','stroke-width':2},g);});
 S('line',{x1:X(0),y1:Y(0),x2:X(1),y2:Y(1),stroke:'#33445e','stroke-width':3,'stroke-dasharray':'10 10'},g);
 const f=x=>1-(1-x)**4;S('path',{d:P(range(0,1,200).map(x=>[X(x),Y(f(x))])),fill:'none',stroke:C.hl,'stroke-width':6,opacity:0.85},g);
 [0.05,0.15,0.3,0.5].forEach(x=>S('circle',{cx:X(x),cy:Y(f(x)),r:10,fill:'#0c1320',stroke:C.hl,'stroke-width':4},g));}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 1 of 8</div>
  <div class="t1">Classification metrics<br>and ROC curves</div>
  <div class="t2">Built from the Spring 2021 practice midterms 1 to 3</div>
  <div class="chips" style="max-width:1000px"><span>Confusion matrix</span><span>Accuracy · TPR · FPR</span><span>Baselines</span><span>ROC and AUC</span><span>Exam questions</span></div>
</div>
<svg class="motif" id="motif" width="620" height="620" viewBox="0 0 620 620"></svg>""", [Step("""Every classification question on this midterm comes down to four counts. Get those four right,
and accuracy, the true positive rate, the false positive rate, and the ROC curve are all just division.
Let's build them up, then use them on real questions from the practice midterms.""")], script=s0_js)

# ---------------------------------------------------------------- 1 confusion matrix
s1 = Scene("The confusion matrix", "The confusion matrix", """
<div class="row" style="gap:80px;align-items:center">
 <div class="cm" style="grid-template-columns:230px 360px 360px;grid-template-rows:90px 240px 240px">
   <div></div><div class="h">Predicted<br>negative</div><div class="h">Predicted<br>positive</div>
   <div class="h rh hn">Actually<br>negative</div>
   <div class="cell n"><div data-in="1" class="k neg">TN</div><div data-in="1" class="d">true negative</div></div>
   <div class="cell n"><div data-in="1" class="k neg">FP</div><div data-in="1" class="d">false positive</div></div>
   <div class="h rh hp">Actually<br>positive</div>
   <div class="cell p"><div data-in="2" class="k pos">FN</div><div data-in="2" class="d">false negative</div></div>
   <div class="cell p"><div data-in="2" class="k pos">TP</div><div data-in="2" class="d">true positive</div></div>
 </div>
 <div class="col" style="width:630px;gap:28px">
   <div><div class="lab">Rows</div>what actually happened</div>
   <div><div class="lab">Columns</div>what the model predicted</div>
   <div class="card" data-in="3" style="font-size:33px;margin-top:10px">
     <div class="lab" style="margin-bottom:12px">Decode any name</div>
     <div><b>Second word</b>: what the model predicted</div>
     <div><b>First word</b>: whether it was right</div>
     <div class="small muted" style="margin-top:14px">False negative = predicted negative, wrong,<br>so it was actually <span class="pos">positive</span></div>
   </div>
 </div>
</div>""", [
    Step("Start with the confusion matrix. The rows are what actually happened. The columns are what the model predicted."),
    Step("""The top row holds the actual negatives. A true negative is a negative the model got right.
A false positive is a negative it flagged by mistake."""),
    Step("""The bottom row holds the actual positives. A false negative is a positive the model missed.
A true positive is one it caught."""),
    Step("""Here's a quick way to decode the names. The second word is what the model predicted.
The first word says whether that prediction was right. So a false negative is a negative prediction that was wrong,
which means the case was actually positive."""),
], css=".cm .hn{color:var(--neg)}.cm .hp{color:var(--pos)}")

# ---------------------------------------------------------------- 2 three rates
s2 = Scene("Accuracy, TPR, FPR", "Three rates, three parts of the table", r"""
<div class="row" style="gap:70px;align-items:center">
  <div class="cm" style="grid-template-columns:190px 270px 270px;grid-template-rows:84px 190px 190px">
    <div></div><div class="h">Predicted<br>negative</div><div class="h">Predicted<br>positive</div>
    <div class="h rh hn">Actually<br>negative</div>
    <div class="cell n" data-hl="0 2" data-dim="1"><div class="k neg">TN</div></div>
    <div class="cell n" data-hl="2" data-dim="0 1"><div class="k neg">FP</div></div>
    <div class="h rh hp">Actually<br>positive</div>
    <div class="cell p" data-hl="1" data-dim="0 2"><div class="k pos">FN</div></div>
    <div class="cell p" data-hl="0 1" data-dim="2"><div class="k pos">TP</div></div>
  </div>
  <div class="col" style="flex:1;gap:20px">
    <div class="card" data-hl="0"><div class="lab">Accuracy · the whole table</div><span class="tex" data-d="1">\text{Accuracy}=\dfrac{TP+TN}{N}</span></div>
    <div class="card" data-in="1" data-hl="1"><div class="lab">TPR · bottom row, the actual positives</div><span class="tex" data-d="1">\text{TPR}=\dfrac{TP}{TP+FN}</span></div>
    <div class="card" data-in="2" data-hl="2"><div class="lab">FPR · top row, the actual negatives</div><span class="tex" data-d="1">\text{FPR}=\dfrac{FP}{FP+TN}</span></div>
    <div data-in="3" class="mono" style="font-size:30px;margin-left:6px">TNR = 1 − FPR &nbsp;&nbsp;·&nbsp;&nbsp; FNR = 1 − TPR</div>
  </div>
</div>""", [
    Step("Accuracy uses the whole table. Add up the diagonal, the cases the model got right, and divide by everything."),
    Step("""The true positive rate only looks at the bottom row, the actual positives. Of all the positives,
what fraction did the model catch? That's TP over TP plus FN."""),
    Step("""The false positive rate only looks at the top row, the actual negatives. Of all the negatives,
what fraction did the model wrongly flag? That's FP over FP plus TN."""),
    Step("The complements come for free. The true negative rate is one minus FPR, and the false negative rate is one minus TPR."),
], css=".cm .hn{color:var(--neg)}.cm .hp{color:var(--pos)}.katex-display{margin:.25em 0 0}.katex-display>.katex{text-align:left!important}")

# ---------------------------------------------------------------- 3 worked example
s3 = Scene("Worked example: YourCabs", "Worked example: YourCabs cancellations", r"""
<div class="lab" style="margin:-6px 0 22px">Practice midterm 1 · positive = driver cancels · logistic model · 1,013 test bookings</div>
<div class="row" style="gap:64px;align-items:flex-start">
  <div class="cm" style="grid-template-columns:160px 220px 220px 120px;grid-template-rows:80px 168px 168px 60px">
    <div></div><div class="h">Predicted<br>negative</div><div class="h">Predicted<br>positive</div><div class="h">Total</div>
    <div class="h rh hn">Actually<br>negative</div>
    <div class="cell n" data-hl="1 3"><div class="k neg">909</div><div class="d">TN</div></div>
    <div class="cell n" data-hl="3"><div class="k neg">69</div><div class="d">FP</div></div>
    <div class="tot" data-hl="3 5"><span class="tt">978</span></div>
    <div class="h rh hp">Actually<br>positive</div>
    <div class="cell p" data-hl="2"><div class="k pos">26</div><div class="d">FN</div></div>
    <div class="cell p" data-hl="1 2"><div class="k pos">9</div><div class="d">TP</div></div>
    <div class="tot" data-hl="2 5"><span class="tt">35</span></div>
    <div></div><div></div><div class="h" style="align-items:center;justify-content:flex-end">N =</div><div class="tot"><span class="tt">1,013</span></div>
  </div>
  <div style="position:relative;flex:1;height:600px">
    <div class="col abs" style="inset:0;gap:30px" data-out="4">
      <div class="calc" data-in="1"><div class="lab">Accuracy</div><div class="mono eq">(909 + 9) / 1,013 = <span class="yel">0.906</span></div></div>
      <div class="calc" data-in="2"><div class="lab">TPR · out of 35 actual positives</div><div class="mono eq">9 / 35 = <span class="yel">0.257</span></div></div>
      <div class="calc" data-in="3"><div class="lab">FPR · out of 978 actual negatives</div><div class="mono eq">69 / 978 = <span class="yel">0.071</span></div></div>
    </div>
    <div class="col abs" style="inset:0;gap:30px" data-in="4">
      <table class="t" style="font-size:32px">
        <tr><th></th><th class="num">Accuracy</th><th class="num">TPR</th><th class="num">FPR</th></tr>
        <tr><td>Model <span class="muted small">(threshold 0.081)</span></td><td class="num">0.906</td><td class="num">0.257</td><td class="num">0.071</td></tr>
        <tr class="hl"><td>Baseline <span class="muted small">(never cancel)</span></td><td class="num yel">0.965</td><td class="num bad">0</td><td class="num">0</td></tr>
      </table>
      <div class="card" data-in="5" style="margin-top:6px">
        <span class="tex" data-d="1">\text{Accuracy}=\dfrac{N_{pos}\cdot TPR+N_{neg}\cdot(1-FPR)}{N}</span>
        <div class="small muted" style="margin-top:6px">35 positives vs 978 negatives: 97% of the weight is on negatives.<br>PM3 Q12 states this identity: true.</div>
      </div>
    </div>
  </div>
</div>""", [
    Step("""Now real numbers, from practice midterm one. The positive class is a driver cancelling.
On 1,013 test bookings, the logistic model gives 909 true negatives, 69 false positives, 26 false negatives, and 9 true positives."""),
    Step("Accuracy is 909 plus 9, over 1,013. That's about 0.906."),
    Step("TPR is 9 over 35, about 0.257. The 35 is every actual cancellation, the whole bottom row."),
    Step("FPR is 69 over 978, about 0.071. The 978 is every booking that didn't cancel, the whole top row."),
    Step("""Now compare the baseline, which predicts the training set's majority class for everyone. Here, that's no cancellation.
Its accuracy is about 0.965, higher than the model's. But its TPR is zero. It never catches a single cancellation."""),
    Step("""Here's why. Accuracy is a weighted average of TPR and the true negative rate, weighted by class size.
With 35 positives and 978 negatives, about 97 percent of that weight is on the negatives.
Question twelve on practice midterm three states this identity, and it's true."""),
], css=""".cm .hn{color:var(--neg)}.cm .hp{color:var(--pos)}.cm .k{font-size:50px}
.cm .tot{justify-content:center;border-radius:14px;border:3px solid transparent}.cm .tot.hl{border-color:var(--hl)}
.cm .tt{font:600 30px 'Plex Mono',monospace;color:var(--text)}
.eq{font-size:50px;margin-top:6px}.katex-display{margin:.1em 0 0}.katex-display>.katex{text-align:left!important}""")

# ---------------------------------------------------------------- 4 quick true/false
def tf(label, q, verdict, cls, why, qin, ain):
    return f"""<div class="card" data-in="{qin}"><div class="row" style="gap:22px;align-items:baseline">
<span class="lab" style="min-width:150px">{label}</span><div style="flex:1">{q}</div></div>
<div class="row" style="gap:22px;align-items:center;margin-top:14px" data-in="{ain}"><span style="min-width:150px"><span class="verdict {cls}">{verdict}</span></span>
<div class="small muted" style="flex:1">{why}</div></div></div>"""

s4 = Scene("Quick true or false", "Quick checks from the multiple choice", '<div class="col" style="gap:26px">' +
    tf("PM1 · Q1", "Test accuracy is exactly 1, and both classes are present. Is TPR also 1?", "TRUE", "t",
       "Perfect accuracy means zero false negatives, so every positive was caught.", 0, 1) +
    tf("PM1 · Q2", "Test accuracy is 0.99. What's the most definitive thing you can say about TPR?", "0 TO 1", "a",
       "One positive in 100, missed: accuracy 0.99, TPR 0. Anything from 0 to 1 is possible.", 2, 3) +
    tf("PM3 · Q8", "True or false: changing the threshold doesn't change accuracy.", "FALSE", "f",
       "Accuracy, TPR and FPR all move with it. Lower the threshold and TPR and FPR both rise.", 4, 5) +
    "</div>", [
    Step("""Three quick checks from the multiple choice. Pause if you want to answer first. One.
If accuracy on the test set is exactly one, with both classes present, is TPR also one?""", hold=1.2),
    Step("True. Perfect accuracy means no false negatives, so every positive was caught."),
    Step("Two. Accuracy is 0.99. What's the most definitive thing you can say about TPR?", hold=1.2),
    Step("""Only that it's between zero and one. If one case in a hundred is positive and the model misses it,
accuracy is 0.99, and TPR is zero."""),
    Step("Three. True or false: changing the threshold doesn't change accuracy.", hold=1.0),
    Step("""False. Accuracy, TPR and FPR all depend on the threshold. Lower it, and the model predicts more positives,
so TPR and FPR both go up."""),
])

# ---------------------------------------------------------------- 5 ROC sweep (animated)
s5_js = C_JS + r"""
const st={};
const fn=x=>20*x*(1-x)**3, fp=x=>20*x**3*(1-x);
const TPR=c=>1-5*c**4+4*c**5, FPR=c=>5*(1-c)**4-4*(1-c)**5;
const X=sc(0,1,40,970), Y=sc(0,2.4,500,90);
const RX=sc(0,1,110,600), RY=sc(0,1,520,30);
function area(f,a,b){const n=Math.max(2,Math.round((b-a)*400));const pts=[[X(a),Y(0)]];range(a,b,n).forEach(x=>pts.push([X(x),Y(f(x))]));pts.push([X(b),Y(0)]);return P(pts)+'Z';}
function init(){
  const d=document.getElementById('dist');
  S('path',{d:area(fn,0,1),fill:'rgba(76,176,255,.10)'},d);
  S('path',{d:area(fp,0,1),fill:'rgba(255,154,61,.10)'},d);
  st.shN=S('path',{fill:'rgba(76,176,255,.45)'},d);
  st.shP=S('path',{fill:'rgba(255,154,61,.45)'},d);
  const xs=range(0,1,400);
  S('path',{d:P(xs.map(x=>[X(x),Y(fn(x))])),fill:'none',stroke:C.neg,'stroke-width':4},d);
  S('path',{d:P(xs.map(x=>[X(x),Y(fp(x))])),fill:'none',stroke:C.pos,'stroke-width':4},d);
  S('line',{x1:X(0),x2:X(1),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},d);
  [0,0.25,0.5,0.75,1].forEach(v=>S('text',{x:X(v),y:Y(0)+36,'text-anchor':'middle',class:'tick'},d,String(v)));
  S('text',{x:(X(0)+X(1))/2,y:Y(0)+80,'text-anchor':'middle',class:'axl'},d,'Predicted probability of being positive');
  S('circle',{cx:X(0)+10,cy:30,r:9,fill:C.neg},d);S('text',{x:X(0)+30,y:38,fill:C.text,'font-size':26},d,'Negatives');
  S('circle',{cx:X(0)+230,cy:30,r:9,fill:C.pos},d);S('text',{x:X(0)+250,y:38,fill:C.text,'font-size':26},d,'Positives');
  st.th=S('line',{y1:110,y2:Y(0),stroke:C.hl,'stroke-width':4,'stroke-dasharray':'10 8'},d);
  st.thl=S('text',{y:98,'text-anchor':'middle',fill:C.hl,'font-size':25},d);
  const r=document.getElementById('roc');
  axes(S('g',{},r),RX,RY,0,1,0,1,[0,0.25,0.5,0.75,1],[0,0.25,0.5,0.75,1],'FPR','TPR');
  st.diag=S('line',{x1:RX(0),y1:RY(0),x2:RX(1),y2:RY(1),stroke:C.muted,'stroke-width':2.5,'stroke-dasharray':'8 8','data-in':3},r);
  const cs=[];for(let v=1;v>=0;v-=0.002)cs.push(v);cs.push(0);
  const pts=cs.map(v=>[FPR(v),TPR(v)]);
  let auc=0;for(let i=1;i<pts.length;i++)auc+=(pts[i][0]-pts[i-1][0])*(pts[i][1]+pts[i-1][1])/2;
  S('path',{d:P([[RX(0),RY(0)]].concat(pts.map(p=>[RX(p[0]),RY(p[1])])).concat([[RX(1),RY(0)]]))+'Z',fill:'rgba(255,216,74,.09)','data-in':3},r);
  document.getElementById('auc').textContent=auc.toFixed(2);
  st.tr=S('path',{fill:'none',stroke:C.hl,'stroke-width':5,'stroke-linejoin':'round'},r);
  st.pt=S('circle',{r:11,fill:C.hl,stroke:'#0c1320','stroke-width':3,'data-in':1},r);
}
function draw(c,trace){
  st.th.setAttribute('x1',X(c));st.th.setAttribute('x2',X(c));
  st.thl.setAttribute('x',Math.min(Math.max(X(c),130),880));st.thl.textContent='threshold '+c.toFixed(2);
  st.shN.setAttribute('d',area(fn,c,1));st.shP.setAttribute('d',area(fp,c,1));
  const t=TPR(c),f=FPR(c);
  st.pt.setAttribute('cx',RX(f));st.pt.setAttribute('cy',RY(t));
  if(trace){const cs=[];for(let v=1;v>c;v-=0.003)cs.push(v);cs.push(c);st.tr.setAttribute('d',P(cs.map(v=>[RX(FPR(v)),RY(TPR(v))])));}
  else st.tr.setAttribute('d','');
  document.getElementById('rt').textContent=t.toFixed(2);document.getElementById('rf').textContent=f.toFixed(2);
}
function onStep(k){
  const vis=k===3?'hidden':'visible';[st.th,st.thl,st.shN,st.shP].forEach(e=>e.style.visibility=vis);
  if(k<=1)draw(0.6,false);
  if(k===2)draw(0.995,true);
  if(k===3){draw(0.0005,true);st.pt.style.visibility='hidden';} else st.pt.style.visibility='';
}
function anim(u,k){if(k===2)draw(0.995-0.99*u,true);}
"""
s5 = Scene("Where the ROC curve comes from", "Where the ROC curve comes from", """
<div class="row" style="gap:70px;align-items:flex-start">
 <div class="col" style="gap:4px">
   <svg id="dist" width="1000" height="600" viewBox="0 0 1000 600"></svg>
   <div class="small" data-in="1" style="margin-left:40px"><span class="pos">Orange</span> area right of the line → <b>TPR</b><br><span class="neg">Blue</span> area right of the line → <b>FPR</b></div>
 </div>
 <div class="col" style="gap:4px">
   <svg id="roc" width="640" height="600" viewBox="0 0 640 600"></svg>
   <div class="mono" style="font-size:31px;margin-left:110px" data-in="1" data-out="3">TPR <span id="rt" class="pos"></span> &nbsp; FPR <span id="rf" class="neg"></span></div>
   <div class="small" data-in="3" style="margin-left:110px">AUC <span class="yel mono" id="auc"></span> · 0.5 is guessing</div>
 </div>
</div>""", [
    Step("""So where does the ROC curve come from? A model gives every observation a score, like a predicted probability.
Negatives, in blue, tend to score low. Positives, in orange, tend to score high.
Pick a threshold, and everything to its right is predicted positive."""),
    Step("""The share of the orange curve to the right of the line is the true positive rate.
The share of the blue curve to the right is the false positive rate. Together, they make one point on the ROC plot."""),
    Step("""Now slide the threshold down. The model catches more positives, but it also flags more negatives,
so the point moves up and to the right. A very high threshold predicts nothing positive: the point zero, zero.
A very low one predicts everything positive: the point one, one. Every threshold in between traces out the curve.""",
         anim=dict(start=0.05, end=0.97)),
    Step("""The diagonal is what random guessing gets. The area under the curve, the AUC, runs from 0.5 for guessing
to 1 for a perfect model. It also equals the chance that a random positive scores higher than a random negative."""),
], script=s5_js)

# ---------------------------------------------------------------- 6 PM1 Q10
s6_js = C_JS + r"""
const k=Math.log(0.5)/Math.log(0.8);
const f=x=>1-(1-x)**k;
const RX=sc(0,1,110,600), RY=sc(0,1,540,50);
const pts={A:[0.2,0.5],B:[0.5,f(0.5)],C:[0.5,0.5],D:[1,1]};
const st={};
function init(){
  const r=document.getElementById('roc');
  st.band=S('rect',{x:RX(0),y:RY(1),width:RX(0.5)-RX(0),height:RY(0)-RY(1),fill:'rgba(255,216,74,.08)','data-in':2},r);
  axes(S('g',{},r),RX,RY,0,1,0,1,[0,0.25,0.5,0.75,1],[0,0.25,0.5,0.75,1],'FPR','TPR');
  S('line',{x1:RX(0.5),x2:RX(0.5),y1:RY(0),y2:RY(1),stroke:C.hl,'stroke-width':3,'stroke-dasharray':'9 7','data-in':2},r);
  S('text',{x:RX(0.5),y:RY(1)-14,'text-anchor':'middle',fill:C.hl,'font-size':23,'data-in':2},r,'FPR ≤ 0.5');
  S('line',{x1:RX(0),y1:RY(0),x2:RX(1),y2:RY(1),stroke:C.muted,'stroke-width':2.5,'stroke-dasharray':'8 8'},r);
  S('path',{d:P(range(0,1,200).map(x=>[RX(x),RY(f(x))])),fill:'none',stroke:C.text,'stroke-width':4.5},r);
  for(const n in pts){const [x,y]=pts[n];
    const g=S('g',n==='B'?{}:{'data-dim':'2'},r);
    S('circle',{cx:RX(x),cy:RY(y),r:n==='B'?13:11,fill:C.muted,stroke:'#0c1320','stroke-width':3,class:'pt'+n},g);
    const dx=n==='D'?-30:-24, dy=n==='C'?38:-16;
    S('text',{x:RX(x)+dx,y:RY(y)+dy,'text-anchor':'end',fill:C.text,'font-size':30,'font-weight':600},g,n);}
}
function onStep(k){const b=document.querySelector('.ptB');b.setAttribute('fill',k===2?C.hl:C.muted);}
"""
s6 = Scene("Exam: choose an ROC point", "Exam question: choose a point on the ROC curve", """
<div class="row" style="gap:70px;align-items:flex-start">
 <div class="col" style="width:900px;gap:24px">
   <div class="card"><div class="lab">Practice midterm 1 · Q10</div><div style="margin-top:10px">Minimize telling sick patients they're healthy, while wrongly telling healthy patients they're sick at most 50% of the time. Which point?</div></div>
   <div class="card" data-in="1"><div class="lab">Translate</div>
      <div style="margin-top:8px">Sick told healthy = <b>false negative</b> → max <b class="pos">TPR</b></div>
      <div>Healthy told sick ≤ 50% → <b class="neg">FPR</b> ≤ 0.5</div></div>
   <div class="card hl" data-in="2"><div class="lab">Answer</div><div style="margin-top:8px"><b class="yel">B</b>: FPR 0.5, TPR ≈ 0.88</div><div class="small muted">A gives up TPR · C is guessing · D breaks the limit</div></div>
 </div>
 <svg id="roc" width="720" height="720" viewBox="0 0 640 640"></svg>
</div>""", [
    Step("""Practice midterm one, question ten. A doctor wants to minimize telling sick patients they're healthy,
while wrongly telling healthy patients they're sick at most half the time. Which point should she choose?""", hold=0.8),
    Step("""First, translate the words into metrics. Telling a sick patient they're healthy is a false negative,
so minimizing it means maximizing TPR. Wrongly alarming healthy patients at most half the time means an FPR of at most 0.5."""),
    Step("""Shade the allowed region, then move right along the curve as far as the limit allows, since TPR never falls as FPR rises.
That's point B, with a TPR of about 0.88. A is allowed but gives up TPR. C sits on the diagonal, which is just guessing.
And D breaks the limit."""),
], script=s6_js)

# ---------------------------------------------------------------- 7 crossing curves
s7_js = C_JS + r"""
const fA=x=>1-(1-x)**4.5, fB=x=>0.62*(1-Math.exp(-x/0.05))+0.38*Math.pow(x,0.9);
const RX=sc(0,1,110,600), RY=sc(0,1,540,50);
function aucOf(f){let a=0;const n=2000;for(let i=1;i<=n;i++){const x0=(i-1)/n,x1=i/n;a+=(x1-x0)*(f(x0)+f(x1))/2;}return a;}
function init(){
  let cx=0.01;for(let x=0.01;x<1;x+=0.0005){if(fA(x)>=fB(x)){cx=x;break;}}
  const r=document.getElementById('roc');
  S('rect',{x:RX(0),y:RY(1),width:RX(cx)-RX(0),height:RY(0)-RY(1),fill:'rgba(255,216,74,.10)','data-in':1},r);
  axes(S('g',{},r),RX,RY,0,1,0,1,[0,0.25,0.5,0.75,1],[0,0.25,0.5,0.75,1],'FPR','TPR');
  S('line',{x1:RX(0),y1:RY(0),x2:RX(1),y2:RY(1),stroke:C.faint,'stroke-width':2,'stroke-dasharray':'8 8'},r);
  S('path',{d:P(range(0,1,300).map(x=>[RX(x),RY(fA(x))])),fill:'none',stroke:C.text,'stroke-width':4.5},r);
  S('path',{d:P(range(0,1,300).map(x=>[RX(x),RY(fB(x))])),fill:'none',stroke:C.hl,'stroke-width':4.5,'stroke-dasharray':'14 9'},r);
  document.getElementById('aA').textContent=aucOf(fA).toFixed(2);
  document.getElementById('aB').textContent=aucOf(fB).toFixed(2);
  document.getElementById('cx').textContent=(Math.round(cx*100)/100).toFixed(2);
}
"""
s7 = Scene("Curves can cross", "A higher AUC isn't better everywhere", """
<div class="row" style="gap:80px;align-items:center">
  <svg id="roc" width="720" height="720" viewBox="0 0 640 640"></svg>
  <div class="col" style="width:880px;gap:26px">
    <div class="card"><div class="lab">Two models</div>
      <div style="margin-top:10px"><svg width="70" height="16"><line x1="0" y1="8" x2="70" y2="8" stroke="#eef2f8" stroke-width="5"/></svg> &nbsp;Model A · AUC <span class="mono" id="aA"></span></div>
      <div><svg width="70" height="16"><line x1="0" y1="8" x2="70" y2="8" stroke="#ffd84a" stroke-width="5" stroke-dasharray="14 9"/></svg> &nbsp;Model B · AUC <span class="mono" id="aB"></span></div></div>
    <div class="card hl" data-in="1"><div>Below an FPR of about <span class="mono" id="cx"></span>, <b class="yel">model B</b> catches more positives.</div>
      <div class="small muted" style="margin-top:10px">Read both curves over the range the question asks about. PM2 Q15 tests exactly this.</div></div>
  </div>
</div>""", [
    Step("""One more trap. A higher AUC does not make a model better at every threshold, because ROC curves can cross.
Here, model A has the larger area."""),
    Step("""But if you need an FPR below about 0.25, model B catches more positives. Question fifteen on practice midterm two
tests exactly this. Read both curves over the range the question asks about, and pick the one that gets there with less FPR."""),
], script=s7_js)

# ---------------------------------------------------------------- 8 PM1 Q11 normal curves
s8_js = C_JS + r"""
const X=sc(0.5,8.5,90,1640), Y=sc(0,0.45,400,40);
const st={};
function area(m,a,b){const pts=[[X(a),Y(0)]];range(a,b,300).forEach(x=>pts.push([X(x),Y(npdf(x,m,1))]));pts.push([X(b),Y(0)]);return P(pts)+'Z';}
function init(){
  const s=document.getElementById('nc');
  S('path',{d:area(5.5,0.5,8.5),fill:'rgba(76,176,255,.09)'},s);
  S('path',{d:area(4,0.5,8.5),fill:'rgba(255,154,61,.09)'},s);
  S('path',{d:area(5.5,0.5,4.3),fill:'rgba(76,176,255,.55)','data-in':1},s);
  S('path',{d:area(4,0.5,4.3),fill:'rgba(255,154,61,.5)','data-in':2},s);
  const xs=range(0.5,8.5,500);
  S('path',{d:P(xs.map(x=>[X(x),Y(npdf(x,5.5,1))])),fill:'none',stroke:C.neg,'stroke-width':4},s);
  S('path',{d:P(xs.map(x=>[X(x),Y(npdf(x,4,1))])),fill:'none',stroke:C.pos,'stroke-width':4},s);
  S('line',{x1:X(0.5),x2:X(8.5),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);
  [1,2,3,4,5,6,7,8].forEach(v=>S('text',{x:X(v),y:Y(0)+36,'text-anchor':'middle',class:'tick'},s,String(v)));
  S('line',{x1:X(4.3),x2:X(4.3),y1:Y(0.45),y2:Y(0),stroke:C.hl,'stroke-width':4,'stroke-dasharray':'10 8'},s);
  S('text',{x:X(4.3),y:Y(0.45)-8,'text-anchor':'middle',fill:C.hl,'font-size':25},s,'x = 4.3');
  S('text',{x:X(4.3)-120,y:Y(0.45)-8,'text-anchor':'end',fill:C.hl,'font-size':25},s,'← predict positive');
  S('text',{x:X(3.15),y:Y(0.36),'text-anchor':'end',fill:C.pos,'font-size':26},s,'Class 1 · positive · mean 4');
  S('text',{x:X(6.35),y:Y(0.36),fill:C.neg,'font-size':26},s,'Class 2 · negative · mean 5.5');
}
"""
s8 = Scene("Exam: FPR as an area", "Exam question: which area is the FPR?", r"""
<svg id="nc" width="1720" height="450" viewBox="0 0 1720 450"></svg>
<div class="col" style="gap:10px;margin-top:4px">
  <div data-in="1"><b class="neg">FPR</b> = negative-class area left of 4.3 ÷ all negative-class area = <span class="tex">\Phi(-1.2)</span> ≈ <span class="yel mono">0.12</span></div>
  <div data-in="2"><b class="pos">TPR</b> = positive-class area left of 4.3 ÷ all positive-class area = <span class="tex">\Phi(0.3)</span> ≈ <span class="yel mono">0.62</span></div>
  <div class="card hl" data-in="3" style="margin-top:8px;font-size:31px"><span class="lab">PM1 · Q11</span> &nbsp; On the exam's lettered figure, FPR = <span class="mono">B / (B + D + E)</span>: answer <b class="yel">D</b>.
  <div class="small muted" style="margin-top:6px">Option A, <span class="mono">(C + D) / (A + B + C + D)</span>, is the false negative rate. The exam colors the curves differently, so go by the letters.</div></div>
</div>""", [
    Step("""Practice midterm one, question eleven, uses two normal curves. Class one, the positive class, is centered at 4.
Class two, the negative class, is centered at 5.5. The rule predicts positive when x is below 4.3,
so here the positive side is on the left."""),
    Step("""The false positive rate is the negative class's area on the predicted positive side, divided by its total area.
That's the blue area left of 4.3, which is the normal CDF at minus 1.2, about 0.12."""),
    Step("The true positive rate is the same idea for the positive class. The orange area left of 4.3 is about 0.62."),
    Step("""On the exam's lettered figure, that region is B, and the whole class two curve is B plus D plus E.
So the answer is D. The tempting option A is actually the false negative rate."""),
], script=s8_js)

# ---------------------------------------------------------------- 9 recap
s9 = Scene("Recap", "Recap", """
<ol class="recap">
  <li><div><b class="pos">TPR</b> = TP / (TP + FN) uses only the actual positives. <b class="neg">FPR</b> = FP / (FP + TN) uses only the actual negatives.</div></li>
  <li><div>The baseline predicts the <b>training</b> majority. On imbalanced data it can win on accuracy with TPR = 0.</div></li>
  <li><div>Lower the threshold and TPR and FPR both rise. Sweep every threshold and you get the ROC curve.</div></li>
  <li><div>AUC 0.5 is guessing, 1 is perfect. Curves can cross, so a higher AUC isn't better everywhere.</div></li>
  <li><div>Under an FPR limit, take the rightmost allowed point.</div></li>
</ol>
<div class="next">Next · Video 2: Decision analysis, from payoffs to a threshold</div>""", [
    Step("""To recap. TPR uses only the actual positives, and FPR uses only the actual negatives.
The baseline predicts the training majority, and on imbalanced data it can win on accuracy while catching nothing.
Lowering the threshold raises both rates, and sweeping it traces the ROC curve. An AUC of 0.5 is guessing, and curves can cross.
Under an FPR limit, take the rightmost allowed point. Next, we'll turn dollars into the threshold itself.""", hold=1.5),
])

VIDEO = Video(1, "v01-metrics", "Classification metrics and ROC curves", "Classification metrics",
              [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
