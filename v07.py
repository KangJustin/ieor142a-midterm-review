from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b',panel:'#141e2e',line:'#2a3950'};\n"
MINI = r"""
function mini(g,x,y,s,col){const L=(a,b,c,d)=>S('line',{x1:x+a*s,y1:y+b*s,x2:x+c*s,y2:y+d*s,stroke:col,'stroke-width':3},g);
 L(0,0,-30,40);L(0,0,30,40);L(-30,40,-48,80);L(-30,40,-12,80);L(30,40,12,80);L(30,40,48,80);
 [[0,0],[-30,40],[30,40]].forEach(([a,b])=>S('circle',{cx:x+a*s,cy:y+b*s,r:8*s,fill:'#0c1320',stroke:col,'stroke-width':3},g));
 [[-48,80],[-12,80],[12,80],[48,80]].forEach(([a,b])=>S('circle',{cx:x+a*s,cy:y+b*s,r:6*s,fill:col},g));}
"""

s0_js = C_JS + MINI + r"""
function init(){const m=document.getElementById('motif');mini(m,140,150,1.6,C.neg);mini(m,320,110,1.6,C.hl);mini(m,490,170,1.6,C.pos);
}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 7 of 8</div>
  <div class="t1">Bagging,<br>random forests,<br>boosting</div>
  <div class="t2">Many trees, combined</div>
  <div class="chips" style="max-width:1000px"><span>Bagging</span><span>Random forests</span><span>Boosting</span><span>Overfitting</span><span>Buggy bagging</span></div>
</div>
<svg class="motif" id="motif" width="620" height="520" viewBox="0 0 620 520"></svg>""", [
    Step("""Ensembles combine many trees. Bagging and random forests average deep trees to cut variance.
Boosting adds small trees one at a time to cut bias. The exam tests which is which, plus two buggy-code questions.""")], script=s0_js)

# ---------------------------------------------------------------- 1 bagging
s1_js = C_JS + MINI + r"""
function init(){const s=document.getElementById('bg');
 S('rect',{x:20,y:200,width:220,height:110,rx:14,fill:C.panel,stroke:C.line,'stroke-width':2.5},s);S('text',{x:130,y:262,'text-anchor':'middle',fill:C.text,'font-size':27},s,'training set');
 [0,1,2].forEach(i=>{const y=60+i*190;S('line',{x1:240,y1:255,x2:380,y2:y+40,stroke:'#4a5a74','stroke-width':3},s);
  S('rect',{x:380,y:y,width:250,height:80,rx:12,fill:C.panel,stroke:C.line,'stroke-width':2.5},s);
  S('text',{x:505,y:y+50,'text-anchor':'middle',fill:C.text,'font-size':25},s,'bootstrap '+(i+1));
  S('line',{x1:630,y1:y+40,x2:700,y2:y+40,stroke:'#4a5a74','stroke-width':3},s);mini(s,780,y+2,1,C.neg);
  S('line',{x1:860,y1:y+40,x2:960,y2:255,stroke:'#4a5a74','stroke-width':3},s);});
 S('rect',{x:960,y:200,width:250,height:110,rx:14,fill:'rgba(255,216,74,.12)',stroke:C.hl,'stroke-width':3},s);
 S('text',{x:1085,y:250,'text-anchor':'middle',fill:C.text,'font-size':26},s,'average');S('text',{x:1085,y:284,'text-anchor':'middle',fill:C.muted,'font-size':22},s,'or majority vote');}
"""
s1 = Scene("Bagging", "Bagging: bootstrap, grow deep trees, average", r"""
<div class="row" style="gap:30px;align-items:center">
 <svg id="bg" width="1230" height="520" viewBox="0 0 1230 520"></svg>
 <div class="col" style="flex:1;gap:18px">
  <div class="card"><div class="small">Deep trees: low bias, high variance. Averaging B of them <b class="yel">cuts the variance</b>.</div></div>
  <div class="card" data-in="1"><div class="row" style="justify-content:space-between;align-items:center"><div class="lab">PM1 · Q4</div><span class="verdict f">FALSE</span></div>
   <div class="small" style="margin-top:8px">"Bagging's main purpose is estimating out-of-sample error." No: it's lowering variance. OOB error is a by-product.</div></div>
 </div>
</div>""", [
    Step("""Bagging, short for bootstrap aggregating, draws B bootstrap samples from the training set, grows a deep tree on each,
then averages their predictions, or takes a vote. Deep trees have low bias but high variance, and averaging many of them cuts the variance."""),
    Step("""So, true or false: the main purpose of bagging is to estimate out of sample error. False. It's to reduce variance.
The out of bag error estimate is a handy by-product."""),
], script=s1_js)

