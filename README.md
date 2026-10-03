# SME-Energy

### An ML-Driven Energy Auditing and Automated Decision System for Turkish Textile SMEs
**Furkan Kalkan and Liang Chengxin**

---

## Quick Start & Demonstration Guide

### 1. Run the Full Intelligence Pipeline
To execute data generation, data quality auditing, AI model training, ISO health scoring, PuLP optimization, and carbon calculations:
```bash
python src/pipeline.py
```

### 2. Launch the Industrial Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501` to interact with the 7 pages:
1. **Factory Overview**: Industrial power telemetry snapshot, factory SEC, and active alert status ticker.
2. **Energy & ToD Monitoring**: Machine power curves and Time-of-Day tariff cost allocation.
3. **Machine Health & Diagnostics**: ISO 10816 vibration severity curves and deep machine drill-down.
4. **Explainable AI Alerts**: 4-tier transparent alert feed.
5. **Production Optimization**: Baseline vs. PuLP load shifting comparison and peak demand shaving.
6. **Carbon & Sustainability**: Configurable 0.42 kg CO2e/kWh Turkey simulation benchmark and carbon intensity.
7. **Architecture & SME Roadmap**: Indicative Turkish SME retrofit budget and 5-phase rollout.

Optional periodic recomputation of the current telemetry and dashboard artifacts:
```bash
streamlit run dashboard/live_monitor.py
```
The independent live monitor updates its telemetry panel in place (default every 5 seconds) and can replay the synthetic sample stream without page reloads. For periodic backend reprocessing of input files, run `python src/refresh_service.py --interval 300` in another terminal. This does not provide physical live sensor readings. The normal one-shot `python src/pipeline.py` and `streamlit run dashboard/app.py` commands remain available.

---

## Executive Summary

The product targets Turkish textile SMEs, with Bursa, Denizli and Gaziantep as illustrative cluster settings. Replace demonstration assumptions with each plant's supplier/OSB contract and production telemetry. Common audit opportunities include:
- Aging legacy machinery without integrated telemetry.
- Flexible loads that may be scheduled against contracted time bands and demand charges.
- Idle energy waste during shift changeovers and unloader valve failures.
- Black-box AI tools that fail to provide actionable physical maintenance guidance.

**Our SME-Energy** is a plug-and-play, non-invasive software and IoT solution that executes the closed-loop cycle:

$$\mathbf{MEASURE} \longrightarrow \mathbf{UNDERSTAND} \longrightarrow \mathbf{DETECT} \longrightarrow \mathbf{PREDICT} \longrightarrow \mathbf{OPTIMIZE} \longrightarrow \mathbf{VERIFY}$$

---

## Key Platform Features

1. **Realistic 4-Machine Textile Ecosystem**:
   - `MOTOR_01`: Ring Spinning Frame Motor (55 kW rated)
   - `COMPRESSOR_01`: Screw Air Compressor for Air-Jet Looms (45 kW rated)
   - `PUMP_01`: Dyeing & Bleaching Liquor Circulation Pump (22 kW rated)
   - `HVAC_01`: Humidification & Climate Control Plant (60 kW rated)
2. **Industrial Data Quality Pipeline (`src/data_processing.py`)**:
   - Transparent auditing of missing values, sensor bounds, and duplicates without silent row dropping.
   - Computes Instantaneous Specific Energy Consumption (`SEC_Proxy`), Thermal Elevation, and ISO Vibration Zones.
3. **Multi-Variate Isolation Forest AI (`src/anomaly_detection.py`)**:
   - Continuous anomaly scoring ($0 - 100$) and severity triaging (`NORMAL`, `MEDIUM`, `HIGH`, `CRITICAL`).
   - Saved model artifacts (`models/anomaly_model.pkl`, `models/model_metadata.json`).
4. **ISO 10816 Machine Health & 4-Tier Explainability (`src/machine_health.py`)**:
   - Industrial vibration severity scoring (Zones A, B, C, D) and 0–100 composite health scores.
   - Structured 4-tier alert feed: **Observed Data $\to$ Model Inference $\to$ Engineering Hypothesis $\to$ Recommended Action**.
5. **PuLP MILP Production Schedule Optimizer (`src/optimization.py`)**:
   - Compares baseline and optimized schedules for cost and peak-demand changes using illustrative TRY time bands.
   - Preserves modeled production targets when feasible; outputs are scenario estimates, not verified savings.
6. **Carbon & Sustainability Accounting (`src/carbon_analysis.py`)**:
   - 0.42 kg CO2e/kWh is used as a synthetic benchmark emission factor for this simulation.
   - Estimates Scope 2 emissions and modeled avoided emissions using the configured factor and optimization schedule.
7. **Industrial Streamlit Dashboard (`dashboard/app.py`)**:
   - Industrial dark slate/green theme with interactive Plotly telemetry curves, machine drill-downs, explainable alerts, and optimization scorecards.

---
## Talking Points

1. **Real-World SME Fit**: Retrofit existing assets with smart meters and condition sensors; use local supplier quotations and verified pilot savings to evaluate payback.
2. **Production-First Optimization**: The PuLP optimizer enforces daily production targets ($\sum X_{m,h} = \text{Target}$) when feasible. Cost results depend on the configured contract scenario.
3. **Explainable AI (XAI)**: We replace black-box alarm fatigue with the **4-Tier Explainability Model** (*Observed Data $\to$ Model Inference $\to$ Engineering Hypothesis $\to$ Recommended Action*), supporting early diagnostic investigation for plant technicians.
4. **Physics & Standards**: Vibration diagnostics use ISO 10816 zone thresholds. The 0.42 kg CO2e/kWh factor is referencing from Turkish Ministry of Energy and Natural Resources.

See [Turkey localization, objective formulation and KPI catalogue](docs/turkey_localization.md) for assumptions, tariff caveats, the MILP objective/constraints and benefit metrics.
