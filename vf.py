"""Video framework: scenes of HTML steps -> narrated MP4 with crossfades, chapters and subtitles."""
import math
import os
import re
import subprocess
import time

import numpy as np
import soundfile as sf
from PIL import Image

import tts

ROOT = os.path.dirname(os.path.abspath(__file__))
NM = "file://" + ROOT + "/node_modules"
OUT = ROOT + "/videos"
FPS = 30
W, H = 1920, 1080
TOTAL_VIDEOS = 8


class Step:
    def __init__(self, say="", hold=0.0, anim=None):
        self.say = " ".join(say.split())
        self.hold = hold
        self.anim = anim  # None or dict(start=0..1, end=0..1) as fractions of the spoken span


class Scene:
    def __init__(self, chapter, title, body, steps, script="", css=""):
        self.chapter, self.title, self.body, self.steps = chapter, title, body, steps
        self.script, self.css = script, css


class Video:
    def __init__(self, num, slug, title, short, scenes):
        self.num, self.slug, self.title, self.short, self.scenes = num, slug, title, short, scenes


def font_faces():
    rules = []
    for fam, pkg, weights, italic in [
        ("Plex Sans", "ibm-plex-sans", [400, 500, 600, 700], [400]),
        ("Plex Mono", "ibm-plex-mono", [400, 500, 600, 700], []),
        ("Fraunces", "fraunces", [400, 600, 700], []),
    ]:
        for w in weights:
            rules.append(f"@font-face{{font-family:'{fam}';src:url('{NM}/@fontsource/{pkg}/files/{pkg}-latin-{w}-normal.woff2') format('woff2');font-weight:{w};font-style:normal}}")
        for w in italic:
            rules.append(f"@font-face{{font-family:'{fam}';src:url('{NM}/@fontsource/{pkg}/files/{pkg}-latin-{w}-italic.woff2') format('woff2');font-weight:{w};font-style:italic}}")
    return "\n".join(rules)


