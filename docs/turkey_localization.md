# Turkey Textile SME Energy Audit & Automated Decision Support

## Product definition

- **Applied area of AI product:** Industrial energy auditing and automated decision support for textile SMEs: energy/SEC benchmarking, explainable anomaly triage, machine condition monitoring, carbon accounting, and production-aware energy scheduling.
- **Project objective:** Help Turkish textile SMEs reduce electricity cost and Scope 2 emissions, extend machine life, and preserve production throughput through continuous energy auditing and explainable, health-aware operating recommendations.
- **Plant story:** A representative spinning, weaving and dyeing SME with ring-spinning motors, compressed air, dyeing circulation pumps and humidity/HVAC loads. Bursa, Denizli and Gaziantep are illustrative textile-cluster settings; the sample data are synthetic, not customer telemetry.

## Turkey configuration and limits

The model stores internal legacy field names such as `Tariff_Rs_per_kWh` and `Total_Cost_Rs` so existing pipeline artifacts and dashboard readers remain compatible. Values in those fields now represent **TRY**, and the dashboard labels them accordingly.

Turkey does not have one universal three-period industrial price. The actual bill depends on the supplier or bilateral contract, connection voltage, distribution area/organized industrial zone (OSB), demand charges, taxes and the applicable tariff. The code's Peak 5.50, Day 4.50 and Night 3.50 TRY/kWh values are **illustrative optimization assumptions**, not quoted national tariffs. As an external 2026 anchor, Invest in Türkiye lists industrial consumer electricity prices of USD 85–130.50/MWh, varying by connection type, inclusive of taxes; users should enter their own contract tariff for a defensible audit. See [Invest in Türkiye: Cost of Doing Business](https://f.invest.gov.tr/en/investmentguide/pages/cost-of-doing-business.aspx) and [EPDK tariff and bill information](https://lisans.epdk.gov.tr/epvys-web/faces/pages/online/tarifeFatura/tarifeFatura.xhtml).

The demo retrofit bill of materials in the dashboard uses broad **budget placeholders in TRY**, not vendor quotations: 3-phase meter ₺8,000–₺14,000; CT set ₺2,000–₺4,000; vibration sensor ₺5,000–₺12,000; temperature sensor ₺1,500–₺4,000; edge gateway ₺8,000–₺20,000. Installation, wiring, tax, calibration and software are excluded. Obtain local supplier quotations before investment/payback decisions.

The requested grid factor is **0.42 kg CO₂e/kWh**. It is treated as a user-provided Turkey simulation benchmark, not represented as a current official Turkish factor or plant-specific audited value. Replace it with an applicable, dated national/supplier factor before regulatory or external ESG reporting.

## Modeling story for a presentation

Tell the story as four linked stages: **meter readings → audit features → explainable alerts → production schedule**. The equations below are a compact and reasonable presentation model. They describe both the implemented analytics and a proposed richer optimization objective; the distinction is stated clearly so the presentation does not imply that every term is already in the code.

### 1. Convert machine readings into useful audit features

For machine $m$ at 15-minute sample $t$, the system observes power $P_{m,t}$, temperature $T_{m,t}$, vibration $V_{m,t}$ and production $q_{m,t}$. Since $\Delta t=0.25$ hour:

$$E_{m,t}=P_{m,t}\Delta t,\qquad SEC_{m,t}=\frac{E_{m,t}}{\max(q_{m,t},\epsilon)}.$$

Compare thermal and vibration readings to their machine baselines:

$$\Delta T_{m,t}=T_{m,t}-T^{base}_m,\qquad \Delta V_{m,t}=V_{m,t}-V^{base}_m.$$

These indicators answer: how much energy was used, how much energy was needed per unit of output, and whether heat or vibration is drifting from normal. The code calls the interval energy-per-output value `SEC_Proxy` because a 15-minute reading is a short-horizon signal, not an audited shift-level SEC.

### 2. Detect unusual behavior and explain it to an operator

Combine normalized features into $z_{m,t}=[SEC,\Delta T,\Delta V,\text{load ratio},\ldots]$. The Multivariate Isolation Forest scores whether the combination is unusual:

$$A_{m,t}=\mathbf{1}[s(z_{m,t})<\tau],$$

where $s(\cdot)$ is the model score and $\tau$ is its threshold. The model flags a pattern, while the alert presents **observed readings → model severity → likely engineering cause → recommended inspection**. ISO 10816 vibration zones and a composite health score make the condition assessment easier to interpret. A likely cause is a technician's investigation lead, not proof of a failure.

### 3. Optimize production with factory constraints

For planning hour $h$, define production $x_{m,h}\ge0$, run/batch binary $y_{m,h}\in\{0,1\}$, machine power $p_{m,h}\ge0$, and plant peak $D\ge0$. A presentation-level multi-objective framework is:

$$\min J=\lambda_C\frac{C}{C_0}+\lambda_D\frac{D}{D_0}+\lambda_G\frac{G}{G_0}+\lambda_H\frac{R}{R_0},$$

$$C=\sum_{m,h}c_h p_{m,h}\Delta t,\qquad D\ge\sum_m p_{m,h}\quad\forall h,$$

$$G=\sum_{m,h}g_h p_{m,h}\Delta t,\qquad R=\sum_{m,h}r_{m,h}y_{m,h}.$$

