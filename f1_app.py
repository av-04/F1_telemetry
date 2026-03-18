import os

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as sd

import Driving_style_analysis
import racing_line
import strat_score

sd.set_page_config(page_title="F1_telemetry_comparisions", layout="wide")

cache_dir = "cache"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)


@sd.cache_data
def load_session(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session


sd.sidebar.title("telemetry settings")
grand_prix = sd.sidebar.text_input("Race Location", "Monaco")
year = sd.sidebar.selectbox("Year", [2020, 2021, 2022, 2023, 2024])
session_map = {
    "Race": "R",
    "Qualifying": "Q",
    "Sprint": "S",
    "FP1": "FP1",
    "FP2": "FP2",
    "FP3": "FP3",
}
session_name = sd.sidebar.selectbox("Session", list(session_map.keys()), index=1)
session_identifier = session_map[session_name]
d1 = sd.sidebar.text_input("Driver 1 (e.g., VER)", "VER")
d2 = sd.sidebar.text_input("Driver 2 (e.g., HAM)", "HAM")

sd.title(f"F1_telemetary_comparisions :{d1}vs{d2}")
sd.write(f"**Event:** {year}{grand_prix}-{session_name}")
if sd.sidebar.button("Load Telemetry"):
    # Loading
    with sd.spinner(f"Searching for '{grand_prix}' in {year}..."):
        session = load_session(year, grand_prix, session_identifier)

    # Validation
    if session:
        sd.success(f"Found Session: {session.event['EventName']}")

        with sd.spinner("Processing Telemetry..."):
            try:
                laps_d1 = session.laps.pick_driver(d1).pick_fastest()
                laps_d2 = session.laps.pick_driver(d2).pick_fastest()

                if laps_d1 is None:
                    sd.error(f"Driver {d1} not found or set no time.")
                    sd.stop()
                if laps_d2 is None:
                    sd.error(f"Driver {d2} not found or set no time.")
                    sd.stop()

                # Telemetry
                tel_d1 = laps_d1.get_car_data().add_distance()
                tel_d2 = laps_d2.get_car_data().add_distance()

                sd.subheader(f"Speed Trace: {d1} vs {d2}")
                fig1, ax1 = plt.subplots(figsize=(10, 5))

                color1 = fastf1.plotting.get_driver_color(d1, session=session)
                color2 = fastf1.plotting.get_driver_color(d2, session=session)

                ax1.plot(tel_d1["Distance"], tel_d1["Speed"], color=color1, label=d1)
                ax1.plot(tel_d2["Distance"], tel_d2["Speed"], color=color2, label=d2)
                ax1.set_xlabel("Distance (m)")
                ax1.set_ylabel("Speed (km/h)")
                ax1.legend()
                ax1.grid(True, linestyle="--", alpha=0.5)

                sd.pyplot(fig1)

                # Delta
                sd.subheader("Time Delta (Gap)")
                sd.caption(
                    f"Negative (Color 1) = {d1} is Ahead | Positive (Color 2) = {d2} is Ahead"
                )

                max_dist = max(tel_d1["Distance"].max(), tel_d2["Distance"].max())
                dist_grid = np.linspace(0, max_dist, int(max_dist))

                time_d1 = np.interp(
                    dist_grid, tel_d1["Distance"], tel_d1["Time"].dt.total_seconds()
                )
                time_d2 = np.interp(
                    dist_grid, tel_d2["Distance"], tel_d2["Time"].dt.total_seconds()
                )

                delta = time_d2 - time_d1

                fig2, ax2 = plt.subplots(figsize=(10, 4))
                ax2.plot(dist_grid, delta, color="white", linewidth=1)
                ax2.axhline(0, color="gray", linestyle="--")

                ax2.fill_between(
                    dist_grid, 0, delta, where=delta < 0, color=color1, alpha=0.3
                )
                ax2.fill_between(
                    dist_grid, 0, delta, where=delta > 0, color=color2, alpha=0.3
                )

                ax2.set_facecolor("black")
                ax2.set_ylabel("Gap (seconds)")
                ax2.set_xlabel("Distance (m)")

                sd.pyplot(fig2)

                # FOR_RACING_LINE
                sd.markdown("---")
                sd.subheader("racing_line_analysis")
                sd.write(f"Visualizing **{d1}'s** fastest lap.")
                with sd.spinner(f"Generating track_graph for {d1}"):
                    fig_track = racing_line.plot_racing_line(session, d1)
                    if fig_track:
                        sd.pyplot(fig_track)
                    else:
                        sd.error("no map")
            except Exception as e:
                sd.error(f"An error occurred during plotting: {e}")

                # FOR_ELORATINGANDPREDICTION
            sd.markdown("---")
            sd.subheader("ELO Rating based on the performance in race")
            try:
                sd.info(f"Comparing Pace, Overtaking, and Consistency for elo rating.")
                col1, col2 = sd.columns(2)
                score_d1 = strat_score.calc_strat_score(session, d1)
                score_d2 = strat_score.calc_strat_score(session, d2)
                proj_pts_d1 = max(0, int((score_d1 - 1000) * 0.6))
                proj_pts_d2 = max(0, int((score_d2 - 1000) * 0.6))
                with col1:
                    sd.metric(
                        label=f"{d1} Rating",
                        value=f"{score_d1}",
                        delta=f"{proj_pts_d1} Proj. Pts",
                    )
                    sd.progress(min(max((score_d1 - 1000) / 1500, 0.0), 1.0))

                with col2:
                    sd.metric(
                        label=f"{d2} Rating",
                        value=f"{score_d2}",
                        delta=f"{proj_pts_d2} Proj. Pts",
                    )
                    sd.progress(min(max((score_d2 - 1000) / 1500, 0.0), 1.0))

                # The_Verdict
                if score_d1 > score_d2:
                    gap = score_d1 - score_d2
                    sd.success(f" **WINNER: {d1}** (+{gap} pts)")
                    sd.write(
                        f"The Strat_Score algorithm predicts **{d1}** had a better score based on higher consistency and racecraft in this session."
                    )
                elif score_d2 > score_d1:
                    gap = score_d2 - score_d1
                    sd.success(f" **WINNER: {d2}** (+{gap} pts)")
                    sd.write(
                        f"The Strat_Score algorithm predicts **{d2}** had a better score based on higher consistency and racecraft in this session."
                    )
                else:
                    sd.warning(" **It's a Tie!**")
            except Exception as e:
                sd.error(f"An error occurred during processing: {e}")
            # Fordriverstyleanalysis
            sd.markdown("---")
            sd.subheader("AI Driving Style Profiler (K-Means Clustering)")
            sd.write(
                "An unsupervised Machine Learning algorithm analyzed the Throttle, Brake, and Speed inputs to categorize the lap into three behavioral states."
            )
            try:
                with sd.spinner("Training K-Means Clustering Model..."):
                    perc_d1, perc_d2 = Driving_style_analysis.analyze_driving_style(
                        tel_d1, tel_d2
                    )

                    if perc_d1 is not None:
                        style_df = pd.DataFrame(
                            {
                                "Driving State": [
                                    "Heavy Braking / Slow",
                                    "Traction / Partial Throttle",
                                    "Flat Out / High Speed",
                                ],
                                d1: perc_d1,
                                d2: perc_d2,
                            }
                        ).set_index("Driving State")

                        fig_style, ax_style = plt.subplots(figsize=(10, 4))
                        style_df.plot(
                            kind="barh", ax=ax_style, color=[color1, color2], alpha=0.8
                        )

                        ax_style.set_xlabel("% of Lap Spent in State")
                        ax_style.set_facecolor("black")
                        ax_style.grid(axis="x", linestyle="--", alpha=0.3)

                        sd.pyplot(fig_style)

                        sd.info(
                            f"**Data Insight:** If {d1} has a lower percentage in 'Traction / Partial Throttle', they are likely using a 'V-Style' cornering technique (getting to 100% throttle faster)."
                        )
                    else:
                        sd.warning("Could not calculate driving style clusters.")
            except Exception as e:
                sd.error(f"Driving Style Error: {e}")
    else:
        sd.warning(
            f"Could not find a race named '{grand_prix}' in {year}. Please check your spelling."
        )

else:
    sd.info("Enter the Race Location in the sidebar and click 'Load Telemetry'")