BASE_CSS = r"""
:root{--bg:#0c1320;--panel:#141e2e;--panel2:#1a2638;--line:#2a3950;--text:#eef2f8;--muted:#97a6bd;--faint:#5f6e86;
--pos:#ff9a3d;--neg:#4cb0ff;--hl:#ffd84a;--good:#4fd18b;--bad:#ff6b6b;}
html,body{margin:0;width:1920px;height:1080px;overflow:hidden;color:var(--text);font-family:'Plex Sans',sans-serif;
background:radial-gradient(1400px 900px at 12% -10%,#162540 0%,var(--bg) 62%);}
.frame{position:absolute;inset:0;padding:54px 100px 60px;display:flex;flex-direction:column;box-sizing:border-box}
.top{display:flex;justify-content:space-between;font:500 22px 'Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.top .chap{color:var(--muted)}
h1.title{font:600 60px/1.12 'Fraunces',serif;margin:30px 0 30px;letter-spacing:-.005em;max-width:1600px}
.content{flex:1;position:relative;font-size:37px;line-height:1.38;display:flex;flex-direction:column;justify-content:center;padding-bottom:20px}
.row{display:flex;gap:56px;align-items:flex-start}
.col{display:flex;flex-direction:column;gap:24px}
.card{background:var(--panel);border:2px solid var(--line);border-radius:20px;padding:28px 36px;box-sizing:border-box}
.card.hl{border-color:var(--hl);box-shadow:0 0 0 6px rgba(255,216,74,.13)}
.lab{font:600 22px 'Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.mono{font-family:'Plex Mono',monospace}
.muted{color:var(--muted)} .faint{color:var(--faint)}
.pos{color:var(--pos)} .neg{color:var(--neg)} .good{color:var(--good)} .bad{color:var(--bad)} .yel{color:var(--hl)}
.small{font-size:31px} .big{font-size:48px}
.hidden{visibility:hidden!important}
.dim{opacity:.22}
mark{background:rgba(255,216,74,.16);color:var(--hl);padding:0 .14em;border-radius:6px}
b,strong{font-weight:600}
.tex .katex{font-size:1.08em}
.abs{position:absolute}
/* confusion matrix */
.cm{display:grid;gap:12px}
.cm .h{font:600 22px/1.25 'Plex Mono',monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:flex-end;justify-content:center;text-align:center;padding-bottom:6px}
.cm .rh{justify-content:flex-end;align-items:center;padding:0 18px 0 0;text-align:right}
.cm .cell{border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:3px solid transparent;box-sizing:border-box}
.cm .n{background:rgba(76,176,255,.10);border-color:rgba(76,176,255,.32)}
.cm .p{background:rgba(255,154,61,.10);border-color:rgba(255,154,61,.32)}
.cm .k{font:700 62px 'Plex Mono',monospace;line-height:1.1}
.cm .d{font-size:27px;color:var(--muted)}
.cm .cell.hl{border-color:var(--hl);box-shadow:0 0 0 6px rgba(255,216,74,.16)}
.cm .tot{font:500 26px 'Plex Mono',monospace;color:var(--muted);display:flex;align-items:center}
/* tables */
table.t{border-collapse:collapse;font-size:33px}
table.t th{font:600 22px 'Plex Mono',monospace;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);text-align:left;padding:10px 24px 12px;border-bottom:2px solid var(--line)}
table.t td{padding:14px 24px;border-bottom:1px solid var(--line)}
table.t td.num,table.t th.num{font-family:'Plex Mono',monospace;text-align:right}
table.t tr.hl td{background:rgba(255,216,74,.09)}
/* verdicts and recap */
.verdict{display:inline-block;font:700 23px 'Plex Mono',monospace;letter-spacing:.12em;padding:6px 16px;border-radius:999px;vertical-align:middle}
.verdict.t{background:rgba(79,209,139,.15);color:var(--good)}
.verdict.f{background:rgba(255,107,107,.15);color:var(--bad)}
.verdict.a{background:rgba(255,216,74,.15);color:var(--hl)}
ol.recap{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:30px;font-size:38px;counter-reset:r}
ol.recap li{counter-increment:r;display:grid;grid-template-columns:70px 1fr;align-items:baseline}
ol.recap li::before{content:counter(r);font:600 34px 'Plex Mono',monospace;color:var(--hl)}
.next{position:absolute;left:0;bottom:0;font:500 26px 'Plex Mono',monospace;color:var(--muted);letter-spacing:.06em}
/* svg charts */
svg text{font-family:'Plex Mono',monospace}
.ax line,.ax path{stroke:#3a4a63;stroke-width:2}
.grid line{stroke:#223047;stroke-width:1.5}
.tick{fill:var(--muted);font-size:23px}
.axl{fill:var(--muted);font-size:23px;letter-spacing:.06em}
/* title card */
.motif{position:absolute;right:-20px;top:50%;transform:translateY(-52%)}
.tc{position:relative;margin-top:-40px}
.tc .t1{font:600 112px/1.04 'Fraunces',serif;letter-spacing:-.015em;margin:22px 0 30px}
.tc .t2{font-size:36px;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:14px;margin-top:70px}
.chips span{font:500 27px 'Plex Mono',monospace;color:var(--text);border:2px solid var(--line);border-radius:999px;padding:10px 22px;background:rgba(20,30,46,.7)}
"""