# ---------------------------------------------------------------- 2 random forests
s2 = Scene("Random forests", "Random forests: bagging plus random features", r"""
<div class="card"><div class="lab">The one twist</div><div style="margin-top:8px">At each split, a tree may only consider a <b class="yel">random m of the p features</b> (mtry).</div>
 <div class="small muted" style="margin-top:8px">One strong feature can't sit at the top of every tree, so the trees are less correlated and averaging helps more.</div></div>
<div class="row" style="gap:24px;margin-top:26px" data-in="1">
 <div class="card" style="flex:1.3"><div class="lab">PM1 · Q8 · why are the trees less correlated?</div>
  <div class="small" style="margin-top:8px">Fresh bootstrap samples <b>and</b> random feature subsets: <span class="mono yel">C, both</span></div></div>
 <div class="card" style="flex:1"><div class="lab">Special case</div><div class="small" style="margin-top:8px">m = p is just bagging.</div></div>
</div>""", [
    Step("""A random forest is bagging plus one twist: at each split, the tree may only consider a random subset of m features out of p.
That stops every tree from using the same strong feature at the top, so the trees are less correlated, and averaging them helps more."""),
    Step("""Practice midterm one asks why random forest trees are less correlated: the bootstrap samples, and the random feature subsets.
Both, answer C. And if m equals p, a random forest is just bagging."""),
])

# ---------------------------------------------------------------- 3 boosting
s3_js = C_JS + MINI + r"""
function init(){const s=document.getElementById('bo');const xs=[120,420,720,1020];
 xs.forEach((x,i)=>{mini(s,x,40,0.9,i===3?C.hl:C.pos);S('text',{x:x,y:170,'text-anchor':'middle',fill:C.text,'font-size':24},s,'tree '+(i+1));
  if(i<3){S('line',{x1:x+70,y1:80,x2:xs[i+1]-70,y2:80,stroke:'#4a5a74','stroke-width':3},s);S('path',{d:`M${xs[i+1]-70} 80l-12 -7v14z`,fill:'#4a5a74'},s);
   S('text',{x:(x+xs[i+1])/2,y:118,'text-anchor':'middle',fill:C.muted,'font-size':20},s,'fits the errors');}});
 S('text',{x:570,y:230,'text-anchor':'middle',fill:C.muted,'font-size':24},s,'each tree is small · added with a small learning rate (shrinkage)');}
"""
s3 = Scene("Boosting", "Boosting: small trees, one at a time", r"""
<svg id="bo" width="1720" height="250" viewBox="0 0 1140 250"></svg>
<div class="col" style="gap:14px;margin-top:20px" data-in="1">
 <div class="card"><div class="row" style="justify-content:space-between;align-items:center"><div class="small">Boosting is sequential; random forests train every tree in parallel.</div><div><span class="lab">PM1 Q5 &nbsp;</span><span class="verdict t">TRUE</span></div></div></div>
 <div class="card"><div class="row" style="justify-content:space-between;align-items:center"><div class="small">Boosting works because each new tree is very large.</div><div><span class="lab">PM2 Q6 &nbsp;</span><span class="verdict f">FALSE</span></div></div></div>
 <div class="card"><div class="row" style="justify-content:space-between;align-items:center"><div class="small">Splits per tree is an input, ideally tuned by cross-validation.</div><div><span class="lab">PM3 Q5 &nbsp;</span><span class="verdict t">TRUE</span></div></div></div>
</div>""", [
    Step("""Boosting works differently. It builds small trees one at a time, and each new tree is fit to the errors the current ensemble
still makes, then added in with a small learning rate. It learns slowly, which cuts bias."""),
    Step("""Three true or false facts. Boosting is inherently sequential, while random forests can train every tree in parallel: true.
Boosting works because each tree is very large: false, it uses small trees. And the number of splits per tree is a setting
you tune with cross-validation: true."""),
], script=s3_js)

