from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b'};\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"
RAND = "let __s=7;function rnd(){__s=(__s*1103515245+12345)%2147483648;return __s/2147483648;}function rnorm(){let u=0,v=0;while(u===0)u=rnd();v=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}\n"

# ---------------------------------------------------------------- 0 intro
s0_js = C_JS + RAND + r"""
function init(){const m=document.getElementById('motif');const X=sc(0,10,40,580),Y=sc(0,10,580,40);const g=S('g',{},m);
 [0,2.5,5,7.5,10].forEach(v=>{S('line',{x1:X(v),x2:X(v),y1:Y(0),y2:Y(10),stroke:'#1c2a40','stroke-width':2},g);S('line',{x1:X(0),x2:X(10),y1:Y(v),y2:Y(v),stroke:'#1c2a40','stroke-width':2},g);});
 for(let i=0;i<46;i++){const x=0.6+rnd()*8.8;const y=1.2+0.78*x+rnorm()*0.9;S('circle',{cx:X(x),cy:Y(y),r:9,fill:'rgba(76,176,255,.55)'},g);}
 S('line',{x1:X(0.3),y1:Y(1.2+0.78*0.3),x2:X(9.7),y2:Y(1.2+0.78*9.7),stroke:C.hl,'stroke-width':6},m);}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 3 of 8</div>
  <div class="t1">Linear regression:<br>reading R output</div>
  <div class="t2">The biggest topic on the practice midterms: 62 of 300 points</div>
  <div class="chips" style="max-width:1000px"><span>Predictions</span><span>p-values</span><span>R² vs OSR²</span><span>VIF</span><span>New variables</span><span>log(Y)</span></div>
</div>
<svg class="motif" id="motif" width="620" height="620" viewBox="0 0 620 620"></svg>""", [
    Step("""Linear regression is worth more points than any other topic on these practice midterms: 62 out of 300.
The good news is that almost every question is a reading exercise on R output. Here's how to read it, and the moves the exam keeps testing.""")],
    script=s0_js)

