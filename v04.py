from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b'};\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"
CONSOLE = """.console{background:#0a111c;border:2px solid #223047;border-radius:18px;padding:26px 30px;font:400 26px/1.5 'Plex Mono',monospace;box-sizing:border-box}
.rt{border-collapse:collapse}.rt td{padding:2px 0 2px 34px;text-align:right}.rt td:first-child{text-align:left;padding-left:0}.rt td.st{padding-left:12px;text-align:left;color:var(--muted)}
.rt tr.hd td{color:var(--muted)}"""

# ---------------------------------------------------------------- 0 intro
s0_js = C_JS + r"""
function init(){const m=document.getElementById('motif');const X=sc(-6,6,40,580),Y=sc(-0.08,1.08,580,40);const g=S('g',{},m);
 [0,0.5,1].forEach(v=>S('line',{x1:X(-6),x2:X(6),y1:Y(v),y2:Y(v),stroke:'#1c2a40','stroke-width':2},g));
 [-4,-2.5,-1.5,-3,0.5,-0.5].forEach((z,i)=>S('circle',{cx:X(z),cy:Y(0),r:10,fill:'rgba(76,176,255,.6)'},g));
 [4,2.5,1.5,3,-0.5,0.8].forEach((z,i)=>S('circle',{cx:X(z),cy:Y(1),r:10,fill:'rgba(255,154,61,.7)'},g));
 S('path',{d:P(range(-6,6,200).map(z=>[X(z),Y(1/(1+Math.exp(-z)))])),fill:'none',stroke:C.hl,'stroke-width':6},g);}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 4 of 8</div>
  <div class="t1">Logistic regression<br>and LDA</div>
  <div class="t2">Two ways to get the probability of a class</div>
  <div class="chips" style="max-width:1000px"><span>The model</span><span>Predictions</span><span>Odds</span><span>Dummy coding</span><span>Red flags</span><span>LDA and Bayes' rule</span></div>
</div>
<svg class="motif" id="motif" width="620" height="620" viewBox="0 0 620 620"></svg>""", [
    Step("""Logistic regression and LDA both turn features into the probability of a class. Logistic regression models that probability directly.
LDA models how the features look within each class, then flips it around with Bayes' rule. Let's do both, using the YourCabs model from practice midterm one.""")],
    script=s0_js)

# ---------------------------------------------------------------- 1 the model
s1_js = C_JS + r"""
function init(){const s=document.getElementById('sg');const X=sc(-6,6,90,640),Y=sc(0,1,420,40);
 axes(S('g',{},s),X,Y,-6,6,0,1,[-6,-3,0,3,6],[0,0.5,1],'z = β₀ + β₁X₁ + … + βₚXₚ','P(Y = 1 | X)',v=>String(v));
 S('line',{x1:X(0),x2:X(0),y1:Y(0),y2:Y(0.5),stroke:C.faint,'stroke-width':2.5,'stroke-dasharray':'7 7'},s);
 S('line',{x1:X(-6),x2:X(0),y1:Y(0.5),y2:Y(0.5),stroke:C.faint,'stroke-width':2.5,'stroke-dasharray':'7 7'},s);
 S('path',{d:P(range(-6,6,200).map(z=>[X(z),Y(1/(1+Math.exp(-z)))])),fill:'none',stroke:C.hl,'stroke-width':5},s);
 S('circle',{cx:X(0),cy:Y(0.5),r:10,fill:C.hl},s);S('text',{x:X(0)+18,y:Y(0.5)+30,fill:C.text,'font-size':24},s,'z = 0 → p = 0.5');}
"""
s1 = Scene("The logistic model", "The logistic regression model", r"""
<div class="row" style="gap:40px;align-items:center">
 <div class="col" style="flex:1;gap:22px">
  <div class="card"><span class="tex" data-d="1">P(Y=1\mid X)=\dfrac{1}{1+e^{-(\beta_0+\beta_1X_1+\cdots+\beta_pX_p)}}</span></div>
  <div class="card" data-in="1"><div class="lab">True or false, from the exams</div>
   <div class="small" style="margin-top:10px;line-height:1.55">
   Y is a probability in [0, 1] <span class="verdict f">FALSE</span> <span class="muted">PM2 Q1, Y is 0 or 1</span><br>
   Predictions satisfy 0 &lt; p &lt; 1 <span class="verdict t">TRUE</span> <span class="muted">PM2 Q2</span><br>
   Assumes X is multivariate normal <span class="verdict f">FALSE</span> <span class="muted">PM2 Q3, that's LDA</span><br>
   The formula above is the model <span class="verdict t">TRUE</span> <span class="muted">PM3 Q1</span></div></div>
 </div>
 <svg id="sg" width="680" height="500" viewBox="0 0 680 500"></svg>
</div>""", [
    Step("""Logistic regression passes a linear score, z, through the logistic function. The output is the probability that Y equals one.
When z is zero, the probability is exactly one half. As z grows, it approaches one, but never reaches it."""),
    Step("""That gives four true or false facts the exams love. Y itself is zero or one, not a probability. Predicted probabilities are always
strictly between zero and one. Logistic regression makes no assumption about how X is distributed; that's LDA. And the formula on screen is exactly the model."""),
], script=s1_js, css=KX + ".verdict{font-size:19px;padding:3px 12px;margin:0 8px}")

