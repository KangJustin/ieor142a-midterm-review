from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b',panel:'#141e2e',line:'#2a3950'};\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"

s0_js = C_JS + r"""
function init(){const m=document.getElementById('motif');for(let r=0;r<5;r++)for(let c=0;c<5;c++){
 S('rect',{x:40+c*108,y:60+r*96,width:96,height:76,rx:12,fill:r===c?'rgba(255,216,74,.85)':'rgba(76,176,255,.28)',stroke:r===c?C.hl:'#2a3950','stroke-width':3},m);}}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 6 of 8</div>
  <div class="t1">Cross-validation<br>and the bootstrap</div>
  <div class="t2">Choosing settings, and measuring how sure you are</div>
  <div class="chips" style="max-width:1000px"><span>k-fold CV</span><span>LOOCV cost</span><span>Why a test set</span><span>Bootstrap samples</span><span>Confidence intervals</span><span>Bias and B</span></div>
</div>
<svg class="motif" id="motif" width="620" height="560" viewBox="0 0 620 560"></svg>""", [
    Step("""Cross-validation picks a model's settings using only the training data. The bootstrap measures how uncertain a number is
by recomputing it on resampled data. Each shows up in a handful of true or false questions, plus one tricky table.""")], script=s0_js)

# ---------------------------------------------------------------- 1 k-fold
s1_js = C_JS + r"""
function init(){const s=document.getElementById('kf');const w=176,h=64,gx=14,gy=16,x0=200,y0=70;
 S('text',{x:x0,y:40,fill:C.muted,'font-size':23},s,'training set, split into 5 folds');
 for(let c=0;c<5;c++){S('rect',{x:x0+c*(w+gx),y:y0,width:w,height:h,rx:10,fill:'rgba(76,176,255,.28)',stroke:C.line,'stroke-width':2},s);
  S('text',{x:x0+c*(w+gx)+w/2,y:y0+42,'text-anchor':'middle',fill:C.text,'font-size':25},s,'fold '+(c+1));}
 for(let r=0;r<5;r++){const y=y0+110+r*(h+gy);const g=S('g',{'data-in':1},s);
  S('text',{x:x0-24,y:y+42,'text-anchor':'end',fill:C.muted,'font-size':24},g,'round '+(r+1));
  for(let c=0;c<5;c++){const v=(r===c);S('rect',{x:x0+c*(w+gx),y,width:w,height:h,rx:10,fill:v?'rgba(255,216,74,.8)':'rgba(76,176,255,.22)',stroke:v?C.hl:C.line,'stroke-width':2},g);
   S('text',{x:x0+c*(w+gx)+w/2,y:y+42,'text-anchor':'middle',fill:v?'#0c1320':C.muted,'font-size':23,'font-weight':v?700:400},g,v?'score':'train');}
  S('text',{x:x0+5*(w+gx)+10,y:y+42,fill:C.hl,'font-size':25,'data-in':2},s,'score '+(r+1));}
}
"""
s1 = Scene("k-fold cross-validation", "k-fold cross-validation", r"""
<div class="row" style="gap:30px;align-items:center">
 <svg id="kf" width="1340" height="620" viewBox="0 0 1340 620"></svg>
 <div class="card hl" data-in="2" style="width:350px"><div class="lab">Then</div><div class="small" style="margin-top:8px">Average the k scores. Repeat for every candidate setting (every cp, say) and keep the best.</div></div>
</div>""", [
    Step("In k-fold cross-validation, you split the training set into k folds. Here, k is 5."),
    Step("""For each fold, train on the other k minus 1 folds, and score on the one you held out.
Every observation is used for validation exactly once."""),
    Step("""Average the k scores. Repeat that for every candidate setting, like every value of cp, and keep the best one."""),
], script=s1_js)

# ---------------------------------------------------------------- 2 cost and k=1
s2 = Scene("Cost, LOOCV, and k = 1", "What k costs, and the k = 1 trap", r"""
<div class="card"><div class="lab">Cost = k model fits per setting · LOOCV is k = n</div>
 <div class="row" style="gap:40px;align-items:baseline;margin-top:12px"><div class="mono" style="font-size:36px">n = 1,000: &nbsp;10-fold = 10 fits &nbsp;·&nbsp; LOOCV = 1,000 fits</div></div>
 <div class="small" style="margin-top:10px">About <b class="yel">100× cheaper</b>. <span class="muted">PM2 Q7:</span> <span class="good">true</span></div></div>
<div class="card" data-in="1" style="margin-top:26px"><div class="lab">PM3 · Q14 · which statements are true?</div>
 <div style="margin-top:12px;line-height:1.7">
  <div>1. Bigger k means more computation <span class="verdict t">TRUE</span></div>
  <div>2. k = n is leave-one-out CV <span class="verdict t">TRUE</span></div>
  <div>3. k = 1 is the validation-set method <span class="verdict f">FALSE</span> <span class="small muted">one fold leaves nothing to train on</span></div></div>
 <div class="mono yel" style="margin-top:10px">Answer A: only 1 and 2</div></div>""", [
    Step("""The cost is k model fits per setting, and leave one out cross-validation is just k equals n. With a thousand training points,
ten-fold needs 10 fits and leave one out needs 1,000, so ten-fold is about a hundred times cheaper. That's true on practice midterm two."""),
    Step("""Practice midterm three lists three claims. Bigger k means more computation: true. k equals n is leave one out: true.
k equals 1 is the validation set method: false. With one fold, there's nothing left to train on.
The validation set method is a single train and validate split. So the answer is only the first two."""),
], css=".verdict{font-size:19px;padding:3px 12px;margin-left:12px}")

