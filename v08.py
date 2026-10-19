from vf import Scene, Step, Video, build

C_JS = "const C={neg:'#4cb0ff',pos:'#ff9a3d',hl:'#ffd84a',text:'#eef2f8',muted:'#97a6bd',faint:'#5f6e86',axis:'#3a4a63',vio:'#b49cff',good:'#4fd18b',bad:'#ff6b6b',panel:'#141e2e',line:'#2a3950'};\n"
RAND = "let __s=11;function rnd(){__s=(__s*1103515245+12345)%2147483648;return __s/2147483648;}function rnorm(){let u=0,v=0;while(u===0)u=rnd();v=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}\n"
KX = ".katex-display{margin:.2em 0 0}.katex-display>.katex{text-align:left!important}"

s0_js = C_JS + RAND + r"""
function init(){const m=document.getElementById('motif');const cs=[[170,190,C.neg],[420,170,C.pos],[300,400,C.vio]];
 cs.forEach(([cx,cy,c])=>{for(let i=0;i<18;i++)S('circle',{cx:cx+rnorm()*42,cy:cy+rnorm()*42,r:8,fill:c,opacity:0.75},m);
  S('path',{d:`M${cx-14} ${cy}h28M${cx} ${cy-14}v28`,stroke:C.hl,'stroke-width':5},m);});}
"""
s0 = Scene("Intro", None, """
<div class="tc">
  <div class="lab">Video 8 of 8</div>
  <div class="t1">K-means, time series,<br>text and features</div>
  <div class="t2">Plus a playbook for the exam itself</div>
  <div class="chips" style="max-width:1000px"><span>K-means</span><span>Trend · season · AR(1)</span><span>Bag of words</span><span>Zipf's law</span><span>Timestamp features</span><span>Exam playbook</span></div>
</div>
<svg class="motif" id="motif" width="620" height="560" viewBox="0 0 620 560"></svg>""", [
    Step("""This last video covers four small topics that each show up as one or two questions, then a playbook for the exam itself.""")],
    script=s0_js)

# ---------------------------------------------------------------- 1 K-means
s1_js = C_JS + RAND + r"""
function init(){const s=document.getElementById('km');const cs=[[180,170,C.neg],[470,150,C.pos],[330,380,C.vio]];
 cs.forEach(([cx,cy,c])=>{for(let i=0;i<22;i++)S('circle',{cx:cx+rnorm()*48,cy:cy+rnorm()*48,r:9,fill:c,opacity:0.8},s);
  S('path',{d:`M${cx-16} ${cy}h32M${cx} ${cy-16}v32`,stroke:C.hl,'stroke-width':6},s);});}
"""
s1 = Scene("K-means", "K-means clustering", r"""
<div class="row" style="gap:40px;align-items:center">
 <svg id="km" width="640" height="540" viewBox="0 0 640 540"></svg>
 <div class="col" style="flex:1;gap:18px">
  <div class="card"><div class="lab">The loop</div><div class="small" style="margin-top:6px;line-height:1.6">1 · pick K random centers<br>2 · assign each point to its nearest center<br>3 · move each center to its cluster's mean<br>4 · repeat until nothing changes</div></div>
  <div class="card" data-in="1"><div class="lab">PM1 · Q9 · compare K = 5 to 10</div><div class="small" style="margin-top:6px">You choose K. Run it once per K: <span class="mono yel">six runs (C)</span>. Compare within-cluster SS (elbow) and interpretability.</div></div>
  <div class="card" data-in="1"><div class="lab">PM2 · Q8 · <span class="good">true</span></div><div class="small" style="margin-top:6px">Random starts can give different clusters. Run several, keep the lowest within-cluster SS. Scale features first.</div></div>
 </div>
</div>""", [
    Step("""K-means groups points into K clusters. Pick K random centers. Assign each point to its nearest center.
Move each center to the mean of its points. Repeat until nothing changes."""),
    Step("""Two exam facts. You choose K, not the algorithm. To compare K from 5 to 10, run it once per K: six runs. Then compare the
within-cluster sum of squares, and how interpretable the clusters are. And because the starting centers are random, two runs can give
different clusters. That's true on practice midterm two. In practice, run several starts and keep the best,
and scale the features first, since K-means runs on distances."""),
], script=s1_js)

