import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def analyze_driving_style(tel_d1, tel_d2):
    try:
        f_d1 = tel_d1[["Speed", "Throttle", "Brake"]].fillna(0)
        f_d2 = tel_d2[["Speed", "Throttle", "Brake"]].fillna(0)
        comb_feat = pd.concat([f_d1, f_d2])
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(comb_feat)
        labels_d1 = kmeans.predict(f_d1)
        labels_d2 = kmeans.predict(f_d2)

        def lap_state(labels):
            count = np.bincount(labels, minlength=3)
            return (count / len(labels)) * 100

        perc_d1 = lap_state(labels_d1)
        perc_d2 = lap_state(labels_d2)
        return perc_d1, perc_d2
    except Exception as e:
        print(f"Error in analyze_driving_style: {e}")
        return None, None