# ---------------------------------------------------------------- 4 comparison + overfitting
s4 = Scene("Which one overfits?", "The comparison to memorize", r"""
<table class="t" style="width:100%;font-size:30px">
 <tr><th></th><th>Bagging</th><th>Random forests</th><th>Boosting</th></tr>
 <tr><td class="muted">Trees</td><td>deep, independent</td><td>deep, independent</td><td>small, in sequence</td></tr>
 <tr><td class="muted">Main goal</td><td>lower variance</td><td>lower variance</td><td>lower bias</td></tr>
 <tr><td class="muted">Parallel?</td><td>yes</td><td>yes</td><td>no</td></tr>
 <tr data-hl="1"><td class="muted">More trees overfit?</td><td>no</td><td><b class="good">no</b></td><td><b class="bad">yes, eventually</b></td></tr>
 <tr><td class="muted">Settings</td><td>trees</td><td>trees, m (mtry)</td><td>trees, shrinkage, splits</td></tr>
</table>
<div class="row" style="gap:24px;margin-top:24px" data-in="1">
 <div class="card hl" style="flex:1"><div class="lab">PM3 · Q13 · least risk of overfitting</div><div class="small" style="margin-top:6px">More random forest trees: <span class="mono yel">B</span>. Not more boosting rounds or quadratic terms.</div></div>
 <div class="card" style="flex:1"><div class="lab">PM3 · Q11</div><div class="small" style="margin-top:6px">No method always wins. A linear model can beat a forest: <span class="bad">false</span>.</div></div>
</div>""", [
    Step("""Here's the comparison to memorize. Bagging and random forests train independent deep trees, in parallel, to cut variance.
Boosting trains small trees in sequence to cut bias."""),
    Step("""The overfitting question: adding more trees to a random forest doesn't overfit; it just averages more. But more boosting rounds
eventually do, and so does adding quadratic terms to a regression. That's why the answer to practice midterm three, question thirteen, is B.
And no method always wins: a linear model can beat a forest out of sample."""),
])

# ---------------------------------------------------------------- 5 buggy bagging
s5 = Scene("The buggy-bagging questions", "The buggy-bagging questions", r"""
<div class="lab" style="margin-bottom:14px">PM2 · short answer 2 · the code samples WITHOUT replacement</div>
<div class="row" style="gap:28px;align-items:stretch">
 <div class="card" style="flex:1"><div class="lab">(a) Bagging with the bug</div>
  <div class="small" style="margin-top:10px">n rows drawn from n without replacement = the training set, reshuffled. Every tree is identical, so the average is that one tree.</div>
  <div class="mono yel" style="margin-top:14px">= CART with cp = 0, exactly</div></div>
 <div class="card" data-in="1" style="flex:1"><div class="lab">(b) Random forest with the bug, m &lt; p</div>
  <div class="small" style="margin-top:10px">The data never changes, but random feature subsets still make the trees differ, so averaging still cuts variance.</div>
  <div class="mono yel" style="margin-top:14px">≥ CART with cp = 0, usually; often better</div></div>
</div>""", [
    Step("""Practice midterm two has a programming bug: bagging that samples without replacement. Drawing n rows from n rows without replacement
just reshuffles the training set. So every tree is identical, and their average is that same tree. The bagged model performs exactly like
a single CART tree with cp equal to zero."""),
    Step("""Now a random forest with the same bug, with m smaller than p. The data never changes, but each split still draws a random subset of features,
so the trees differ. Averaging them still reduces variance. Expect performance at least as good as CART with cp zero in most cases,
and often better, though less of a gain than a correct random forest."""),
])

# ---------------------------------------------------------------- 6 recap
s6 = Scene("Recap", "Recap", """
<ol class="recap" style="font-size:35px;gap:22px">
  <li><div>Bagging: bootstrap samples, deep trees, average. Its purpose is lower variance.</div></li>
  <li><div>Random forest: bagging plus a random m of p features at each split. m = p is bagging.</div></li>
  <li><div>Boosting: small trees in sequence, each fit to current errors. Tune trees, shrinkage, splits.</div></li>
  <li><div>More forest trees don't overfit. More boosting rounds can.</div></li>
  <li><div>Without replacement: bagging = one CART tree. A random forest still helps a little.</div></li>
</ol>
<div class="next">Next · Video 8: K-means, time series, text, and the exam playbook</div>""", [
    Step("""To recap. Bagging averages deep trees grown on bootstrap samples, to lower variance. A random forest adds a random subset of features
at each split, and with m equal to p it's just bagging. Boosting adds small trees in sequence, each fit to the current errors.
More forest trees don't overfit, but more boosting rounds can. And if the bootstrap samples without replacement,
bagging collapses to a single CART tree. Next: the smaller topics, and an exam playbook.""", hold=1.5),
])

VIDEO = Video(7, "v07-ensembles", "Bagging, random forests and boosting", "Ensembles",
              [s0, s1, s2, s3, s4, s5, s6])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