# ---------------------------------------------------------------- 1 anatomy of summary()
s1_js = r"""
function onStep(k){const t=document.getElementById('rt');t.classList.toggle('hl-est',k===1);t.classList.toggle('hl-p',k===2);
 document.getElementById('r2').classList.toggle('hlr',k===3);}
"""
s1 = Scene("Reading summary(lm)", "Reading the output of summary(lm)", r"""
<div class="row" style="gap:40px;align-items:center">
 <div class="console">
  <div class="faint">&gt; summary(mod1) &nbsp;&nbsp;<span class="muted">PM2 · predicting PRP, a CPU's published performance</span></div>
  <div style="margin:10px 0 14px">lm(PRP ~ MYCT + MMIN + MMAX + CACH + CHMIN + CHMAX)</div>
  <table id="rt" class="rt">
   <tr class="hd"><td></td><td class="est">Estimate</td><td>Std. Error</td><td>t value</td><td class="p">Pr(&gt;|t|)</td><td></td></tr>
   <tr><td>(Intercept)</td><td class="est">-28.27</td><td>8.888105</td><td>-3.18</td><td class="p">0.00181</td><td class="st">**</td></tr>
   <tr><td>MYCT</td><td class="est">0.02895</td><td>0.016653</td><td>1.74</td><td class="p">0.08437</td><td class="st">.</td></tr>
   <tr><td>MMIN</td><td class="est">0.01806</td><td>0.001742</td><td>10.37</td><td class="p">&lt; 2e-16</td><td class="st">***</td></tr>
   <tr><td>MMAX</td><td class="est">0.002705</td><td>0.000695</td><td>3.89</td><td class="p">0.00015</td><td class="st">***</td></tr>
   <tr><td>CACH</td><td class="est">0.6985</td><td>0.139216</td><td>5.02</td><td class="p">1.6e-06</td><td class="st">***</td></tr>
   <tr><td>CHMIN</td><td class="est">2.906</td><td>0.969768</td><td>3.00</td><td class="p">0.00323</td><td class="st">**</td></tr>
   <tr><td>CHMAX</td><td class="est">0.3732</td><td>0.276328</td><td>1.35</td><td class="p">0.17897</td><td class="st"></td></tr>
  </table>
  <div style="margin-top:14px" class="muted">Residual standard error: 48.67 on 138 degrees of freedom</div>
  <div id="r2">Multiple R-squared: 0.88, &nbsp;Adjusted R-squared: 0.8748</div>
 </div>
 <div class="col" style="width:540px;gap:20px">
  <div class="card" data-in="1" data-hl="1"><div class="lab">Estimate</div><div class="small" style="margin-top:6px">Change in predicted Y when X rises by 1, others held fixed. Use it to predict.</div></div>
  <div class="card" data-in="2" data-hl="2"><div class="lab">Pr(&gt;|t|)</div><div class="small" style="margin-top:6px">p-value for H₀: β = 0. Below 0.05 means significant.</div></div>
  <div class="card" data-in="3" data-hl="3"><div class="lab">R-squared</div><div class="small" style="margin-top:6px">Training fit only. Adjusted R² charges for each extra variable.</div></div>
 </div>
</div>""", [
    Step("""Here's the output from practice midterm two: a regression predicting a CPU's published performance, PRP, from six hardware specs.
Three parts of it answer nearly every question."""),
    Step("""The Estimate column is the coefficient: how much the prediction changes when that feature rises by one unit,
holding the others fixed. That's what you use to make predictions."""),
    Step("""The last column is the p-value for the null hypothesis that the coefficient is zero. Below 0.05 means significant.
The stars are just a shortcut for the same thing."""),
    Step("""And R squared at the bottom is the fit on the training data only. Adjusted R squared adds a penalty for each extra variable,
so use it to compare models of different sizes."""),
], script=s1_js, css=""".console{background:#0a111c;border:2px solid #223047;border-radius:18px;padding:26px 30px;font:400 25px/1.45 'Plex Mono',monospace;width:1140px;box-sizing:border-box}
.rt{border-collapse:collapse}.rt td{padding:2px 0 2px 34px;text-align:right}.rt td:first-child{text-align:left;padding-left:0}.rt td.st{padding-left:12px}
.rt tr.hd td{color:var(--muted)}.rt td.st{text-align:left;color:var(--muted)}
.rt.hl-est td.est,.rt.hl-p td.p{background:rgba(255,216,74,.14);color:var(--hl)}
#r2.hlr{background:rgba(255,216,74,.14);color:var(--hl);border-radius:6px}""")

# ---------------------------------------------------------------- 2 predictions
s2 = Scene("Making a prediction", "Predictions: plug in, then add up", r"""
<div class="col" style="gap:22px">
 <div class="card"><div class="lab">PM2 · new CPU</div>
  <div class="mono" style="margin-top:8px;font-size:32px">MYCT 75 · MMIN 2,500 · MMAX 10,000 · CACH 30 · CHMIN 4 · CHMAX 8</div></div>
 <div class="card" data-in="1"><span class="tex" data-d="1">\hat y=-28.27+0.02895(75)+0.01806(2500)+0.002705(10000)+0.6985(30)+2.906(4)+0.3732(8)</span>
  <div class="row" style="justify-content:space-between;align-items:baseline;margin-top:8px"><div class="small muted">Write the expression first. The rubric gives points for the right coefficients and values.</div><div class="mono yel big">= 81.67</div></div></div>
 <div class="card" data-in="2"><div class="lab">PM3 · golf winnings, $ millions</div>
  <span class="tex" data-d="1">\hat y=114.161-1.7459(70.50)+2.1927(1.76)+0.0264(300)-0.003636(60)\approx 2.635</span>
  <div class="small" style="margin-top:8px"><b class="yel">Units trap:</b> DrivingAccuracy is a percentage, and head() shows 57.7, so plug in 60, not 0.6.</div></div>
</div>""", [
    Step("""Predictions are plug and chug. On practice midterm two, a new CPU has a cycle time of 75, minimum memory of 2,500,
maximum memory of 10,000, cache of 30, and between 4 and 8 channels."""),
    Step("""Start with the intercept, then add each coefficient times its value. Write the whole expression before you compute:
the rubric gives points for the right coefficients and the right values, even if the arithmetic slips. The answer is about 81.67."""),
    Step("""Same move on midterm three's golf model gives about 2.64 million dollars. One trap: driving accuracy is a percentage,
and the data preview shows values like 57.7, so you plug in 60, not 0.6."""),
], css=KX + ".card .katex{font-size:.93em}")

