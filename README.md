# IEOR 142A Midterm Review

Eight narrated video lessons and a written study guide for the IEOR 142A (Intro to Machine Learning and Data Analytics) midterm. Everything is built from the Spring 2021 practice midterms 1 to 3.

## Videos

| # | Lesson | Length | Covers |
| --- | --- | --- | --- |
| 1 | [Classification metrics and ROC curves](videos/01%20Classification%20metrics%20and%20ROC%20curves.mp4) | 8:08 | Confusion matrix, accuracy/TPR/FPR, baselines, ROC and AUC, PM1 Q10–Q11 |
| 2 | [Decision analysis](videos/02%20Decision%20analysis%20-%20payoffs%20to%20a%20threshold.mp4) | 7:27 | Decision trees, regret losses, p* = L_FP / (L_FP + L_FN), profit, ensemble thresholds |
| 3 | [Linear regression](videos/03%20Linear%20regression%20-%20reading%20R%20output.mp4) | 6:35 | Reading `summary(lm)`, predictions, p-values, R² vs OSR², VIF, new variables, log(Y) |
| 4 | [Logistic regression and LDA](videos/04%20Logistic%20regression%20and%20LDA.mp4) | 5:45 | The logistic model, predictions, odds, dummy coding, LDA and Bayes' rule |
| 5 | [CART](videos/05%20CART%20decision%20trees.mp4) | 7:11 | Greedy splits, impurity, reading trees, step functions, cp bounds, choosing cp |
| 6 | [Cross-validation and the bootstrap](videos/06%20Cross-validation%20and%20the%20bootstrap.mp4) | 4:18 | k-fold, LOOCV cost, test sets, bootstrap CIs, bias across B |
| 7 | [Bagging, random forests and boosting](videos/07%20Bagging,%20random%20forests%20and%20boosting.mp4) | 3:41 | The three methods, overfitting, the buggy-bagging questions |
| 8 | [K-means, time series, text, playbook](videos/08%20K-means,%20time%20series,%20text%20and%20the%20exam%20playbook.mp4) | 3:53 | K-means, trend/season/AR(1), bag of words, Zipf, features, exam playbook |

Each MP4 has chapters and an embedded subtitle track. The same subtitles are in [`videos/subtitles`](videos/subtitles) as `.srt` files.

## Study guide

[`STUDY_GUIDE.md`](STUDY_GUIDE.md) is the written companion. It has every concept the practice midterms test, worked exam questions, new practice problems with answers, all 43 multiple-choice answers with reasons, and a note-sheet blueprint.

## How the videos are made

Each lesson is a Python file (`v01.py` … `v08.py`) that lists scenes. A scene is an HTML layout plus narrated steps.

1. `tts.py` voices each step with [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) (voice `af_heart`). It spells out decimals and acronyms so they're read correctly, and caches the audio.
2. `vf.py` renders each step's frame in headless Chromium (Playwright). Animated steps get one frame per change.
3. `vf.py` then crossfades the frames and encodes a variable-frame-rate H.264 MP4 with ffmpeg, adding the narration, chapters and subtitles.

`preview.py` renders every step as stills for a quick layout check. `qa.py` checks that video and audio lengths match and transcribes the narration with faster-whisper.

### Rebuild

Requirements: Python 3.11+, Node 18+, ffmpeg.

```bash
pip install -r requirements.txt
python -m playwright install chromium
npm install
mkdir -p models
curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

python preview.py v03        # layout check -> preview/v03-linreg/sheet*.png
python v03.py                # build one video -> videos/
./build_all.sh               # build all eight
```

A full build takes about 4 to 7 minutes per video on 2 CPU cores, mostly narration.

## Source

The exam questions, datasets and R output quoted in the lessons come from the IEOR 142 (UC Berkeley) Spring 2021 practice midterms.