BASE_JS = r"""
const NS='http://www.w3.org/2000/svg';
function S(tag,a,parent,text){const e=document.createElementNS(NS,tag);if(a)for(const k in a)e.setAttribute(k,a[k]);if(text!==undefined&&text!==null)e.textContent=text;if(parent)parent.appendChild(e);return e;}
function erf(x){const s=Math.sign(x);x=Math.abs(x);const t=1/(1+0.3275911*x);const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return s*y;}
function npdf(x,m,s){m=m||0;s=s||1;return Math.exp(-0.5*((x-m)/s)**2)/(s*Math.sqrt(2*Math.PI));}
function ncdf(x,m,s){m=m||0;s=s||1;return 0.5*(1+erf((x-m)/(s*Math.SQRT2)));}
function sc(d0,d1,r0,r1){return v=>r0+(v-d0)*(r1-r0)/(d1-d0);}
function P(pts){return pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join('');}
function range(a,b,n){const o=[];for(let i=0;i<=n;i++)o.push(a+(b-a)*i/n);return o;}
function axes(g,X,Y,x0,x1,y0,y1,xt,yt,xl,yl,fmt){
  fmt=fmt||(v=>String(v));
  const grid=S('g',{class:'grid'},g);
  yt.forEach(v=>S('line',{x1:X(x0),x2:X(x1),y1:Y(v),y2:Y(v)},grid));
  xt.forEach(v=>S('line',{x1:X(v),x2:X(v),y1:Y(y0),y2:Y(y1)},grid));
  const ax=S('g',{class:'ax'},g);
  S('line',{x1:X(x0),x2:X(x1),y1:Y(y0),y2:Y(y0)},ax);
  S('line',{x1:X(x0),x2:X(x0),y1:Y(y0),y2:Y(y1)},ax);
  xt.forEach(v=>S('text',{x:X(v),y:Y(y0)+34,'text-anchor':'middle',class:'tick'},g,fmt(v)));
  yt.forEach(v=>S('text',{x:X(x0)-14,y:Y(v)+8,'text-anchor':'end',class:'tick'},g,fmt(v)));
  if(xl)S('text',{x:(X(x0)+X(x1))/2,y:Y(y0)+76,'text-anchor':'middle',class:'axl'},g,xl);
  if(yl){const t=S('text',{x:0,y:0,'text-anchor':'middle',class:'axl',transform:`translate(${X(x0)-70},${(Y(y0)+Y(y1))/2}) rotate(-90)`},g,yl);}
}
let __step=0;
function setStep(k){
  __step=k;
  document.querySelectorAll('[data-in]').forEach(e=>e.classList.toggle('hidden',+e.dataset.in>k));
  document.querySelectorAll('[data-out]').forEach(e=>{if(+e.dataset.out<=k)e.classList.add('hidden');});
  document.querySelectorAll('[data-hl]').forEach(e=>e.classList.toggle('hl',e.dataset.hl.split(' ').map(Number).includes(k)));
  document.querySelectorAll('[data-dim]').forEach(e=>e.classList.toggle('dim',e.dataset.dim.split(' ').map(Number).includes(k)));
  if(window.onStep)window.onStep(k);
}
"""


def page_html(video, scene):
    chap = f"{video.num:02d} · {video.short}"
    title = f'<h1 class="title">{scene.title}</h1>' if scene.title else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{NM}/katex/dist/katex.min.css">
