# Casual-Inference-in-Virtual-Economies
A DiD approach to the CS2 engine update.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Econometrics](https://img.shields.io/badge/Econometrics-Causal%20Inference-success)
![statsmodels](https://img.shields.io/badge/Library-statsmodels-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## 📌 Executive Summary
This project employs a rigorous **Difference-in-Differences (DiD)** framework to identify the causal impact of the Counter-Strike 2 (CS2) Source 2 engine update on the valuation of virtual digital assets. 

By exploiting the lighting engine overhaul (PBR rendering) as a **Natural Experiment**, this study proves that high-tier aesthetic items experienced a pure, statistically significant **Average Treatment Effect (ATT) of ~50.8%**, independent of macroeconomic liquidity and aggregate game demand. This project serves as an institutional-grade demonstration of high-frequency data engineering, econometric modeling, and computational algorithm optimization.

## 🔬 Research Design & Methodology

### 1. The Natural Experiment ($T_0$)
The CS2 Limited Test announcement on **March 22, 2023**, serves as our exogenous shock ($T_0$). This update drastically improved the physical lighting reactions of specific in-game assets.

### 2. Treatment & Control Groups (Strictly Controlled)
To eliminate Omitted Variable Bias (OVB) caused by item wear/degradation (a critical pricing factor in virtual markets), the dataset is strictly subsetted to **"Factory New" (FN)** items, achieving a perfect Apples-to-Apples comparison:
* **Treatment Group ($N=49$):** Factory New *Doppler* skins (Highly sensitive to the new PBR lighting engine).
* **Control Group ($N=61$):** Factory New *Night* skins (Matte finish, virtually unaffected by lighting updates).

### 3. Macroeconomic Proxy Variables (Addressing API Downsampling)
Due to historical data downsampling by Steam APIs, granular daily player counts for early 2023 were unavailable. To maintain a high-frequency daily panel and robustly control for aggregate liquidity in the digital alternative asset market, **daily Bitcoin (BTC-USD) prices** and the **S&P 500 Index** were integrated as macroeconomic proxy covariates.

## 📊 Core Findings

### 1. Dynamic Model: Event Study & Parallel Trends
A dynamic leads-and-lags DiD model with clustered standard errors at the skin level was deployed to test the parallel trends assumption.
* **Pre-trend:** Point estimates prior to $T_0$ are statistically indistinguishable from zero, confirming that the treatment and control groups shared a parallel trajectory before the announcement (No Anticipation Effect).
* **Marginal Effect:** A stark, statistically significant structural break occurs exactly at $T_0$, persisting over the following 16 weeks with an initial marginal premium of 10%-20%.

<img width="1776" height="951" alt="parallel_trends_verification" src="https://github.com/user-attachments/assets/634ad805-3641-4643-8633-84c8bb88c051" />
<div align="center">
  <br>
  <p><i>Figure 1: Dynamic Event Study & Parallel Trends Assumption. The marginal premium jumped significantly at T0.</i></p>
</div>

### 2. Static Model: Baseline Average Treatment Effect (ATT)
Using an un-truncated static DiD model over a 9-month post-announcement window (capturing the massive hype leading up to the official release), the regression yielded a **True Causal Coefficient of 0.4109**. 
Given the log-transformed dependent variable, this translates to a massive, pure causal premium of **~50.8%** ($\approx e^{0.4109}-1$) driven solely by the engine's visual upgrade.

### 3. Robustness Check: FWL-Accelerated Placebo Test
To ensure the observed causal premium was not a statistical artifact or driven by random market noise, a **Monte Carlo Placebo Test** was conducted over 300 random permutations.

⚡ **Computational Optimization:** A traditional permutation test with Two-Way Fixed Effects (TWFE) resulted in a massive computational bottleneck due to the generation of highly sparse dummy matrices in each loop. To solve this, the **Frisch-Waugh-Lovell (FWL) theorem** was implemented to project out the fixed effects via double-demeaning. This algorithmic optimization compressed the iterative calculation time from tens of minutes to under 10 seconds while maintaining perfect econometric integrity.

* **Result:** The true causal premium (0.4109) vastly outperformed all placebo coefficients, yielding an **empirical p-value of 0.0000**. This definitively confirms the exogenous shock as the sole driver of the observed asset inflation.

<img width="1476" height="876" alt="placebo_test" src="https://github.com/user-attachments/assets/247eb18a-644a-4974-bed5-6d2cac050185" />
<div align="center">
  <br>
  <p><i>Figure 2: Placebo Test Distribution via FWL Theorem. The true causal effect (0.4109) significantly outperforms all placebo permutations (p = 0.0000).</i></p>
</div>
