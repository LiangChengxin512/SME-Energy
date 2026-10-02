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
6. **Carbon & Sustainability**: Configurable CEA grid factor slider and carbon intensity.
7. **Architecture & SME Roadmap**: Low-cost IoT retrofit kit BOM (< ₹18,000/machine) and 5-phase rollout.

---

## Executive Summary

Small and Medium Enterprises (SMEs) in textile hubs operate on thin margins (3–8%), with electricity accounting for up to 30% of operational costs. Most factories face:
- Aging legacy machinery without integrated telemetry.
- Punitive Time-of-Day (ToD) peak electricity surcharges (up to ₹10/kWh during 18:00–22:00).
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
   - Shaves peak grid demand by **8.08%** (12.51 kW reduction: 154.89 kW $\to$ 142.38 kW) and reduces daily electricity costs by **4.78%** (modeled savings: ₹1,127.79 / day = ₹338,337/year across 300 operating days/year).
   - **Enforces 100% throughput conservation** (4,500 kg daily finished yarn production maintained without shortfall).
6. **CEA Carbon & Sustainability Accounting (`src/carbon_analysis.py`)**:
   - 0.82 kg CO2e/kWh is used as a synthetic benchmark emission factor for this simulation (referencing India's CEA Baseline Database Version 19 methodology).
   - Avoids an estimated 10.99 kg CO2e/day (3.30 t CO2e/year across 300 operating days/year) in indirect Scope 2 emissions through peak load shifting and efficiency.
7. **Industrial Streamlit Dashboard (`dashboard/app.py`)**:
   - Industrial dark slate/green theme with interactive Plotly telemetry curves, machine drill-downs, explainable alerts, and optimization scorecards.

---
## Talking Points

1. **Real-World SME Fit**: Rather than asking an SME to scrap their ₹40 Lakh spinning frame, the proposed deployment retrofits it with a standard DIN-rail multifunction energy meter and an external vibration sensor, offering a low-barrier retrofit telemetry approach where payback can be determined from pilot installation costs and verified annual savings.
2. **Production-First Optimization**: The PuLP optimizer strictly enforces daily production targets ($\sum X_{m,h} = \text{Target}$). Modeled energy savings come from **smart load shifting away from the ₹10/kWh peak tariff**, not by shutting down the factory.
3. **Explainable AI (XAI)**: We replace black-box alarm fatigue with the **4-Tier Explainability Model** (*Observed Data $\to$ Model Inference $\to$ Engineering Hypothesis $\to$ Recommended Action*), supporting early diagnostic investigation for plant technicians.
4. **Credible Physics & Standards**: All vibration diagnostics adhere strictly to **ISO 10816-3**, and 0.82 kg CO2e/kWh is used as a synthetic benchmark emission factor for this simulation referencing the **Central Electricity Authority (CEA) Baseline Database v19** methodology.