# ---------------------------------------------------------------- 3 significance
s3 = Scene("Is a coefficient significant?", "Is a coefficient significant?", r"""
<div class="card hl" style="font-size:36px"><div class="lab" style="margin-bottom:10px">Answer template</div>
 <b>Yes / No</b>: the p-value is <span class="mono yel">___</span>, which is below / above 0.05,<br>so we can / cannot reject H₀: the coefficient is 0.</div>
<table class="t" data-in="1" style="margin-top:30px;width:100%;font-size:34px">
 <tr><th>Variable</th><th>Model</th><th class="num">p-value</th><th>Verdict</th></tr>
 <tr><td>AverageScore</td><td>PM3 golf</td><td class="num">2.46e−15</td><td><span class="verdict t">SIGNIFICANT</span></td></tr>
 <tr><td>AveragePutts</td><td>PM3 golf</td><td class="num">0.617</td><td><span class="verdict f">NOT SIGNIFICANT</span></td></tr>
 <tr><td>CHMAX</td><td>PM2 CPU</td><td class="num">0.179</td><td><span class="verdict f">NOT SIGNIFICANT</span></td></tr>
</table>""", [
    Step("""Significance questions want a verdict plus evidence. Use this template. Yes or no: the p-value is this number,
which is below or above 0.05, so we can or cannot reject the null hypothesis that the coefficient is zero."""),
    Step("""Average score on the golf model has a p-value of 2.46 times 10 to the minus 15: significant. Average putts has 0.617,
and CHMAX on the CPU model has 0.179, so neither is significant. Quote the number. That's where the points are."""),
])