# ---------------------------------------------------------------- 2 time series
s2_js = C_JS + RAND + r"""
function init(){const s=document.getElementById('ts');const X=sc(0,730,60,1060),Y=sc(0,9000,330,20);let prev=2500;const pts=[];
 for(let t=0;t<730;t+=2){const v=2200+3.4*t+1700*Math.sin((t-110)/365*2*Math.PI)+0.6*(prev-(2200+3.4*(t-2)+1700*Math.sin((t-112)/365*2*Math.PI)))+rnorm()*380;prev=v;pts.push([X(t),Y(Math.max(200,v))]);}
 S('line',{x1:X(0),x2:X(730),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);
 S('path',{d:P(pts),fill:'none',stroke:C.neg,'stroke-width':2.5},s);
 S('path',{d:P([[X(0),Y(2200)],[X(730),Y(2200+3.4*730)]]),stroke:C.hl,'stroke-width':4,'stroke-dasharray':'12 8',fill:'none'},s);
 S('text',{x:X(10),y:Y(0)+34,fill:C.muted,'font-size':22},s,'year 1');S('text',{x:X(380),y:Y(0)+34,fill:C.muted,'font-size':22},s,'year 2');
 S('text',{x:X(730),y:20,'text-anchor':'end',fill:C.muted,'font-size':22},s,'daily bike rentals (simulated)');}
"""
s2 = Scene("Time series", "Time series: match the plot to the terms", r"""
<div class="row" style="gap:30px;align-items:flex-start">
 <svg id="ts" width="1080" height="370" viewBox="0 0 1080 370"></svg>
 <table class="t" style="flex:1;font-size:29px">
  <tr><th>You see</th><th>Add</th></tr>
  <tr><td>steady drift</td><td class="yel">trend: β·t</td></tr>
  <tr><td>repeats each year/week</td><td class="yel">month or weekday dummies</td></tr>
  <tr><td>today ≈ yesterday</td><td class="yel">previous value as a feature</td></tr>
 </table>
</div>
<div class="row" style="gap:24px;margin-top:22px">
 <div class="card" data-in="1" style="flex:1"><div class="lab">PM1 · Q12</div><div class="small" style="margin-top:6px">Trend, summer peaks, and day-to-day persistence: use all three, <span class="mono yel">D</span>.</div></div>
 <div class="card" data-in="2" style="flex:1.3"><div class="lab">PM2 · Q10 · <span class="bad">false</span></div><span class="tex" data-d="1">\text{AR}(1):\;X_t=\beta_0+\beta_1X_{t-1}+\varepsilon_t</span>
  <div class="small muted">The exam's version had β₁t and X<sub>t−1</sub> with no coefficient. Split train and test by date.</div></div>
</div>""", [
    Step("""For time series, match the plot to the model terms. A steady drift calls for a trend term, beta times t. A pattern that repeats
each year or week calls for month or weekday dummies. And if each day looks like the day before, add the previous value as a feature."""),
    Step("""Practice midterm one's bike rentals climb over two years, peak every summer, and track the previous day,
so the answer uses all three: D."""),
    Step("""The autoregressive model, AR(1), is X t equals beta zero plus beta one times X t minus one, plus noise. Practice midterm two's version
had a time trend instead, and the previous value with no coefficient, so it's not an AR model: false.
And always split training and test data by date, never at random."""),
], script=s2_js, css=KX)

# ---------------------------------------------------------------- 3 text
s3_js = C_JS + r"""
function init(){const s=document.getElementById('zf');const X=sc(0.5,40.5,60,1000),Y=sc(0,1,300,20);
 for(let r=1;r<=40;r++){S('rect',{x:X(r-0.4),y:Y(1/r),width:X(r+0.4)-X(r-0.4),height:Y(0)-Y(1/r),fill:r>5?'rgba(255,216,74,.65)':'rgba(76,176,255,.75)'},s);}
 S('line',{x1:X(0.5),x2:X(40.5),y1:Y(0),y2:Y(0),stroke:C.axis,'stroke-width':2},s);
 S('text',{x:X(1),y:Y(0)+30,'text-anchor':'middle',class:'tick'},s,'1');S('text',{x:X(40),y:Y(0)+30,'text-anchor':'middle',class:'tick'},s,'40');
 S('text',{x:X(20),y:Y(0)+60,'text-anchor':'middle',class:'axl'},s,'word rank r');
 S('text',{x:X(22),y:Y(0.42),'text-anchor':'middle',fill:C.hl,'font-size':24},s,'long tail: rare words add up');}
"""
s3 = Scene("Text", "Text: bag of words and Zipf's law", r"""
<div class="row" style="gap:28px;align-items:stretch">
 <div class="card" style="flex:1"><div class="lab">Bag of words · PM3 Q10 · <span class="bad">false</span></div>
  <div class="small" style="margin-top:8px">Word counts, order ignored. "Paul likes to travel" written twice has counts of 2, so it's a different vector.</div>
  <div class="small muted" style="margin-top:8px">Cleanup: lowercase, strip punctuation, drop stop words, stem, drop rare terms.</div></div>
 <div class="card" data-in="1" style="flex:1.25"><div class="lab">Zipf · PM2 Q11 · <span class="bad">false</span></div>
  <div class="small" style="margin-top:6px">The r-th most common word appears about 1/r as often as the top word. That's a <b>heavy</b> tail, not a light one.</div>
  <svg id="zf" width="760" height="330" viewBox="0 0 1040 340"></svg></div>
</div>""", [
    Step("""Bag of words turns a document into word counts and ignores the order. So writing a sentence twice doubles its counts,
and the vectors differ. That's false on practice midterm three."""),
    Step("""Zipf's law says the r-th most common word appears about one over r as often as the most common one. That's a heavy tail:
rare words, added together, make up a large share of the text. So practice midterm two's claim of a light, exponential tail is false."""),
], script=s3_js)

