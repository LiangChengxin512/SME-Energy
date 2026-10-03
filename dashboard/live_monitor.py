"""Independent live-style monitor for the Turkish textile SME demo.

Run from the repository root with:
    streamlit run dashboard/live_monitor.py

The monitor replays synthetic 15-minute telemetry and polls the result CSV on
each fragment tick. It can also display new result files written by the
optional refresh service; it does not claim to ingest physical live meters.
"""

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

try:
    from utils import DEFAULT_GRID_EMISSION_FACTOR, TOD_TARIFF_SLABS
except ImportError:
    DEFAULT_GRID_EMISSION_FACTOR = 0.42
    TOD_TARIFF_SLABS = {
        "PEAK": {"rate": 5.50},
        "NORMAL": {"rate": 4.50},
        "OFF_PEAK": {"rate": 3.50},
    }

TELEMETRY_PATH = ROOT / "results" / "factory_data_enriched.csv"
ALERTS_PATH = ROOT / "results" / "explainable_alerts.csv"
MACHINE_LABELS = {
    "MOTOR_01": "Ring spinning",
    "COMPRESSOR_01": "Air compressor",
    "PUMP_01": "Dyeing pump",
    "HVAC_01": "Humidity / HVAC",
}

st.set_page_config(
    page_title="SME-Energy Live Monitor",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 1rem;}
    .live-banner {padding: 12px 16px; border-radius: 12px;
      background: linear-gradient(90deg,#092b2d,#103c37); border:1px solid #1c7655;
      color:#d9f8e7; margin: 8px 0 18px 0;}
    .live-dot {color:#35e889; font-size:1.1rem; padding-right:8px;}
    div[data-testid="stMetric"] {background:#0c2028; padding:14px;
      border:1px solid #24454d; border-radius:12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SME-Energy | Textile Mill Monitor")
st.caption("Energy audit · explainable machine health · production-aware decisions")
st.markdown(
    f'<div class="live-banner"><span class="live-dot">●</span>'
    "SYNTHETIC TELEMETRY REPLAY · each selected interval advances one "
    "15-minute sample · the panel updates in place without reloading the page</div>",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Monitor controls")
    streaming = st.toggle("Start live view", value=True)
    refresh_seconds = st.select_slider(
        "Display update interval",
        options=[2, 5, 10, 30],
        value=5,
        format_func=lambda value: f"{value} seconds",
    )
    st.divider()
    st.caption("Scenario site: Turkish textile SME")
    st.caption("Grid benchmark: 0.42 kg CO₂e/kWh")
    st.caption(
        "Tariff scenario (TRY/kWh): "
        f"peak {TOD_TARIFF_SLABS['PEAK']['rate']:.2f} · "
        f"day {TOD_TARIFF_SLABS['NORMAL']['rate']:.2f} · "
        f"night {TOD_TARIFF_SLABS['OFF_PEAK']['rate']:.2f}"
    )
    st.caption("Replace demo tariffs and emission factor with plant contract data for an audit.")


def read_telemetry():
    if not TELEMETRY_PATH.exists():
        return None
    try:
        frame = pd.read_csv(TELEMETRY_PATH)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        # The refresh service may be rewriting the artifact at this instant;
        # the next fragment tick will retry without interrupting the dashboard.
        return None
    if frame.empty:
        return None
    frame["Timestamp"] = pd.to_datetime(frame["Timestamp"])
    return frame


def read_alerts():
    if not ALERTS_PATH.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_csv(ALERTS_PATH)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        return pd.DataFrame()
    if not frame.empty:
        frame["Timestamp"] = pd.to_datetime(frame["Timestamp"])
    return frame


@st.fragment(run_every=refresh_seconds if streaming else None)
def live_panel():
    # Read on every fragment tick so the backend refresh service can atomically
    # replace the current pipeline output without a full app rerun.
    frame = read_telemetry()
    if frame is None:
        st.warning("No processed telemetry found. Run `python src/pipeline.py` first.")
        return

    timeline = frame["Timestamp"].drop_duplicates().sort_values().reset_index(drop=True)
    if timeline.empty:
        st.info("Waiting for telemetry records…")
        return

    if "live_replay_index" not in st.session_state:
        st.session_state.live_replay_index = max(0, len(timeline) - min(96, len(timeline)))
    cursor = int(st.session_state.live_replay_index) % len(timeline)
    sample_time = timeline.iloc[cursor]
    current = frame[frame["Timestamp"] == sample_time].copy()

    # A deterministic replay makes the demo move even when no real meters are
    # connected. An external refresh service can replace the source artifacts.
    st.session_state.live_replay_index = (cursor + 1) % len(timeline)
    st.markdown(
        f"**Replay sample:** `{sample_time:%Y-%m-%d %H:%M}` &nbsp; · &nbsp; "
        f"**Updated:** `{pd.Timestamp.now():%H:%M:%S}` &nbsp; · &nbsp; "
        f"**Mode:** {'streaming' if streaming else 'paused'}",
        unsafe_allow_html=True,
    )

    total_power = float(current["Power_kW"].sum())
    interval_energy = float(current["Energy_kWh"].sum())
    interval_cost = float((current["Energy_kWh"] * current["Tariff_Rs_per_kWh"]).sum())
    yarn = current[current["Machine_ID"] == "MOTOR_01"]
    sec = float(yarn["SEC_Proxy"].iloc[0]) if not yarn.empty else 0.0
    interval_carbon = interval_energy * DEFAULT_GRID_EMISSION_FACTOR
    critical = int((current["Severity"].astype(str) == "CRITICAL").sum())
    alert_count = int((current["Predicted_Anomaly"].fillna(0).astype(int) == 1).sum())

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Factory demand", f"{total_power:,.1f} kW")
    k2.metric("15-min energy", f"{interval_energy:,.2f} kWh")
    k3.metric("Interval cost", f"₺{interval_cost:,.2f}")
    k4.metric("Yarn SEC proxy", f"{sec:.3f} kWh/kg")
    k5.metric("Scope 2 estimate", f"{interval_carbon:.2f} kg CO₂e")
    k6.metric("AI flags / critical", f"{alert_count} / {critical}")

    left, right = st.columns([1.6, 1])
    with left:
        timeline_mask = (frame["Timestamp"] <= sample_time) & (
            frame["Timestamp"] >= sample_time - pd.Timedelta(hours=24)
        )
        trend = frame.loc[timeline_mask].copy()
        fig = px.line(
            trend,
            x="Timestamp",
            y="Power_kW",
            color="Machine_ID",
            color_discrete_sequence=["#27d98b", "#35a7ff", "#ffad42", "#b28dff"],
            labels={"Timestamp": "Replay time", "Power_kW": "Power (kW)", "Machine_ID": "Asset"},
            title="Machine power · trailing 24-hour replay window",
        )
        fig.update_layout(
            template="plotly_dark", height=370, margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(7,20,27,0.75)",
            legend=dict(orientation="h", y=1.12),
        )
        st.plotly_chart(fig, use_container_width=True, key="live_power_chart")

    with right:
        st.markdown("#### Asset status at this sample")
        for _, row in current.sort_values("Machine_ID").iterrows():
            label = MACHINE_LABELS.get(row["Machine_ID"], row["Machine_ID"])
            risk = str(row.get("Risk_Level", "LOW"))
            color = "🔴" if risk in {"HIGH", "CRITICAL"} else "🟡" if risk == "MEDIUM" else "🟢"
            st.markdown(
                f"**{color} {label}** · {row['Power_kW']:.1f} kW · "
                f"vibration {row['Vibration_mm_s']:.2f} mm/s · "
                f"health {row.get('Health_Score', 0):.0f}/100"
            )
            st.caption(
                f"Thermal elevation {row.get('Temp_Elevation', 0):+.1f}°C · "
                f"ISO zone {row.get('ISO_Vib_Zone', 'N/A')} · {row.get('Machine_Status', 'N/A')}"
            )

    st.markdown("#### Explainable alerts around the replay point")
    alerts = read_alerts()
    if alerts.empty:
        st.info("No alert records are available.")
    else:
        near = alerts[
            (alerts["Timestamp"] >= sample_time - pd.Timedelta(minutes=30))
            & (alerts["Timestamp"] <= sample_time)
        ].sort_values("Timestamp", ascending=False).head(3)
        if near.empty:
            st.success("No explainable alert in the last 30 replay minutes.")
        else:
            for _, alert in near.iterrows():
                st.warning(
                    f"{alert['Machine_Name']} · {alert['Severity']} · "
                    f"{alert['Engineering_Hypothesis']}\n\n"
                    f"Recommended action: {alert['Recommended_Action']}"
                )

    st.caption(
        "Demo note: the replay advances through synthetic 15-minute records; it is not live meter ingestion. "
        "The panel polls result files each tick, so a separately running refresh service can update its source data."
    )


live_panel()