# ---------------------------------------------------------------- 4 R2 vs OSR2
s4_js = C_JS + r"""
function init(){const s=document.getElementById('cx');const X=sc(1,10,90,620),Y=sc(0,1,400,40);
 axes(S('g',{},s),X,Y,1,10,0,1,[1,4,7,10],[0,0.5,1],'number of variables',null,v=>String(v));
 const tr=x=>0.55+0.4*(1-Math.exp(-(x-1)/2.5)), te=x=>0.55+0.3*(1-Math.exp(-(x-1)/1.6))-0.025*(x-1)**1.3;
 S('path',{d:P(range(1,10,100).map(x=>[X(x),Y(tr(x))])),fill:'none',stroke:C.text,'stroke-width':5},s);
 S('path',{d:P(range(1,10,100).map(x=>[X(x),Y(te(x))])),fill:'none',stroke:C.hl,'stroke-width':5,'stroke-dasharray':'12 8'},s);
 S('text',{x:X(10),y:Y(tr(10))-14,'text-anchor':'end',fill:C.text,'font-size':25},s,'training R²');
 S('text',{x:X(10),y:Y(te(10))+36,'text-anchor':'end',fill:C.hl,'font-size':25},s,'test OSR²');}
"""
s4 = Scene("R² versus OSR²", "Training R² versus test OSR²", r"""
<div class="row" style="gap:50px;align-items:center">
 <div class="col" style="flex:1;gap:20px">
  <div class="card"><span class="tex" data-d="1">R^2=1-\dfrac{SSE_{train}}{SST_{train}}\qquad OSR^2=1-\dfrac{\sum_{test}(y_i-\hat y_i)^2}{\sum_{test}(y_i-\bar y_{train})^2}</span></div>
  <div class="card" data-in="1"><div class="small">Add a variable: training R² <b>never falls</b>. Remove one: it <b>never rises</b>, but it can stay the same.</div>
   <div class="small muted" style="margin-top:6px">PM3 Q2: "removing a variable always decreases R²" is <span class="bad">false</span>.</div></div>
  <div class="card" data-in="2"><div class="small">Test OSR² can go <b>either way</b>, and can be <b>negative</b> (worse than the training mean).</div>
   <div class="small muted" style="margin-top:6px">PM1 Q3 and PM3 Q3: <span class="bad">false</span>.</div></div>
  <div class="card" data-in="3"><div class="small">Two points, different x, no noise: least squares fits exactly, so the estimates equal the true β's.</div>
   <div class="small muted" style="margin-top:6px">PM3 Q4: <span class="good">true</span>.</div></div>
 </div>
 <div data-in="2"><svg id="cx" width="660" height="480" viewBox="0 0 660 480"></svg><div class="small muted" style="margin-left:90px">illustration</div></div>
</div>""", [
    Step("""Next, R squared versus OSR squared. R squared measures fit on the training data. OSR squared measures it on the test set,
compared against just predicting the training mean."""),
    Step("""Adding a variable can never lower training R squared, and removing one can never raise it. But removal can leave R squared unchanged,
so the claim on practice midterm three that removing a variable always decreases it is false."""),
    Step("""Out of sample, anything goes. Test OSR squared can rise or fall when you add or remove a variable, so a higher training R squared
guarantees nothing on the test set. OSR squared can even be negative, which means the model predicts worse than the training mean."""),
    Step("""One more true or false: with two points at different x values and no noise, least squares fits them exactly,
so the estimates equal the true coefficients. True."""),
], script=s4_js, css=KX + ".card .katex{font-size:.9em}")

# ---------------------------------------------------------------- 5 VIF
s5 = Scene("Multicollinearity and VIF", "Multicollinearity and the VIF", r"""
<div class="row" style="gap:40px;align-items:stretch">
 <div class="card" style="flex:1"><span class="tex" data-d="1">VIF_j=\dfrac{1}{1-R_j^2}</span>
  <div class="small" style="margin-top:10px">R<sub>j</sub>² comes from regressing X<sub>j</sub> on all the other X's. <b class="yel">Above 5 is high.</b></div>
  <div class="small muted" style="margin-top:8px">High VIF inflates standard errors and makes signs unstable.</div></div>
 <div class="card" data-in="1" style="flex:1.25"><div class="lab">PM2 · vif(mod1)</div>
  <div class="mono" style="font-size:26px;margin-top:10px;white-space:pre"> MYCT   MMIN   MMAX   CACH  CHMIN  CHMAX
1.26   <span class="yel">3.14</span>   3.14   1.78   2.29   1.59</div>
  <div class="small" style="margin-top:14px"><b>No</b> high multicollinearity: every VIF is below 5, and the largest is 3.14.</div>
  <div class="small muted" style="margin-top:6px">Even though MMIN and MMAX correlate at 0.80. The VIF is the test.</div></div>
</div>
<div class="card" data-in="2" style="margin-top:26px"><div class="lab">PM1 · Q6 · true</div>
 <div class="small" style="margin-top:8px">Large VIFs with only modest pairwise correlations? Yes. If X₉ ≈ X₁ + … + X₈, each pairwise correlation is about 0.35, but X₉'s VIF is about 800.</div></div>
""", [
    Step("""Multicollinearity means one feature is nearly a combination of the others. The VIF measures it: regress feature j on all the other
features, take that R squared, and compute one over one minus it. Above 5 is high. It inflates standard errors and makes coefficient signs unstable."""),
    Step("""On practice midterm two, the largest VIF is 3.14, so the answer is no high multicollinearity, even though MMIN and MMAX
have a pairwise correlation near 0.8. The VIF is the test the rubric wants."""),
    Step("""And the true or false from midterm one: can variables have large VIFs but only modest pairwise correlations? Yes.
If X nine is roughly the sum of eight other features, each pairwise correlation is only about 0.35, but X nine's VIF is around 800."""),
], css=KX)