# ---------------------------------------------------------------- 3 test set still matters
s3 = Scene("CV doesn't replace a test set", "Cross-validation doesn't replace a test set", r"""
<div class="card"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">PM2 · Q5</div><span class="verdict f">FALSE</span></div>
 <div style="margin-top:10px">"If we used k-fold CV to select the final model, there's no need for a test set, since the model can't overfit."</div></div>
<div class="row" style="gap:26px;margin-top:26px" data-in="1">
 <div class="card" style="flex:1"><div class="lab">Training set</div><div class="small" style="margin-top:8px">CV picks the best of many settings. Picking the best can overfit the CV scores themselves.</div></div>
 <div class="card hl" style="flex:1"><div class="lab">Test set, held out</div><div class="small" style="margin-top:8px">Used once, at the end, for the honest estimate of performance.</div></div>
</div>""", [
    Step("""A classic false statement: if you used cross-validation to choose the final model, you don't need a test set,
because the model can't overfit."""),
    Step("""Choosing the best of many settings can overfit the cross-validation scores themselves. So keep a test set,
and use it once, at the end, for the final, honest estimate."""),
])

# ---------------------------------------------------------------- 4 bootstrap samples
s4_js = C_JS + r"""
const draws=[[3,7,7,1,5,2,7,8],[1,1,4,6,6,2,8,3],[5,2,2,4,8,8,6,1]];
function row(s,y,vals,label,step){const g=S('g',step===undefined?{}:{'data-in':step},s);
 S('text',{x:250,y:y+10,'text-anchor':'end',fill:C.muted,'font-size':24},g,label);
 vals.forEach((v,i)=>{S('circle',{cx:310+i*92,cy:y,r:32,fill:'rgba(76,176,255,.25)',stroke:C.neg,'stroke-width':2.5},g);
  S('text',{x:310+i*92,y:y+10,'text-anchor':'middle',fill:C.text,'font-size':28},g,String(v));});
 if(step!==undefined){const miss=[1,2,3,4,5,6,7,8].filter(v=>!vals.includes(v));S('text',{x:310+8*92,y:y+10,fill:C.bad,'font-size':24},g,'missing: '+miss.join(', '));}}
function init(){const s=document.getElementById('bs');row(s,60,[1,2,3,4,5,6,7,8],'original');
 S('line',{x1:270,x2:1300,y1:115,y2:115,stroke:C.line,'stroke-width':2,'data-in':1},s);
 draws.forEach((d,i)=>row(s,170+i*95,d,'sample '+(i+1),1));}
"""
s4 = Scene("The bootstrap", "The bootstrap: resample with replacement", r"""
<svg id="bs" width="1720" height="460" viewBox="0 0 1720 460"></svg>
<div class="card" data-in="2" style="margin-top:6px"><div class="small">Each sample draws n rows from n, <b>with replacement</b>. On average about <b class="yel">37%</b> of rows are left out:
 <span class="tex">(1-1/n)^n\to e^{-1}\approx 0.37</span></div></div>""", [
    Step("The bootstrap starts from the data you have. One bootstrap sample draws n rows from your n rows, with replacement."),
    Step("So some rows show up twice or more, and others don't show up at all."),
    Step("On average, about 37 percent of the rows are left out of each bootstrap sample."),
], script=s4_js)