# ---------------------------------------------------------------- 2 glm output and prediction
s2 = Scene("Predicting from glm output", "Predicting a probability from glm output", r"""
<div class="row" style="gap:36px;align-items:flex-start">
 <div class="console" style="width:940px">
  <div class="faint">&gt; summary(log.mod2) &nbsp;<span class="muted">PM1 · YourCabs</span></div>
  <div style="margin:8px 0 14px">glm(Cancellation ~ OnlineBooking + MobileSiteBooking,<br>&nbsp;&nbsp;&nbsp;&nbsp;family = "binomial")</div>
  <table class="rt">
   <tr class="hd"><td></td><td>Estimate</td><td>Std. Error</td><td>Pr(&gt;|z|)</td><td></td></tr>
   <tr><td>(Intercept)</td><td class="yel">-4.6625</td><td>0.3177</td><td>&lt; 2e-16</td><td class="st">***</td></tr>
   <tr><td>OnlineBooking</td><td>1.6883</td><td>0.3470</td><td>1.14e-06</td><td class="st">***</td></tr>
   <tr><td>MobileSiteBooking</td><td class="yel">2.3231</td><td>0.4117</td><td>1.67e-08</td><td class="st">***</td></tr>
  </table>
  <div class="muted" style="margin-top:12px">AIC: 659.63</div>
 </div>
 <div class="col" style="flex:1;gap:20px">
  <div class="card" data-in="1"><div class="lab">Booked on the mobile site</div>
   <div class="mono" style="font-size:28px;margin-top:8px">z = −4.6625 + 2.3231(1) + 1.6883(0)<br>&nbsp;&nbsp;= −2.3394</div></div>
  <div class="card hl" data-in="1"><span class="tex" data-d="1">p=\dfrac{1}{1+e^{2.3394}}\approx 0.088</span></div>
 </div>
</div>
<div class="row" style="gap:30px;margin-top:24px">
 <div class="small" data-in="1"><b class="yel">Distractor:</b> the question says the vehicle is model 65, but this model has no vehicle variable.</div>
</div>
<div class="small muted" data-in="2" style="margin-top:8px">Check: z &lt; 0 always means p &lt; 0.5. You can leave the answer as an expression.</div>""", [
    Step("""Here's the second logistic model from practice midterm one, predicting whether a driver cancels from how the ride was booked.
The output reads like linear regression, but the estimates are on the log odds scale."""),
    Step("""To predict, compute z first, then convert it. A rider books on the mobile site, so OnlineBooking is zero and MobileSiteBooking is one.
z is minus 4.6625 plus 2.3231, which is minus 2.3394. The probability is one over one plus e to the 2.3394, about 0.088.
The question also says the driver's vehicle is model 65, but this model has no vehicle variable, so ignore it."""),
    Step("""Sanity check: a negative z always means a probability below one half. And you can leave the answer as an expression
if your calculator has no e to the x key."""),
], css=CONSOLE + KX)