# ---------------------------------------------------------------- 6 new variables
s6 = Scene("Can a new variable help?", "Can a new variable improve the model?", r"""
<div class="row" style="gap:40px;align-items:stretch">
 <div class="card" style="flex:1"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">Linear combination</div><span class="verdict f">NO</span></div>
  <div class="mono" style="font-size:30px;margin-top:16px;line-height:1.7">CHAVG = (CHMIN + CHMAX) / 2<br>PuttsPerRound = 18 × AveragePutts</div>
  <div class="small" style="margin-top:14px">The model could already build it. R reports <span class="mono">NA</span>: perfect collinearity.</div>
  <div class="small muted" style="margin-top:6px">PM2 short answer 1d · PM3 short answer 1e</div></div>
 <div class="card" data-in="1" style="flex:1"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">Nonlinear transform</div><span class="verdict t">YES, CAN HELP</span></div>
  <div class="mono" style="font-size:30px;margin-top:16px;line-height:1.7">CACH²<br>log(X) &nbsp;·&nbsp; X₁ × X₂</div>
  <div class="small" style="margin-top:14px">Gives the model a shape it couldn't make before.</div>
  <div class="small muted" style="margin-top:6px">PM2 short answer 1e</div></div>
</div>""", [
    Step("""A favorite short answer: can adding this new variable improve the model? If it's a linear combination of existing variables, no.
CHAVG, the average of CHMIN and CHMAX, and putts per round, which is 18 times putts per hole, add nothing the model couldn't already build.
R would even report an NA coefficient, because of perfect collinearity."""),
    Step("""If it's a nonlinear transformation, yes, it can help. Cache squared, a log, or a product of two features gives the model
a shape it couldn't make before."""),
])

# ---------------------------------------------------------------- 7 log(Y)
s7_js = C_JS + RAND + r"""
function init(){const pts=[];for(let i=0;i<105;i++){const s=69.6+rnd()*2.8;const lw=0.55-1.45*(s-70.8)+rnorm()*0.38;pts.push([s,lw]);}
 const A=document.getElementById('pa'),B=document.getElementById('pb');
 const X=sc(69.5,72.5,90,700),YA=sc(0,10,420,30),YB=sc(-2,2.5,420,30);
 axes(S('g',{},A),X,YA,69.5,72.5,0,10,[70,71,72],[0,2.5,5,7.5,10],'AverageScore','Winnings ($M)',v=>String(v));
 axes(S('g',{},B),X,YB,69.5,72.5,-2,2.5,[70,71,72],[-2,-1,0,1,2],'AverageScore','log(Winnings)',v=>String(v));
 pts.forEach(([s,lw])=>{const w=Math.exp(lw);if(w<=10)S('circle',{cx:X(s),cy:YA(w),r:7,fill:'rgba(76,176,255,.6)'},A);if(lw>=-2&&lw<=2.5)S('circle',{cx:X(s),cy:YB(lw),r:7,fill:'rgba(76,176,255,.6)'},B);});
 S('line',{x1:X(69.6),y1:YB(0.55-1.45*(69.6-70.8)),x2:X(72.4),y2:YB(0.55-1.45*(72.4-70.8)),stroke:C.hl,'stroke-width':5,'data-in':1},B);}
"""
s7 = Scene("Transforming Y", "Curved and fanning out? Try log(Y)", r"""
<div class="row" style="gap:20px;align-items:flex-start">
 <div class="col" style="gap:0"><svg id="pa" width="740" height="510" viewBox="0 0 740 510"></svg><div class="small muted" style="margin-left:90px">Curves up, spreads out at low scores</div></div>
 <div class="col" style="gap:0"><svg id="pb" width="740" height="510" viewBox="0 0 740 510"></svg><div class="small" style="margin-left:90px">A straight band with even spread</div></div>
</div>
<div class="card hl" data-in="1" style="margin-top:20px"><b>Choose log(Winnings)</b> (PM3 short answer 1f). Predict on the log scale, then exponentiate to get dollars back.
 <span class="small muted">&nbsp;Simulated data with the shape of PM3 Figure 3.</span></div>""", [
    Step("""Midterm three also shows two scatter plots: winnings against average score, and the log of winnings against average score.
Raw winnings curve upward and fan out at low scores. The log version is a straight band with even spread."""),
    Step("""So choose log of winnings: linear regression fits straight lines, and the log makes the relationship linear.
Just remember to predict on the log scale, then exponentiate to get dollars back."""),
], script=s7_js)