$C$ is energy cost (TRY), $D$ is peak demand (kW), $G$ is estimated Scope 2 emissions, and $R$ is a machine-condition risk proxy. $C_0,D_0,G_0,R_0$ normalize the different units; the $\lambda$ weights express business priorities. If $g_h$ is constant and the plan uses the same total energy, emissions are an outcome rather than a useful scheduling lever. A time-varying grid factor or energy-saving decision is needed for carbon to change the preferred schedule.

The schedule must still produce the required output and respect machine capabilities:

$$\sum_h x_{m,h}=Q_m,\qquad \underline q_m y_{m,h}\le x_{m,h}\le\overline q_m y_{m,h},$$

$$p_{m,h}=P^{idle}_m y_{m,h}+\alpha_m x_{m,h},\qquad 0\le p_{m,h}\le P^{max}_m a_{m,h}.$$

$Q_m$ is the output target; $a_{m,h}$ represents availability after maintenance and condition-based derating. Add process constraints where needed: HVAC must support spinning-hall humidity, dyeing pump batches run for three consecutive hours, and a plant may impose $D\le D^{contract}$ for its contracted demand.

### Implemented demo vs. proposed presentation framework

The expanded $J$ above is a **proposed presentation framework**. The current PuLP model implements the shorter objective:

$$\min\sum_{m,h}c_h p_{m,h}+\lambda D,\qquad D\ge\sum_m p_{m,h}\quad\forall h.$$

The implemented constraints preserve production targets when feasible and include availability/health derating, HVAC-to-spinning coupling, and contiguous dyeing-pump batches. Carbon is reported beside the schedule, and machine health can constrain availability; the current objective does **not** include a separate carbon or maintenance-risk term, and it does not calculate guaranteed asset-life extension. On stage, call the expanded objective the **proposed decision framework** and the shorter one the **implemented demo MILP**. The code's scenario tariff assumptions are in `src/utils.py`.
## AI and audit methods currently represented

- Multivariate Isolation Forest for anomaly detection and severity triage, with human-readable alerts.
- Industrial feature engineering and benchmark accounting for `SEC_Proxy`, thermal elevation, load ratios and energy/cost.
- ISO 10816 vibration zones and a composite machine health score used for condition-aware recommendations/scheduling.
- Carbon audit: $E_{CO2e}=E_{kWh}\times0.42$, and carbon intensity per kg yarn; optimization avoided emissions are scenario-derived.
- PuLP MILP dispatch for time-band cost and demand-peak reduction.

The energy/carbon savings are modeled outcomes on synthetic profiles. `dashboard/live_monitor.py` replays synthetic telemetry in place using Streamlit fragments; `src/refresh_service.py` can periodically regenerate pipeline artifacts. Neither currently ingests physical meter readings, establishes causal savings, or verifies actual equipment life extension.

Launch the independent replay dashboard with `streamlit run dashboard/live_monitor.py`. It polls result files on every tick and advances through the synthetic 15-minute records without refreshing the full page. To periodically refresh those files, run `python src/refresh_service.py --interval 300` in another terminal.

## Benefit and KPI catalogue

| Outcome | System metric / formula | Interpretation |
|---|---|---|
| Electricity spend | `Total_Cost_Rs` (TRY under the Turkey configuration), $\sum_{m,h} E_{m,h}c_h$ | Modeled bill component; add real invoices, taxes, demand charges and contract rules for audited bills. |
| Cost saving | baseline cost − optimized cost; percentage vs baseline | Scheduling scenario delta; report TRY/day, TRY/year only with disclosed operating-day assumption. |
| Energy use | total `Energy_kWh`; kWh by machine/state/time band | Audit consumption and identify high-use assets. |
| Peak demand | max hourly factory kW; optimized reduction in kW and % | Demand management potential, not necessarily bill saving unless contract bills demand. |
| Production-normalized energy | SEC = kWh / output; yarn SEC in kWh/kg; `SEC_Proxy` for instant/interval benchmarks | Separates energy performance from changes in throughput/product mix. |
| Idle waste | idle kWh and TRY by machine/state | Quantifies nonproductive consumption opportunities. |
| Scope 2 emissions | kWh × grid factor; kg CO₂e and t CO₂e | Location/supplier factor and reporting boundary must be stated. |
| Carbon intensity | kg CO₂e / kg yarn | Production-normalized emissions indicator. |
| Avoided carbon | baseline less optimized kg CO₂e | Valid only for the modeled electricity schedule/factor; not offset or verified abatement. |
| Asset health | ISO 10816 vibration zone, composite health score, thermal elevation, alert count/severity | Leading maintenance indicators; not a guaranteed remaining-useful-life forecast. |
| Production service | output vs target; throughput conservation % | Confirms savings recommendation does not trade away planned output. |
| Reliability & response | anomaly count, alert precision/recall (when labeled), downtime hours, MTTR/MTBF (once captured) | Operational benefit requires real maintenance/work-order data. |
| Financial return | annual verified savings / retrofit investment; payback months | Calculate only after metered pilot and actual installed cost. |

The current dashboard already exposes total energy, cost, SEC, peak demand, idle waste, production output, machine health/alerts, optimization cost and peak deltas, and carbon footprint/intensity/avoided emissions. Availability depends on the generated result artifacts.