# ---------------------------------------------------------------- 3 odds
s3 = Scene("Coefficients and odds", "Coefficients live on the log odds scale", r"""
<div class="card"><span class="tex" data-d="1">z=\log\dfrac{p}{1-p}\qquad\Longrightarrow\qquad e^{\beta}=\text{the factor the odds are multiplied by when }X\text{ rises by }1</span></div>
<div class="row" data-in="1" style="gap:36px;margin-top:28px">
 <div class="card" style="flex:1"><div class="lab">Mobile site booking</div><div class="mono" style="font-size:54px;margin-top:8px">e<sup>2.3231</sup> ≈ <span class="yel">10.2×</span></div><div class="small muted">the odds of cancelling</div></div>
 <div class="card" style="flex:1"><div class="lab">Online booking</div><div class="mono" style="font-size:54px;margin-top:8px">e<sup>1.6883</sup> ≈ <span class="yel">5.4×</span></div><div class="small muted">the odds of cancelling</div></div>
</div>
<div class="small" data-in="1" style="margin-top:22px">Both compared with a booking made through neither channel, everything else equal. Odds, not probability.</div>""", [
    Step("""The linear score z is the log of the odds, p over one minus p. So each coefficient says how the log odds change.
Exponentiate it, and you get the factor the odds are multiplied by when that feature rises by one."""),
    Step("""For mobile site bookings, e to the 2.3231 is about 10.2. A mobile booking has about ten times the odds of cancelling,
compared with a booking made through neither channel. Online bookings: about 5.4 times. That's the odds, not the probability,
though with probabilities this small, the two are close."""),
], css=KX)

# ---------------------------------------------------------------- 4 dummies and red flags
s4 = Scene("Dummies and red flags", "Categorical variables and red flags", r"""
<div class="row" style="gap:36px;align-items:flex-start">
 <div class="console" style="width:900px;font-size:24px">
  <div class="faint">&gt; summary(log.mod1) &nbsp;<span class="muted">PM1 · first model</span></div>
  <table class="rt" style="margin-top:12px">
   <tr class="hd"><td></td><td>Estimate</td><td>Std. Error</td><td>Pr(&gt;|z|)</td></tr>
   <tr><td>(Intercept)</td><td>-21.9830</td><td class="se">7811.7349</td><td class="pv">0.998</td></tr>
   <tr><td>VehicleModelId12</td><td>17.7046</td><td class="se">7811.7349</td><td class="pv">0.998</td></tr>
   <tr><td>VehicleModelId17</td><td>0.3730</td><td class="se">14433.6515</td><td class="pv">1.000</td></tr>
   <tr><td>VehicleModelId23</td><td>0.3039</td><td class="se">8411.4265</td><td class="pv">1.000</td></tr>
   <tr><td class="faint">… 10 more …</td><td></td><td></td><td></td></tr>
   <tr><td>OnlineBooking</td><td>1.6218</td><td>0.3482</td><td>3.20e-06</td></tr>
   <tr><td>MobileSiteBooking</td><td>2.1716</td><td>0.4139</td><td>1.55e-07</td></tr>
  </table>
  <div class="muted" style="margin-top:10px">AIC: 644.88 &nbsp;(model 2: 659.63)</div>
 </div>
 <div class="col" style="flex:1;gap:18px">
  <div class="card" data-hl="0"><div class="lab">Why 13 coefficients for 14 levels?</div><div class="small" style="margin-top:6px">Model 10 is the reference, absorbed into the intercept. A 14th dummy is perfectly collinear with it.</div></div>
  <div class="card" data-in="1" data-hl="1"><div class="lab">Why drop VehicleModelId?</div><div class="small" style="margin-top:6px">Every coefficient has p ≈ 1: none is significant.</div></div>
  <div class="card" data-in="2" data-hl="2"><div class="lab">Go deeper</div><div class="small" style="margin-top:6px">Std. errors near 7,800 signal separation. AIC (lower is better) prefers model 1.</div></div>
 </div>
</div>""", [
    Step("""The first model on practice midterm one included VehicleModelId, a categorical variable with 14 levels, but the output shows only 13 coefficients.
That's dummy coding: one level, here model 10, is the reference, absorbed into the intercept. A fourteenth dummy would add nothing,
since all fourteen always sum to one, which is perfectly collinear with the intercept."""),
    Step("Why remove VehicleModelId? The exam answer: every one of its coefficients has a p-value near one, so none is significant."),
    Step("""To go deeper, look at the standard errors: around 7,800. That's a red flag for separation. Some vehicle models probably had no cancellations at all,
so their coefficients run off toward infinity, and their p-values stop meaning much. And AIC, where lower is better,
actually prefers the first model: 644.88 versus 659.63."""),
], script="function onStep(k){document.querySelectorAll('.se').forEach(e=>e.classList.toggle('flag',k===2));document.querySelectorAll('.pv').forEach(e=>e.classList.toggle('flag',k===1));}",
   css=CONSOLE + ".flag{background:rgba(255,216,74,.15);color:var(--hl)}")

