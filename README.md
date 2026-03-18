# 🏎️ F1 Telemetry Explorer

A Python-based telemetry analysis tool that allows users to compare Formula 1 driver performance in real-time. Built with **FastF1**, **Streamlit**, and **Matplotlib**.

## 🚀 Features
* **Dynamic Race Selection:** Automatically fetches the race calendar for any season (2020-2024).
* **Speed Trace Analysis:** Compare speed vs. distance for any two drivers.
* **Gap Analysis (Delta):** Visualizes where one driver is gaining or losing time against another using linear interpolation.
* **Corner Visualization:** Highlights track sectors and braking zones.
* **Elo rating based on the current race:** Uses an Elo-like rating system named `strat_score` which uses finishing position, overtaking, and consistency.

  ```
  Strat_Score = Base + S_Finish + S_Overtake + S_Consistency
  ```

  Short explanation:
  - Base: baseline points or starting rating for the calculation
  - S_Finish: contribution from finishing position (higher for better finishes)
  - S_Overtake: bonus for overtaking moves made during the race
  - S_Consistency: reward/penalty based on lap-to-lap consistency

## 🛠️ Tech Stack
* **Python 3.10+**
* **Streamlit** (Frontend/UI)
* **FastF1** (Data API & Processing)
* **Matplotlib & Seaborn** (Visualization)
* **Pandas & NumPy** (Data Manipulation)

## 🖼️ Screenshots
<img width="1919" height="935" alt="Screenshot 2025-12-07 031044" src="https://github.com/user-attachments/assets/7eca13ac-cb37-4a50-888c-509d950f68a6" />
<img width="1919" height="936" alt="Screenshot 2025-12-07 031053" src="https://github.com/user-attachments/assets/723ab731-03ba-4395-9da1-e6c190871555" />
<img width="1252" height="1318" alt="b1765bcdcb5f999d48a6c797863bbc22c1ae8da0c012126acd1e1271" src="https://github.com/user-attachments/assets/b6934903-550c-4a07-a43a-092ee48e7d79" />
<img width="1918" height="821" alt="image" src="https://github.com/user-attachments/assets/6a17a527-e509-4dcb-b785-4ec637c49a75" />

## 📦 How to Run Locally

1. Clone the repository
   ```bash
   git clone https://github.com/av-04/F1_telemetry.git
   cd F1_telemetry
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies
   - If there's a requirements file:
     ```bash
     pip install -r requirements.txt
     ```
   - Or install the main packages directly:
     ```bash
     pip install fastf1 streamlit matplotlib seaborn pandas numpy
     ```

4. Configure FastF1 cache (recommended)
   - FastF1 caches session data to avoid repeated downloads. You can enable/point the cache in code:
     ```python
     import fastf1
     fastf1.Cache.enable_cache('path/to/ff1_cache')  # create a cache directory
     ```
   - Or set an environment variable for a consistent cache location:
     ```bash
     export FASTF1_CACHE=/path/to/ff1_cache  # macOS / Linux
     setx FASTF1_CACHE "C:\path\to\ff1_cache"  # Windows (persisted)
     ```
   - Note: caching will speed up repeated runs and reduce network usage.

5. Run the app
   - Typical Streamlit command (replace `app.py` with the actual entrypoint if different, e.g. `streamlit_app.py` or `main.py`):
     ```bash
     streamlit run app.py
     ```
   - To set a custom port:
     ```bash
     streamlit run app.py --server.port 8501
     ```

6. Example usage
   - Open http://localhost:8501 in your browser after Streamlit starts.
   - Select season, race, and drivers from the UI to load telemetry and visualizations.
   - Use the comparison and delta tools to inspect time gains/losses and corner behavior.

## ⚠️ Common Issues & Troubleshooting
* FastF1 data loading errors:
  - Ensure you have internet access for initial downloads.
  - If a session fails to load, try a different session or verify the season/year is supported by FastF1.
  - Update FastF1 if you encounter compatibility issues: `pip install -U fastf1`
* Streamlit not starting:
  - Make sure your virtual environment is activated and dependencies installed.
  - Check for port conflicts; change the port with `--server.port`.
* Visualization scaling/overlap:
  - If labels overlap on small screens, expand the browser width or save figures to inspect.

## Contributing
Contributions are welcome! Please open an issue for discussion or submit a pull request with:
1. A clear description of the change.
2. Tests (if applicable) or screenshots for UI changes.
3. Updated docs or README entries for new features.




