import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tittel
st.title("Sykefraværskostnader i virksomheten")

# Dummydata for sykefravær (kan erstattes med faktiske data)
data = {
    "Avdeling": ["Salg", "IT", "HR", "Produksjon", "Logistikk"],
    "Antall ansatte": [30, 25, 10, 50, 40],
    "Gj.snittslønn (kr)": [650000, 700000, 600000, 550000, 500000],
    "Sykefravær (%)": [5.2, 4.8, 3.5, 6.0, 7.2],
}

df = pd.DataFrame(data)

# Vis tabellen med sykefraværsdata
st.subheader("Sykefraværsdata per avdeling")
st.dataframe(df)

# Beregninger av kostnader
arbeidsdager_per_aar = 260
arbeidsgiverperiode = 16
df["Direkte lønnskostnad (kr)"] = (
    df["Gj.snittslønn (kr)"] * (df["Sykefravær (%)"] / 100) * (arbeidsgiverperiode / arbeidsdager_per_aar)
)
df["Sosiale avgifter (kr)"] = df["Direkte lønnskostnad (kr)"] * 1.14
df["Indirekte kostnader (kr)"] = df["Direkte lønnskostnad (kr)"] * 0.5
df["Total sykefraværskostnad per ansatt (kr)"] = df["Sosiale avgifter (kr)"] + df["Indirekte kostnader (kr)"]
df["Total sykefraværskostnad per avdeling (kr)"] = df["Total sykefraværskostnad per ansatt (kr)"] * df["Antall ansatte"]

# Vis tabellen med beregninger
st.subheader("Beregnet sykefraværskostnad per avdeling")
st.dataframe(df)

# Diagram: Totale sykefraværskostnader per avdeling
st.subheader("Totale sykefraværskostnader per avdeling")
fig, ax = plt.subplots()
ax.bar(df["Avdeling"], df["Total sykefraværskostnad per avdeling (kr)"])
ax.set_xlabel("Avdeling")
ax.set_ylabel("Kostnad (kr)")
ax.set_title("Totale sykefraværskostnader per avdeling")
st.pyplot(fig)

# Pie chart for kostnadsfordeling
st.subheader("Kostnadsfordeling for sykefravær")
selected_avdeling = st.selectbox("Velg avdeling", df["Avdeling"])
selected_data = df[df["Avdeling"] == selected_avdeling]

fig, ax = plt.subplots()
ax.pie(
    [selected_data["Direkte lønnskostnad (kr)"].values[0], selected_data["Indirekte kostnader (kr)"].values[0]],
    labels=["Direkte kostnader", "Indirekte kostnader"],
    autopct="%1.1f%%",
    startangle=90,
)
ax.set_title(f"Kostnadsfordeling - {selected_avdeling}")
st.pyplot(fig)