# ---------------------------------------------------------------- 8 interpretation trap
s8 = Scene("Coefficient signs", "A coefficient isn't a correlation", r"""
<div class="row" style="gap:40px;align-items:stretch">
 <div class="card" style="flex:1"><div class="lab">Raw correlation with Winnings</div><div class="mono big" style="margin-top:14px">AveragePutts: <span class="neg">−0.28</span></div>
  <div class="small muted" style="margin-top:10px">Players who putt more tend to win less.</div></div>
 <div class="card" style="flex:1"><div class="lab">Coefficient in the full model</div><div class="mono big" style="margin-top:14px">AveragePutts: <span class="pos">+2.19</span></div>
  <div class="small muted" style="margin-top:10px">Holding AverageScore and the rest fixed. p = 0.617, not significant.</div></div>
</div>
<div class="small" style="margin-top:30px">A coefficient compares observations with every other variable held fixed, so its sign can differ from the raw correlation.</div>""", [
    Step("""Last, a reading trap. A coefficient compares players with every other variable held fixed, so its sign can differ from the raw correlation.
In the golf data, average putts correlates negatively with winnings, minus 0.28, but its coefficient is positive, 2.19, and not significant.
Holding average score fixed changes the comparison."""),
])

# ---------------------------------------------------------------- 9 recap
s9 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:35px;gap:22px">
  <li><div>ŷ = intercept + Σ coefficient × value. Write the expression first, and check units.</div></li>
  <li><div>Significant when p &lt; 0.05. Quote the p-value in your answer.</div></li>
  <li><div>Training R² can't fall when you add a variable. Test OSR² can do anything, even go negative.</div></li>
  <li><div>VIF = 1 / (1 − R<sub>j</sub>²). Above 5 is high. Use the VIF, not pairwise correlations.</div></li>
  <li><div>Linear combinations never help. Nonlinear transforms can.</div></li>
  <li><div>Curved and fanning out? Try log(Y), then exponentiate predictions.</div></li>
</ol>
<div class="next">Next · Video 4: Logistic regression and LDA</div>""", [
    Step("""To recap. A prediction is the intercept plus each coefficient times its value: write the expression first, and check units.
A coefficient is significant when its p-value is below 0.05, and you should quote that p-value. Training R squared can't fall when you add a variable,
but test OSR squared can do anything. Judge multicollinearity with the VIF, where above 5 is high. Linear combinations of features never help,
but nonlinear transforms can. And if the relationship curves and fans out, try the log. Next: logistic regression and L D A.""", hold=1.5),
])

VIDEO = Video(3, "v03-linreg", "Linear regression - reading R output", "Linear regression",
              [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