# ---------------------------------------------------------------- 5 CI for a trained model
s5 = Scene("Bootstrapping a test metric", "A confidence interval for a trained model's metric", r"""
<div class="row" style="gap:0;align-items:center">
 <div class="card fb"><div class="lab">1 · Train once</div><div class="small" style="margin-top:6px">on the training set</div></div><div class="arr">→</div>
 <div class="card fb"><div class="lab">2 · Resample</div><div class="small" style="margin-top:6px">the <b>test set</b>, B times</div></div><div class="arr">→</div>
 <div class="card fb"><div class="lab">3 · Recompute</div><div class="small" style="margin-top:6px">the metric on each. Never retrain.</div></div>
</div>
<div class="row" style="gap:24px;margin-top:26px" data-in="1">
 <div class="card" style="flex:1"><div class="lab">PM2 · Q14</div><div class="small" style="margin-top:6px">Train on the training set, bootstrap the test set: <b class="yel">C</b></div></div>
 <div class="card" style="flex:1"><div class="lab">PM3 · Q7</div><div class="small" style="margin-top:6px">B = 10,000 means 10,000 OSR² calculations: <span class="good">true</span></div></div>
</div>
<div class="card" data-in="2" style="margin-top:24px"><span class="tex" data-d="1">\widehat{SE}=\text{SD}(\hat\theta^*_1,\dots,\hat\theta^*_B)\qquad \widehat{\text{bias}}=\overline{\hat\theta^*}-\hat\theta\qquad 95\%\text{ CI}=[q_{2.5},\,q_{97.5}]</span></div>""", [
    Step("""To put a confidence interval on a trained model's test metric, train the model once on the training set. Then resample the test set
B times, and recompute the metric on each resample. The model is never retrained."""),
    Step("""That's answer C on practice midterm two, question fourteen. And on midterm three: with B equal to 10,000,
the procedure computes the metric 10,000 times. True."""),
    Step("""From the B values you get three things. The standard error is their standard deviation. The bias estimate is their average
minus the original value. And a 95 percent interval runs from the 2.5th to the 97.5th percentile."""),
], css=KX + ".fb{width:500px;min-height:130px}.arr{font-size:46px;color:var(--faint);padding:0 14px}")

# ---------------------------------------------------------------- 6 bias across B
s6 = Scene("Reading bias across B", "Is the bias real, or just noise?", r"""
<div class="lab" style="margin-bottom:12px">PM2 · Q16 · bootstrap bias estimates</div>
<table class="t" style="width:100%;font-size:34px">
 <tr><th>Estimate</th><th class="num">B = 10,000</th><th class="num">B = 1,000,000</th><th>Verdict</th></tr>
 <tr data-hl="1"><td>OSR²</td><td class="num">0.0300</td><td class="num">0.0297</td><td data-in="1">stable → <b class="bad">biased</b></td></tr>
 <tr data-hl="1"><td>MAE</td><td class="num">0.223</td><td class="num">0.00927</td><td data-in="1">collapsed → <b class="good">unbiased</b></td></tr>
</table>
<div class="card" style="margin-top:26px"><div class="small">Bootstrap noise shrinks like <span class="mono yel">1/√B</span>: 100× more samples → about 10× less noise.</div></div>
<div class="card hl" data-in="2" style="margin-top:20px"><div class="small"><b>Answer D.</b> Matches theory: MAE is a plain average (unbiased); OSR² is a ratio (generally biased).</div></div>""", [
    Step("""Practice midterm two's question sixteen gives bias estimates for OSR squared and mean absolute error, with B of 10,000,
and then a million. The key fact: random noise in a bootstrap estimate shrinks like one over the square root of B.
A hundred times more samples means about ten times less noise."""),
    Step("""OSR squared's bias barely moves, from 0.0300 to 0.0297. It's stable, so the bias is real. MAE's bias collapses from 0.223 to 0.009,
so it was mostly noise."""),
    Step("""So the answer is D: MAE is likely unbiased, and OSR squared is likely biased. That matches theory: MAE is a plain average,
which is unbiased, while OSR squared is a ratio, which generally isn't."""),
])

# ---------------------------------------------------------------- 7 recap
s7 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:34px;gap:20px">
  <li><div>k-fold: train on k − 1 folds, score the held-out fold, average. Cost = k fits per setting.</div></li>
  <li><div>LOOCV is k = n. k = 1 is not the validation-set method.</div></li>
  <li><div>CV doesn't make overfitting impossible. Keep a test set.</div></li>
  <li><div>Bootstrap: n draws with replacement. About 37% of rows left out.</div></li>
  <li><div>CI for a trained model: resample the test set, never retrain. B resamples = B computations.</div></li>
  <li><div>Bias that holds steady as B grows is real. Bias that shrinks like 1/√B was noise.</div></li>
</ol>
<div class="next">Next · Video 7: Bagging, random forests and boosting</div>""", [
    Step("""To recap. In k-fold cross-validation, you train on k minus 1 folds and score the held-out fold, k times per setting.
Leave one out is k equals n, and k equals 1 is not the validation set method. Cross-validation doesn't make overfitting impossible,
so keep a test set. A bootstrap sample draws n rows with replacement. To get a confidence interval for a trained model,
resample the test set and never retrain. And a bias that holds steady as B grows is real. Next: ensembles.""", hold=1.5),
])

VIDEO = Video(6, "v06-cv-boot", "Cross-validation and the bootstrap", "CV and bootstrap",
              [s0, s1, s2, s3, s4, s5, s6, s7])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
