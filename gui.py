import os
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import streamlit as st

from src.parsinator import Parsinator
from src.readinator import Readinator


st.set_page_config(
    page_title="Carbonara",
    page_icon="🍝",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.write("# 📁 Select source files")
experiment_output = st.sidebar.selectbox("Experiment output", os.listdir("output"))
powergadget_output = st.sidebar.selectbox("PowerGadget output", os.listdir("powerlogz"))

st.sidebar.warning("*If there is no PowerGadget output, it might be saved in the wrong folder. Drag the results into this folder:*")
powerlogz_location_expander = st.sidebar.beta_expander("Powerlogz folder location", expanded=False)
powerlogz_location_expander.write("```" + os.path.abspath("powerlogz") + "```")

st.write("# Carbonara")
st.write("## Visualisation of experiments")

view = st.empty()
results_loaded = False
results = {}

p = Parsinator(experiment_log_path=experiment_output, powerlogz_log_path=powergadget_output)

# Create a button in the sidebar that when clicked runs the parsing
st.sidebar.write("## 📝 Parse files")
st.sidebar.write("*Parse the selected files and create a CSV file with the results*")
if st.sidebar.button("Parse"):
    p.run()

# Create a button in the sidebar that when clicked runs the parsing
st.sidebar.write("## 📊 Visualize results")
st.sidebar.write("*Select the result and visualize it*")
result_output = st.sidebar.selectbox("Results", os.listdir("results"))
if st.sidebar.button("Visualize"):
    r = Readinator(result_output)
    r.reader()
    results = r.data_dict
    results_loaded = True

if not results_loaded:
    view.error("Please refer to the sidebar to visualize any experiment results.")
else:
    experiments = results.keys()
    
    st.write("### Raw results")
    raw_expanders = {experiment : st.beta_expander('Experiment: ' + experiment) for experiment in experiments}
    for experiment in experiments:
        raw_expanders[experiment].write(results[experiment])
    
    st.write("### Graphs")
    graph_expanders = {experiment : st.beta_expander('Experiment: ' + experiment) for experiment in experiments}
    for experiment in experiments:

        # Group data together
        data = [[float(val) for val in package_values] for package_values in results[experiment].values()]
        labels = [package_name for package_name in results[experiment].keys()]
        
        # Create dataframe to use with Plotly
        df = pd.DataFrame()
        for col_name, col_values in results[experiment].items():
            df[col_name] = pd.Series([float(col_value) for col_value in col_values])
        df.fillna(0, inplace=True)
        
        # Scatter plot
        fig = px.scatter(
            df, 
            x=df.index,
            y=df.columns,
            title="Energy consumption per iteration")
        fig.update_layout(
            xaxis_title="Iteration",
            yaxis_title="Energy consumption (J)"
        )
        fig.update_traces(
            marker=dict(
                size=12,
                line=dict(
                    width=2,
                    color='DarkSlateGrey'
                )
            ),
            selector=dict(mode='markers')
        )
        graph_expanders[experiment].plotly_chart(fig)
        
        # Violin plot
        fig2 = px.violin(df, title="Violin plot of energy consumption")
        fig2.update_layout(
            xaxis_title="Package",
            yaxis_title="Energy consumption (J)"
        )
        graph_expanders[experiment].plotly_chart(fig2)