# ---------------------------------------------------------------- 5 LDA and Bayes
s5_js = C_JS + r"""
function init(){const s=document.getElementById('lb');const X=sc(0,20,70,760),Y=sc(0,0.13,330,30);
 const fp=x=>0.9*npdf(x,12,3), ff=x=>0.1*npdf(x,6,3);
 S('line',{x1:X(0),x2:X(20),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);
 [0,5,10,15,20].forEach(v=>S('text',{x:X(v),y:Y(0)+34,'text-anchor':'middle',class:'tick'},s,String(v)));
 S('text',{x:X(10),y:Y(0)+72,'text-anchor':'middle',class:'axl'},s,'hours studied');
 S('path',{d:P(range(0,20,300).map(x=>[X(x),Y(fp(x))])),fill:'none',stroke:C.pos,'stroke-width':4},s);
 S('path',{d:P(range(0,20,300).map(x=>[X(x),Y(ff(x))])),fill:'none',stroke:C.neg,'stroke-width':4},s);
 S('text',{x:X(15.3),y:Y(0.105),fill:C.pos,'font-size':24},s,'0.9 · f_pass');
 S('text',{x:X(1.0),y:Y(0.03),fill:C.neg,'font-size':24},s,'0.1 · f_fail');
 S('line',{x1:X(10),x2:X(10),y1:Y(0),y2:Y(0.125),stroke:C.hl,'stroke-width':3,'stroke-dasharray':'8 6'},s);
 S('circle',{cx:X(10),cy:Y(fp(10)),r:9,fill:C.pos},s);S('circle',{cx:X(10),cy:Y(ff(10)),r:9,fill:C.neg},s);
 const post=fp(10)/(fp(10)+ff(10));
 S('text',{x:X(10)-14,y:Y(0.125)+6,'text-anchor':'end',fill:C.hl,'font-size':24},s,'P(pass | 10 h) ≈ '+post.toFixed(2));}
"""
s5 = Scene("LDA and Bayes' rule", "LDA: model each class, then flip with Bayes' rule", r"""
<div class="row" style="gap:36px;align-items:stretch">
 <div class="col" style="flex:1;gap:20px">
  <div class="card"><div class="lab">LDA's assumption · PM2 Q4 · true</div><div class="small" style="margin-top:6px">Given Y = k, X is multivariate normal, with the <b>same covariance</b> in every class.</div></div>
  <div class="card" data-in="1"><span class="tex" data-d="1">P(Y=k\mid X=x)=\dfrac{\pi_k\,f_k(x)}{\sum_j \pi_j\,f_j(x)}</span><div class="small muted">π<sub>k</sub> = prior share of class k</div></div>
 </div>
 <div class="card hl" data-in="2" style="width:820px"><div class="lab">PM2 · Q12 · 90% of students pass</div>
  <span class="tex" data-d="1">P(\text{pass}\mid 10)=\dfrac{0.9\,f_{pass}(10)}{0.9\,f_{pass}(10)+0.1\,f_{fail}(10)}\;\;\textbf{(B)}</span>
  <svg id="lb" width="770" height="400" viewBox="0 0 800 420"></svg>
  <div class="small muted">Decoys drop the priors (A), the denominator (C), or keep the prior only on top (D).</div></div>
</div>""", [
    Step("""LDA takes the other route. It assumes that within each class, the features follow a multivariate normal distribution,
with the same covariance matrix in every class. That's question four on practice midterm two, and it's true."""),
    Step("""Then it flips those class distributions into a probability with Bayes' rule: the prior for class k times its density at x,
divided by the same thing summed over all the classes."""),
    Step("""Practice midterm two, question twelve: 90 percent of students pass. The probability of passing given 10 hours of study is 0.9 times f pass at 10,
over 0.9 times f pass at 10 plus 0.1 times f fail at 10. That's answer B. The decoys drop the priors, drop the denominator, or keep the prior only on top."""),
], script=s5_js, css=KX + ".card .katex{font-size:.92em}")