<style>{font_faces()}{BASE_CSS}{scene.css}</style></head><body>
<div class="frame"><div class="top"><span class="chap">{chap}</span><span>IEOR 142A · Midterm review</span></div>
{title}<div class="content">{scene.body}</div></div>
<script src="{NM}/katex/dist/katex.min.js"></script>
<script>{BASE_JS}
{scene.script}
(async()=>{{
  document.querySelectorAll('.tex').forEach(e=>katex.render(e.textContent,e,{{displayMode:e.dataset.d==='1',throwOnError:true}}));
  if(window.init)window.init();
  await Promise.all(["400 30px 'Plex Sans'","600 30px 'Plex Sans'","500 30px 'Plex Mono'","600 30px 'Plex Mono'","700 30px 'Plex Mono'","600 60px Fraunces"].map(f=>document.fonts.load(f)));
  await document.fonts.ready; setStep(0); window.__ready=true;
}})();</script></body></html>"""


def ease(u):
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def timeline(video):
    shots = []
    for si, sc in enumerate(video.scenes):
        for k, st in enumerate(sc.steps):
            if st.say:
                st.wav, st.dur = tts.synth(st.say)
            else:
                st.wav, st.dur = None, 0.0
            first, last = k == 0, k == len(sc.steps) - 1
            lead = 0.6 if first else 0.32
            tail = 1.0 if last else 0.45
            frames = int(round((lead + st.dur + tail + st.hold) * FPS))
            xf = 0 if not shots else (16 if first else 10)
            shots.append(dict(scene=si, step=k, lead=lead, frames=frames, xf=xf, st=st))
    start = 0
    for s in shots:
        s["start"] = start
        start += s["frames"]
    return shots, start


def render(video, shots, work, only_scenes=None):
    from playwright.sync_api import sync_playwright
    os.makedirs(work, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for si, sc in enumerate(video.scenes):
            if only_scenes is not None and si not in only_scenes:
                continue
            path = f"{work}/scene{si:02d}.html"
            with open(path, "w") as f:
                f.write(page_html(video, sc))
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto("file://" + path)
            page.wait_for_function("window.__ready===true", timeout=30000)
            for shot in [s for s in shots if s["scene"] == si]:
                k, st = shot["step"], shot["st"]
                page.evaluate(f"setStep({k})")
                if st.anim:
                    a0 = shot["lead"] + st.anim.get("start", 0.0) * st.dur
                    a1 = shot["lead"] + st.anim.get("end", 1.0) * st.dur
                    paths, last_u, last_path = [], None, None
                    for i in range(shot["frames"]):
                        t = i / FPS
                        u = 0.0 if t <= a0 else 1.0 if t >= a1 else (t - a0) / (a1 - a0)
                        u = round(ease(u), 4)
                        if u != last_u:
                            page.evaluate(f"anim({u},{k})")
                            last_path = f"{work}/f{si:02d}_{k:02d}_{i:04d}.png"
                            page.screenshot(path=last_path)
                            last_u = u
                        paths.append(last_path)
                    shot["paths"] = paths
                else:
                    pth = f"{work}/f{si:02d}_{k:02d}.png"
                    page.screenshot(path=pth)
                    shot["paths"] = [pth]
            if errors:
                raise RuntimeError(f"scene {si} JS errors: {errors}")
        browser.close()


def caption_chunks(text, limit=84):
    parts = re.split(r"(?<=[.?!])\s+", text)
    out = []
    for p in parts:
        while len(p) > limit:
            cut = p.rfind(", ", 0, limit)
            if cut < limit * 0.4:
                cut = p.rfind(" ", 0, limit)
            else:
                cut += 1
            out.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            out.append(p)
    return out


def srt_time(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def assemble(video, shots, total, work, out_path):
    sr = tts.SR
    audio = np.zeros(int(math.ceil(total / FPS * sr)) + sr, dtype=np.float32)
    subs, idx = [], 1
    for s in shots:
        st = s["st"]
        if not st.wav:
            continue
        data, _ = sf.read(st.wav, dtype="float32")
        a = int(round((s["start"] / FPS + s["lead"]) * sr))
        audio[a:a + len(data)] += data
        chunks = caption_chunks(st.say)
        t0 = s["start"] / FPS + s["lead"]
        total_chars = sum(len(c) for c in chunks)
        for c in chunks:
            d = st.dur * len(c) / total_chars
            subs.append(f"{idx}\n{srt_time(t0)} --> {srt_time(t0 + d)}\n{c}\n")
            idx += 1
            t0 += d
    voiced = np.abs(audio) > 0.005
    rms = float(np.sqrt(np.mean(audio[voiced] ** 2))) if voiced.any() else 1.0
    audio = np.clip(audio * (0.1 / rms), -0.98, 0.98)
    wav = f"{work}/audio.wav"
    sf.write(wav, audio[: int(math.ceil(total / FPS * sr))], sr)
    srt = f"{work}/subs.srt"
    with open(srt, "w") as f:
        f.write("\n".join(subs))
    chap = f"{work}/chapters.txt"
    starts = {}
    for s in shots:
        starts.setdefault(s["scene"], s["start"])
    keys = sorted(starts)
    with open(chap, "w") as f:
        f.write(f";FFMETADATA1\ntitle={video.title}\n")
        for i, si in enumerate(keys):
            a = int(starts[si] / FPS * 1000)
            b = int((starts[keys[i + 1]] if i + 1 < len(keys) else total) / FPS * 1000)
            f.write(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={a}\nEND={b}\ntitle={video.scenes[si].chapter}\n")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-i", srt, "-f", "ffmetadata", "-i", chap,
           "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map_metadata", "3", "-map_chapters", "3",
           "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-ac", "1",
           "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
           "-metadata", f"title={video.title}", "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    prev = None
    cache_path, cache_arr, cache_bytes = None, None, None
    for s in shots:
        for i, pth in enumerate(s["paths"] if len(s["paths"]) > 1 else [s["paths"][0]] * s["frames"]):
            if pth != cache_path:
                cache_arr = np.asarray(Image.open(pth).convert("RGB"))
                cache_bytes = cache_arr.tobytes()
                cache_path = pth
            if i < s["xf"] and prev is not None:
                a = (i + 1) / (s["xf"] + 1)
                a = a * a * (3 - 2 * a)
                frame = (prev.astype(np.float32) * (1 - a) + cache_arr.astype(np.float32) * a).astype(np.uint8)
                proc.stdin.write(frame.tobytes())
            else:
                proc.stdin.write(cache_bytes)
        prev = cache_arr
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")


def assemble_vfr(video, shots, total, work, out_path):
    """Same tracks as assemble(), but the video is variable frame rate: stills are encoded once and held."""
    import shutil
    sr = tts.SR
    audio = np.zeros(int(math.ceil(total / FPS * sr)) + sr, dtype=np.float32)
    subs, idx = [], 1
    for s in shots:
        st = s["st"]
        if not st.wav:
            continue
        data, _ = sf.read(st.wav, dtype="float32")
        a = int(round((s["start"] / FPS + s["lead"]) * sr))
        audio[a:a + len(data)] += data
        chunks = caption_chunks(st.say)
        t0 = s["start"] / FPS + s["lead"]
        total_chars = sum(len(c) for c in chunks)
        for c in chunks:
            d = st.dur * len(c) / total_chars
            subs.append(f"{idx}\n{srt_time(t0)} --> {srt_time(t0 + d)}\n{c}\n")
            idx += 1
            t0 += d
    voiced = np.abs(audio) > 0.005
    rms = float(np.sqrt(np.mean(audio[voiced] ** 2))) if voiced.any() else 1.0
    audio = np.clip(audio * (0.1 / rms), -0.98, 0.98)
    wav = f"{work}/audio.wav"
    sf.write(wav, audio[: int(math.ceil(total / FPS * sr))], sr)
    srt = f"{work}/subs.srt"
    with open(srt, "w") as f:
        f.write("\n".join(subs))
    chap = f"{work}/chapters.txt"
    starts = {}
    for s in shots:
        starts.setdefault(s["scene"], s["start"])
    keys = sorted(starts)
    with open(chap, "w") as f:
        f.write(f";FFMETADATA1\ntitle={video.title}\n")
        for i, si in enumerate(keys):
            a = int(starts[si] / FPS * 1000)
            b = int((starts[keys[i + 1]] if i + 1 < len(keys) else total) / FPS * 1000)
            f.write(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={a}\nEND={b}\ntitle={video.scenes[si].chapter}\n")
    xdir = f"{work}/xf"
    shutil.rmtree(xdir, ignore_errors=True)
    os.makedirs(xdir)
    cache = {}
    def load(p):
        if p not in cache:
            if len(cache) > 6:
                cache.clear()
            cache[p] = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
        return cache[p]
    entries, prev = [], None
    for n, s in enumerate(shots):
        paths = s["paths"] if len(s["paths"]) > 1 else [s["paths"][0]] * s["frames"]
        for i in range(s["frames"]):
            p = paths[i]
            if i < s["xf"] and prev is not None:
                a = (i + 1) / (s["xf"] + 1)
                a = a * a * (3 - 2 * a)
                fp = f"{xdir}/x{n:03d}_{i:02d}.png"
                Image.fromarray((prev * (1 - a) + load(p) * a).astype(np.uint8)).save(fp, compress_level=1)
                entries.append([fp, 1])
            elif entries and entries[-1][0] == p:
                entries[-1][1] += 1
            else:
                entries.append([p, 1])
        prev = load(paths[-1])
    lst = f"{work}/frames.ffconcat"
    with open(lst, "w") as f:
        f.write("ffconcat version 1.0\n")
        for p, nfr in entries:
            f.write(f"file '{p}'\noption framerate {FPS}\nduration {nfr / FPS:.6f}\n")
        f.write(f"file '{entries[-1][0]}'\noption framerate {FPS}\n")
    kf = ",".join(f"{starts[k] / FPS:.3f}" for k in keys)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
           "-i", wav, "-i", srt, "-f", "ffmetadata", "-i", chap,
           "-map", "0:v", "-map", "1:a", "-map", "2:s", "-map_metadata", "3", "-map_chapters", "3",
           "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "20", "-bf", "0", "-pix_fmt", "yuv420p",
           "-fps_mode", "passthrough", "-enc_time_base", "1/30000", "-video_track_timescale", "30000", "-g", "90", "-force_key_frames", kf,
           "-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-ac", "1",
           "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
           "-metadata", f"title={video.title}", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True)
    return len(entries)


def build(video, render_only=None):
    t = time.time()
    work = f"{ROOT}/work/{video.slug}"
    os.makedirs(work, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    shots, total = timeline(video)
    print(f"[{video.slug}] narration ready: {total / FPS:.1f}s ({time.time() - t:.0f}s)", flush=True)
    render(video, shots, work, only_scenes=render_only)
    print(f"[{video.slug}] frames rendered ({time.time() - t:.0f}s)", flush=True)
    if render_only is not None:
        return shots
    out = f"{OUT}/{video.num:02d} {video.title}.mp4"
    n = assemble_vfr(video, shots, total, work, out)
    print(f"[{video.slug}] {n} distinct frames; wrote {out} ({os.path.getsize(out) / 1e6:.1f} MB, {time.time() - t:.0f}s)", flush=True)
    return out
