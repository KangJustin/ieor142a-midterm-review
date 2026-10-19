# IEOR 142A Midterm Review

Narrated video lessons and a written study guide for the IEOR 142A (Intro to Machine Learning and Data Analytics) midterm. Everything is built from the Spring 2021 practice midterms 1 to 3.

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

Each MP4 has chapters and an embedded subtitle track. The same subtitles are in [`videos/subtitles`](videos/subtitles) as `.srt` files.

## Study guide

[`STUDY_GUIDE.md`](STUDY_GUIDE.md) is the written companion. It has every concept the practice midterms test, worked exam questions, new practice problems with answers, all 43 multiple-choice answers with reasons, and a note-sheet blueprint.

## Source

The exam questions, datasets and R output quoted in the lessons come from the IEOR 142 (UC Berkeley) Spring 2021 practice midterms.