# ---------------------------------------------------------------- 6 LDA facts
s6 = Scene("LDA facts and choosing", "Two LDA facts, and which model to use", r"""
<div class="col" style="gap:22px">
 <div class="card"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">PM2 · Q9 · "LDA can't use categorical features"</div><span class="verdict f">FALSE</span></div>
  <div class="small" style="margin-top:8px">They break the normal assumption, but you can dummy-code them and train LDA anyway.</div></div>
 <div class="card" data-in="1"><div class="lab">Two classes, equal variances, equal priors</div>
  <div class="small" style="margin-top:8px">The boundary sits halfway between the means. With means 4 and 5.5 (PM1 Q11), that's <span class="mono yel">4.75</span>. The exam's 4.3 is just a chosen cutoff.</div></div>
 <div class="row" data-in="2" style="gap:22px">
  <div class="card" style="flex:1"><div class="lab">Logistic regression</div><div class="small" style="margin-top:8px">No assumption about X. Safer when features are far from normal.</div></div>
  <div class="card" style="flex:1"><div class="lab">LDA</div><div class="small" style="margin-top:8px">Pays off when normality holds, especially with small samples. Handles 3+ classes naturally.</div></div>
 </div>
</div>""", [
    Step("""Two more LDA facts. Categorical features break the normal assumption, but you can still dummy-code them and train LDA.
So the claim that it's not possible to train LDA with categorical features is false."""),
    Step("""With two normal classes, equal variances, and equal priors, the decision boundary sits halfway between the means.
In question eleven's setup, that's 4.75. The exam's 4.3 is just a chosen cutoff."""),
    Step("""So which should you use? Logistic regression assumes nothing about X, so it's safer when features are far from normal.
LDA's stronger assumption pays off when it holds, especially with small samples, and it handles three or more classes naturally."""),
])

# ---------------------------------------------------------------- 7 recap
s7 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:35px;gap:22px">
  <li><div>p = 1 / (1 + e<sup>−z</sup>), always strictly between 0 and 1. No assumption about X.</div></li>
  <li><div>Predict: compute z from the model's own variables, then convert. z &lt; 0 means p &lt; 0.5.</div></li>
  <li><div>e<sup>β</sup> multiplies the odds. Mobile site: about 10.2 times.</div></li>
  <li><div>K levels become K − 1 dummies. p ≈ 1 everywhere: drop it. Huge std. errors: suspect separation.</div></li>
  <li><div>LDA: normal within each class, shared covariance. Posterior = π<sub>k</sub>f<sub>k</sub>(x) / Σ π<sub>j</sub>f<sub>j</sub>(x).</div></li>
</ol>
<div class="next">Next · Video 5: CART decision trees</div>""", [
    Step("""To recap. Logistic regression outputs one over one plus e to the minus z, always strictly between zero and one, with no assumption about X.
To predict, compute z using only the model's own variables, then convert. e to the beta multiplies the odds.
A factor with K levels becomes K minus 1 dummies, and p-values near one, or huge standard errors, are red flags.
And LDA assumes normal classes with a shared covariance, then uses Bayes' rule with the priors. Next up: CART.""", hold=1.5),
])

VIDEO = Video(4, "v04-logistic", "Logistic regression and LDA", "Logistic regression and LDA",
              [s0, s1, s2, s3, s4, s5, s6, s7])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
