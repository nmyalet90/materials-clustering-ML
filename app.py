# Basic app structure
import streamlit as st
import pandas as pd

st.title("🔬 Materials Clustering Explorer")
st.write("Interactive exploration of materials using Machine Learning")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/materials_clustering.csv")
    return df

df = load_data()

# Prepare data
# Cluster labels

# df["cluster_label"] = df["cluster"].apply(lambda x: f"Cluster {x+1}")

# Sidebar filters
st.sidebar.header("Filters")

# Search bar
search = st.sidebar.text_input("🔍 Search material (formula)")

# Band gap
bg_min, bg_max = float(df["band_gap"].min()), float(df["band_gap"].max())
band_gap = st.sidebar.slider("Band Gap (eV)", bg_min, bg_max, (bg_min, bg_max))

# Density
d_min, d_max = float(df["density"].min()), float(df["density"].max())
density = st.sidebar.slider("Density", d_min, d_max, (d_min, d_max))

# Cluster
clusters = st.sidebar.multiselect(
    "Cluster",
    options=sorted(df["cluster_label"].unique()),
    default=sorted(df["cluster_label"].unique())
)

# Apply filters
filtered_df = df[
    (df["band_gap"] >= band_gap[0]) &
    (df["band_gap"] <= band_gap[1]) &
    (df["density"] >= density[0]) &
    (df["density"] <= density[1]) &
    (df["cluster_label"].isin(clusters))
]

# Search filter
if search:
    filtered_df = filtered_df[
        filtered_df["formula_pretty"].str.contains(search, case=False, na=False)
    ]

# Highlight search
filtered_df["highlight"] = filtered_df["formula_pretty"].str.contains(
    search, case=False, na=False
)

# Plot
import plotly.express as px

fig = px.scatter(
    filtered_df,
    x="pca1",
    y="pca2",
    color="cluster_label",
    size=filtered_df["highlight"].map({True: 12, False: 6}),
    hover_name="formula_pretty",
    hover_data=["band_gap", "density"],
    title="Materials Clustering (PCA Projection)"
)

st.plotly_chart(fig, use_container_width=True)

# Metrics
st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Materials", len(filtered_df))
col2.metric("Avg Band Gap", round(filtered_df["band_gap"].mean(), 2))
col3.metric("Avg Density", round(filtered_df["density"].mean(), 2))

# Data table
st.subheader("📋 Filtered Data")

st.dataframe(
    filtered_df[[
        "formula_pretty",
        "band_gap",
        "density",
        "cluster_label"
    ]].head(100)
)

# Final polish
st.set_page_config(
    page_title="Materials ML Explorer",
    layout="wide"
)