# ---------------------------------------------------------------- 4 timestamp features
s4 = Scene("Features from timestamps", "Building features from timestamps", r"""
<div class="lab" style="margin-bottom:14px">PM1 · short answer 5 · BookingDateTime and TripDateTime · at least one feature must use both</div>
<div class="row" style="gap:28px;align-items:stretch">
 <div class="card" style="flex:1"><div class="lab">From one timestamp</div><div class="small" style="margin-top:8px;line-height:1.6">day of week · hour · month<br>weekend or holiday flag<br><span class="muted">coded as dummies</span></div></div>
 <div class="card hl" style="flex:1"><div class="lab">From both</div><div class="mono" style="font-size:30px;margin-top:10px">lead time =<br>TripDateTime − BookingDateTime</div><div class="small muted" style="margin-top:6px">in minutes</div></div>
</div>
<div class="card" data-in="1" style="margin-top:24px"><div class="small"><b class="bad">Leakage rule:</b> only use what you'd know when you predict. A timestamp recorded after the outcome leaks the answer.</div></div>""", [
    Step("""Practice midterm one's last question asks for two features built from the booking and trip timestamps, with at least one that uses both.
From one timestamp: day of week, hour, month, or a weekend flag, coded as dummies. From both: the lead time, trip time minus booking time, in minutes."""),
    Step("""And only build features you'd know at prediction time. Anything recorded after the outcome leaks the answer."""),
])

# ---------------------------------------------------------------- 5 exam playbook
s5 = Scene("Exam playbook", "Exam playbook: six question types", r"""
<table class="t" style="width:100%;font-size:29px">
 <tr><th>When you see</th><th>Do this</th></tr>
 <tr><td>always · never · guaranteed</td><td>Hunt for one counterexample. One is enough for false.</td></tr>
 <tr><td>"most definitive statement"</td><td>Find the tightest range that's guaranteed.</td></tr>
 <tr><td>can a new feature help?</td><td>Linear combination: no. Nonlinear transform: yes.</td></tr>
 <tr data-in="1"><td>enough information?</td><td>Trace every branch. A prediction isn't a probability.</td></tr>
 <tr data-in="1"><td>compute from output</td><td>Write the expression first, then the number.</td></tr>
 <tr data-in="1"><td>justify a choice</td><td>Quote the evidence: p-value, VIF, CV score, plot shape.</td></tr>
</table>
<div class="card" data-in="2" style="margin-top:22px"><div class="small"><b class="yel">Tiebreaker, only when stuck:</b> on these exams, always / impossible / guaranteed claims were usually false, and "it is possible that…" was true both times. The exceptions were math facts.</div></div>""", [
    Step("""Finally, the exam playbook. Most questions fall into six types. Statements with always, never, or guaranteed: hunt for one counterexample,
which is enough to make them false. For the most definitive statement, find the tightest range that's guaranteed.
And for 'can a new feature help': a linear combination of existing features can't, but a nonlinear transform can."""),
    Step("""For 'is there enough information': trace every branch you can't rule out, and remember that a prediction isn't a probability.
For computations from output, write the expression first, then the number. And for justification questions, quote the evidence:
a p-value, a VIF, a cross-validation score."""),
    Step("""One tiebreaker for true or false when you're stuck. In these three exams, always, impossible and guaranteed claims were usually false,
and 'it is possible that' was true both times it appeared. The exceptions were math facts. Use it only as a last resort."""),
])

# ---------------------------------------------------------------- 6 closing
s6 = Scene("What to do next", "What to do next", """
<ol class="recap" style="font-size:36px;gap:26px">
  <li><div>Work the study guide's practice problems under a timer. They're your fresh test.</div></li>
  <li><div>Drill the 43 multiple-choice answers as flashcards. Redo misses the next day.</div></li>
  <li><div>Build your note sheet from the guide's blueprint as you go.</div></li>
  <li><div>Take one full practice midterm with only your note sheet.</div></li>
</ol>
<div class="next">IEOR 142A midterm review · videos 1 to 8</div>""", [
    Step("""That's the whole series. Next, work the practice problems in the study guide under a timer; they're your fresh test.
Drill the multiple choice answers as flashcards, and build your note sheet as you go. Then take one practice midterm with just your note sheet.
Good luck on the midterm.""", hold=2.0),
])

VIDEO = Video(8, "v08-small", "K-means, time series, text and the exam playbook", "Smaller topics and playbook",
              [s0, s1, s2, s3, s4, s5, s6])

if __name__ == "__main__":
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    build(VIDEO, render_only=only)
