import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Load Data ----------
cpi_gdp_df = pd.read_csv("cpi_gdp_df.csv")
r_and_d_gdp_summary = pd.read_csv("r_and_d_gdp_summary.csv")
excel_df = pd.read_excel("Model Evaluation.xlsx")

# Contingency Table Data
contingency_data = {
    "Variable": ["Gender", "Married", "Dependents", "Education", "Self_Employed", "Credit_History", "Area"],
    "p-value": [0.73915, 0.02961, 0.36887, 0.04310, 1.00000, 0.00000, 0.00214],
    "Significant": ["No", "Yes", "No", "Yes", "No", "Yes", "Yes"]
}
contingency_df = pd.DataFrame(contingency_data)

# ---------- Compute Unified Year Range ----------
common_start = cpi_gdp_df["start_year"].max()
common_end = cpi_gdp_df["end_year"].min()
common_years = common_end - common_start

top10_filtered = cpi_gdp_df.copy()
top10_filtered["CPI_AAGR_percent"] = (
    (top10_filtered["last_CPI"] / top10_filtered["first_CPI"])**(1 / common_years) - 1
) * 100
top10_filtered["GDP_AAGR_percent"] = (
    (top10_filtered["last_GDP"] / top10_filtered["first_GDP"])**(1 / common_years) - 1
) * 100

# ---------- Create Visualizations ----------
fig1 = px.scatter(
    cpi_gdp_df,
    x='CPI_AAGR_percent',
    y='GDP_AAGR_percent',
    text='Country',
    color='Country',
    size='num_years',
    size_max=60,
    title='CPI vs GDP Growth by Country',
    trendline="ols",
    labels={
        'CPI_AAGR_percent': 'CPI Average Annual Growth (%)',
        'GDP_AAGR_percent': 'GDP Average Annual Growth (%)'
    }
)
fig1.update_traces(textposition='top center')
fig1.update_layout(showlegend=False)

fig2 = px.scatter(
    top10_filtered,
    x="CPI_AAGR_percent",
    y="GDP_AAGR_percent",
    hover_name="Country",
    trendline="ols",
    title=f"CPI vs GDP Growth ({common_start}–{common_end}) by Country",
    labels={
        "CPI_AAGR_percent": "CPI Average Annual Growth (%)",
        "GDP_AAGR_percent": "GDP Average Annual Growth (%)"
    }
)
fig2.update_layout(
    xaxis=dict(zeroline=True, zerolinecolor='LightPink'),
    yaxis=dict(zeroline=True, zerolinecolor='LightBlue')
)

fig3 = px.bar(
    r_and_d_gdp_summary,
    x="Continent",
    y="Average GDP",
    color="R&D Category",
    barmode="group",
    title="Average GDP by R&D Spending Category Across Continents",
    labels={"Average GDP": "Mean GDP (USD)", "Country Count": "Number of Countries"},
    hover_data=["Country Count"],
    text="Country Count"
)
fig3.update_layout(yaxis_type="log")
fig3.update_traces(textposition='outside')

# ---------- App Layout ----------
st.set_page_config(page_title="Global Economic Visualizations", layout="wide")
st.title("🌍 Global Economic & Model Insights")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 CPI vs GDP Growth",
    "📈 CPI vs GDP (Unified Years)",
    "🧪 R&D Spending by Continent",
    "📋 Model Evaluation Table",
    "📑 Contingency Table"
])

# Tab 1
with tab1:
    st.header("CPI vs GDP Growth by Country")
    st.plotly_chart(fig1, use_container_width=True)

# Tab 2
with tab2:
    st.header(f"CPI vs GDP Growth ({common_start}–{common_end}) by Country")
    st.plotly_chart(fig2, use_container_width=True)

# Tab 3
with tab3:
    st.header("R&D Spending Categories Across Continents")
    st.plotly_chart(fig3, use_container_width=True)

# Tab 4 - Model Evaluation
with tab4:
    st.header("Model Evaluation Table")



    styled_excel = excel_df.style.format(precision=4)  
    st.dataframe(styled_excel, use_container_width=True)

# Tab 5 - Contingency Table
with tab5:
    st.header("Contingency Table (Chi-squared Tests)")
    styled_contingency = contingency_df.style.format({"p-value": "{:.5f}"})
    st.dataframe(styled_contingency, use_container_width=True)
