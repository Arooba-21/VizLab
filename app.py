import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt   

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Data Visualization Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ GLOBAL CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #eaeaea;
}

.block-container {
    padding-top: 2rem;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 600;
}

.page-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #9aa0a6;
    margin-bottom: 25px;
}

.card {
    background: #161b22;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #232a35;
}

.small-text {
    color: #9aa0a6;
}

hr {
    border: 0.5px solid #232a35;
}

/* ---------- BUTTON POLISH ---------- */
div.stButton > button:first-child {
    background-color: #6a6a6a;
    color: #0f172a;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    font-weight: 600;
}

div.stButton > button:first-child:hover {
    background-color: #6a6a6a;
    color: #020617;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "Home",
        "Dataset Overview",
        "Chart Recommendation Engine",
        "Interactive Visuals (Plotly)",
        "Matplotlib (Foundations)",
        "Seaborn (Statistical Insights)",
        "Library Comparison",
        "Export & Summary"
    ]
)

# ------------------ HOME PAGE ------------------
if page == "Home":
    st.markdown("<div class='page-title'>Data Visualization Studio</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h4>Project Overview</h4>
        <p class="small-text">
        A guided platform for learning and applying data visualization using
        Plotly, Matplotlib, and Seaborn.
        </p>
        <ul class="small-text">
            <li>Understand data before visualizing</li>
            <li>Get smart chart recommendations</li>
            <li>Explore interactive and static charts</li>
            <li>Compare visualization libraries</li>
            <li>Export report-ready visuals</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------ DATASET OVERVIEW ------------------
elif page == "Dataset Overview":
    st.markdown("<div class='page-title'>Dataset Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Upload and understand your dataset</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        st.markdown("""
        <div class="card">
            <h4>Dataset Summary</h4>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Numeric Columns", len(numeric_cols))

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'><h4>Data Preview (Head)</h4>", unsafe_allow_html=True)
            st.dataframe(df.head())
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'><h4>Data Preview (Tail)</h4>", unsafe_allow_html=True)
            st.dataframe(df.tail())
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h4>Column Types</h4>
            <p class="small-text">
            Numeric columns are best for trends, correlation, and distributions.
            Categorical columns are useful for comparison and grouping.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Please upload a CSV file to continue.")

# ------------------ PLACEHOLDER PAGES ------------------
elif page == "Chart Recommendation Engine":
    st.markdown("<div class='page-title'>Chart Recommendation Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Choose the right chart based on your data</div>", unsafe_allow_html=True)

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first from the Dataset Overview page.")
    else:
        df = st.session_state["df"]

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        all_cols = df.columns.tolist()

   

        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("Select X-axis column", all_cols)
        with col2:
            y_col = st.selectbox("Select Y-axis column (optional)", ["None"] + all_cols)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ------------------ RECOMMENDATION LOGIC ------------------
        recommendations = []

        x_type = "numeric" if x_col in numeric_cols else "categorical"
        y_type = None
        if y_col != "None":
            y_type = "numeric" if y_col in numeric_cols else "categorical"

        # Numeric vs Numeric
        if x_type == "numeric" and y_type == "numeric":
            recommendations = [
                ("Scatter Plot", "Shows relationship between two numeric variables.",
                 "Avoid when data has strong time order."),
                ("Line Chart", "Useful if one variable represents time or sequence.",
                 "Not ideal for unordered numeric data."),
                ("Density Plot", "Helps understand data concentration.",
                 "Avoid for small datasets."),
                ("Correlation Heatmap", "Shows strength of relationship.",
                 "Not meaningful with very few observations.")
            ]

        # Categorical vs Numeric
        elif (x_type == "categorical" and y_type == "numeric") or (x_type == "numeric" and y_type == "categorical"):
            recommendations = [
                ("Bar Chart", "Compares numeric values across categories.",
                 "Avoid when too many categories."),
                ("Box Plot", "Shows distribution and outliers.",
                 "Not ideal for small samples."),
                ("Violin Plot", "Shows distribution shape.",
                 "May confuse non-technical users.")
            ]

        # Single Numeric
        elif x_type == "numeric" and y_col == "None":
            recommendations = [
                ("Histogram", "Shows distribution of values.",
                 "Bin size can mislead interpretation."),
                ("Density Plot", "Smooth distribution estimation.",
                 "Avoid for very small datasets.")
            ]

        # Single Categorical
        elif x_type == "categorical" and y_col == "None":
            recommendations = [
                ("Bar Chart", "Shows frequency of categories.",
                 "Avoid when categories are too many."),
                ("Pie Chart", "Shows proportion of categories.",
                 "Not good for precise comparisons.")
            ]

        else:
            recommendations = [
                ("Table View", "Best for mixed or unclear data.",
                 "Visualization may not add value here.")
            ]

        # ------------------ DISPLAY RECOMMENDATIONS ------------------
        
        st.markdown("<h4>Recommended Charts</h4>", unsafe_allow_html=True)

        for chart, reason, caution in recommendations:
            st.markdown(f"""
            <b>{chart}</b><br>
            <span class="small-text">
            Why: {reason}<br>
            When not to use: {caution}
            </span>
            <hr>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


 # ------------------ INTERACTIVE VISUAL ------------------
    st.info(
    "Select a chart category, choose one chart type, then provide required columns. "
    "Only one chart is generated at a time to keep analysis clear."
)

elif page == "Interactive Visuals (Plotly)":
    st.markdown("<div class='page-title'>Interactive Visuals (Plotly)</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Explore data using interactive charts</div>", unsafe_allow_html=True)

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        df = st.session_state["df"]

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        all_cols = df.columns.tolist()

        chart_category = st.selectbox(
            "Chart Category",
            ["Basic", "Statistical", "Hierarchical", "Advanced", "Financial"]
        )

        chart_map = {
    "Basic": ["Line", "Bar", "Scatter", "Bubble", "Area"],
    "Statistical": [
        "Histogram", "Box", "Violin", "Strip",
        "Density Contour", "Density Heatmap",
        "Scatter Matrix", "Parallel Coordinates"
    ],
    "Hierarchical": ["Pie", "Tree Map", "Sunburst", "Funnel"],
    "Maps": ["Scatter Map", "Choropleth Map"],
    "Advanced": ["3D Scatter", "Facet Scatter", "Heatmap"],
    "Financial": ["Candlestick", "Waterfall"]
}


        chart_type = st.selectbox("Chart Type", chart_map[chart_category])

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


        # -------- COLUMN SELECTION --------
        if chart_type in ["Line", "Bar", "Scatter", "Area"]:
            x = st.selectbox("X-axis", all_cols)
            y = st.selectbox("Y-axis", numeric_cols)

        elif chart_type == "Bubble":
            x = st.selectbox("X-axis", all_cols)
            y = st.selectbox("Y-axis", numeric_cols)
            size = st.selectbox("Bubble Size", numeric_cols)

        elif chart_type == "Histogram":
            x = st.selectbox("Column", numeric_cols)

        elif chart_type in ["Box", "Violin", "Strip"]:
            x = st.selectbox("Category", categorical_cols)
            y = st.selectbox("Value", numeric_cols)

        elif chart_type in ["Density Contour", "Density Heatmap", "Heatmap"]:
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)

        elif chart_type == "Scatter Matrix":
            dims = st.multiselect("Dimensions", numeric_cols, default=numeric_cols[:4])

        elif chart_type == "Parallel Coordinates":
            color = st.selectbox("Color", numeric_cols)

        elif chart_type in ["Pie", "Funnel"]:
            names = st.selectbox("Category", categorical_cols)
            values = st.selectbox("Values", numeric_cols)

        elif chart_type == "Scatter Map":
            lat = st.selectbox("Latitude", numeric_cols)
            lon = st.selectbox("Longitude", numeric_cols)
            color = st.selectbox("Color (optional)", ["None"] + numeric_cols)

        elif chart_type == "Choropleth Map":
            location = st.selectbox("Location Column (Country/State)", categorical_cols)
            value = st.selectbox("Value Column", numeric_cols)

        elif chart_type in ["Tree Map", "Sunburst"]:
            path = st.multiselect("Hierarchy", categorical_cols, default=categorical_cols[:2])
            values = st.selectbox("Values", numeric_cols)

        elif chart_type == "3D Scatter":
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)
            z = st.selectbox("Z-axis", numeric_cols)

        elif chart_type in ["Facet Scatter", "Facet Animated Scatter"]:
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)
            color = st.selectbox("Color", categorical_cols)
            facet = st.selectbox("Facet Column", categorical_cols)

        elif chart_type == "Candlestick":
            x = st.selectbox("Time", all_cols)
            open_ = st.selectbox("Open", numeric_cols)
            high = st.selectbox("High", numeric_cols)
            low = st.selectbox("Low", numeric_cols)
            close = st.selectbox("Close", numeric_cols)

        elif chart_type == "Waterfall":
            x = st.selectbox("Category", all_cols)
            y = st.selectbox("Values", numeric_cols)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        generate = st.button("Generate Chart", type="primary")
        if generate:

            if chart_type == "Line":
                fig = px.line(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Bar":
                fig = px.bar(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Bubble":
                fig = px.scatter(df, x=x, y=y, size=size)
                st.session_state["last_plot"] = fig

            elif chart_type == "Area":
                fig = px.area(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x)
                st.session_state["last_plot"] = fig

            elif chart_type == "Box":
                fig = px.box(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Violin":
                fig = px.violin(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Strip":
                fig = px.strip(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Density Contour":
                fig = px.density_contour(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Density Heatmap":
                fig = px.density_heatmap(df, x=x, y=y)
                st.session_state["last_plot"] = fig

            elif chart_type == "Scatter Matrix":
                fig = px.scatter_matrix(df, dimensions=dims)
                st.session_state["last_plot"] = fig

            elif chart_type == "Parallel Coordinates":
                fig = px.parallel_coordinates(df, color=color)
                st.session_state["last_plot"] = fig

            elif chart_type == "Pie":
                fig = px.pie(df, names=names, values=values)
                st.session_state["last_plot"] = fig

            elif chart_type == "Funnel":
                fig = px.funnel(df, x=values, y=names)
                st.session_state["last_plot"] = fig

            elif chart_type == "Tree Map":
                fig = px.treemap(df, path=path, values=values)
                st.session_state["last_plot"] = fig

            elif chart_type == "Sunburst":
                fig = px.sunburst(df, path=path, values=values)
                st.session_state["last_plot"] = fig

            elif chart_type == "3D Scatter":
                fig = px.scatter_3d(df, x=x, y=y, z=z)
                st.session_state["last_plot"] = fig

            elif chart_type == "Facet Scatter":
                fig = px.scatter(df, x=x, y=y, color=color, facet_col=facet)
                st.session_state["last_plot"] = fig

            elif chart_type == "Heatmap":
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr)
                st.session_state["last_plot"] = fig

            elif chart_type == "Candlestick":
                fig = go.Figure(data=[go.Candlestick(
                    x=df[x],
                    open=df[open_],
                    high=df[high],
                    low=df[low],
                    close=df[close]
                )])
                st.session_state["last_plot"] = fig


            elif chart_type == "Scatter Map":
                fig = px.scatter_mapbox(
                    df,
                    lat=lat,
                    lon=lon,
                    color=None if color == "None" else color,
                    zoom=1,
                    height=550
                  )
                fig.update_layout(mapbox_style="open-street-map")
                st.session_state["last_plot"] = fig

            elif chart_type == "Choropleth Map":
                fig = px.choropleth(
                df,
                locations=location,
                locationmode="country names",
                color=value
                 )
                st.session_state["last_plot"] = fig

            elif chart_type == "Waterfall":
                fig = go.Figure(go.Waterfall(x=df[x], y=df[y]))
                st.session_state["last_plot"] = fig

            st.plotly_chart(fig, use_container_width=True)

        # -------- MATPLOTLIB SECTION --------
elif page == "Matplotlib (Foundations)":
    st.markdown("<div class='page-title'>Matplotlib Foundations</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Learn basic plotting concepts using Matplotlib</div>", unsafe_allow_html=True)

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        st.info("Matplotlib is best for static, publication-ready charts.")

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Line", "Bar", "Histogram", "Scatter", "Pie"]
        )

        if chart_type == "Line":
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)

        elif chart_type == "Bar":
            x = st.selectbox("Category", categorical_cols)
            y = st.selectbox("Values", numeric_cols)

        elif chart_type == "Histogram":
            x = st.selectbox("Column", numeric_cols)

        elif chart_type == "Scatter":
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", numeric_cols)

        elif chart_type == "Pie":
            x = st.selectbox("Category", categorical_cols)
            y = st.selectbox("Values", numeric_cols)

        with st.expander("Chart Size Settings"):
            width = st.slider("Width", 1, 10, 2)
            height = st.slider("Height", 1, 10, 3)


        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Generate Matplotlib Chart", type="primary"):
            fig, ax = plt.subplots(figsize=(width, height),dpi=80)

            if chart_type == "Line":
               ax.plot(df[x], df[y])
               ax.set_xlabel(x)
               ax.set_ylabel(y)

            elif chart_type == "Bar":
               grouped = df.groupby(x)[y].mean()
               ax.bar(grouped.index, grouped.values)

            elif chart_type == "Histogram":
               ax.hist(df[x], bins=20)

            elif chart_type == "Scatter":
               ax.scatter(df[x], df[y])

            elif chart_type == "Pie":
               grouped = df.groupby(x)[y].sum()
               ax.pie(grouped.values, labels=grouped.index, autopct="%1.1f%%")

            st.session_state["last_plot"] = fig
            st.session_state["plot_lib"] = "matplotlib"

            st.pyplot(fig, use_container_width=False)
        
        # -------- SEABORN SECTION --------
elif page == "Seaborn (Statistical Insights)":
    st.markdown("<div class='page-title'>Seaborn Statistical Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Explore distributions and relationships</div>", unsafe_allow_html=True)

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        st.info("Seaborn is ideal for statistical exploration and pattern detection.")

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Count Plot", "Box Plot", "Violin Plot", "Pair Plot", "Correlation Heatmap"]
        )

        if chart_type == "Count Plot":
            x = st.selectbox("Category", categorical_cols)

        elif chart_type in ["Box Plot", "Violin Plot"]:
            x = st.selectbox("Category", categorical_cols)
            y = st.selectbox("Numeric Value", numeric_cols)

        elif chart_type == "Pair Plot":
            cols = st.multiselect("Select Numeric Columns", numeric_cols, default=numeric_cols[:4])

        elif chart_type == "Correlation Heatmap":
            cols = st.multiselect("Select Numeric Columns", numeric_cols, default=numeric_cols)

        with st.expander("Chart Size Settings"):
            width = st.slider("Width", 1, 10, 2)
            height = st.slider("Height", 1, 10, 3)

        # ---------------------------------
        # SAFE DEFAULT
        fig = None

        # ---------------------------------
        if st.button("Generate Seaborn Chart", type="primary"):

            if chart_type == "Count Plot":
                fig, ax = plt.subplots(figsize=(width, height),dpi=80)
                sns.countplot(data=df, x=x, ax=ax)

            elif chart_type == "Box Plot":
                fig, ax = plt.subplots(figsize=(width, height),dpi=80)
                sns.boxplot(data=df, x=x, y=y, ax=ax)

            elif chart_type == "Violin Plot":
                fig, ax = plt.subplots(figsize=(width, height),dpi=80)
                sns.violinplot(data=df, x=x, y=y, ax=ax)

            elif chart_type == "Pair Plot":
                pair = sns.pairplot(df[cols])
                st.session_state["last_plot"] = pair.fig
                st.session_state["plot_lib"] = "seaborn"
                st.pyplot(pair.fig)
                st.stop()

            elif chart_type == "Correlation Heatmap":
                fig, ax = plt.subplots(figsize=(width, height),dpi=80)
                corr = df[cols].corr()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

        # ---------------------------------
        # DISPLAY + SAVE
        if fig is not None:
            st.session_state["last_plot"] = fig
            st.session_state["plot_lib"] = "seaborn"
            st.pyplot(fig, use_container_width=False)

#-------LIBRARY COMPARISON---------

elif page == "Library Comparison":
    st.markdown("<div class='page-title'>Visualization Library Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Choosing the right tool for the job</div>", unsafe_allow_html=True)

    st.markdown("""
    <h4>Quick Comparison</h4>

    | Feature | Plotly | Matplotlib | Seaborn |
    |------|--------|------------|---------|
    | Interactivity | High | None | Low |
    | Learning Curve | Medium | Steep | Easy |
    | Customization | High | Very High | Medium |
    | Performance | Medium | High | Medium |
    | Statistical Support | Medium | Low | High |
    | Best Use Case | Dashboards | Publications | Analysis |
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <h4>Plotly</h4>
        <ul>
            <li>Interactive dashboards</li>
            <li>Hover, zoom, animations</li>
            <li>Best for web apps</li>
        </ul>
        <b>Avoid when:</b> Static academic papers
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <h4>Matplotlib</h4>
        <ul>
            <li>Complete control over visuals</li>
            <li>Publication-ready plots</li>
            <li>Industry standard</li>
        </ul>
        <b>Avoid when:</b> Interactivity is required
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <h4>Seaborn</h4>
        <ul>
            <li>Statistical visualization</li>
            <li>Quick insights</li>
            <li>Beautiful defaults</li>
        </ul>
        <b>Avoid when:</b> Heavy customization needed
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h4>Final Recommendation</h4>
    <ul>
        <li><b>Exploration:</b> Seaborn</li>
        <li><b>Reporting:</b> Matplotlib</li>
        <li><b>Dashboards:</b> Plotly</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ FINAL STEP ------------------

elif page == "Export & Summary":
    st.markdown("<div class='page-title'>Export & Summary</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Finalize insights and export results</div>", unsafe_allow_html=True)

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
    else:
        df = st.session_state["df"]

        # ------------------ DATASET SUMMARY ------------------
        st.markdown("<h4>Dataset Overview</h4>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isnull().sum().sum()))

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ------------------ NUMERIC SUMMARY ------------------
        st.markdown("<h4>Numeric Summary</h4>", unsafe_allow_html=True)
        st.dataframe(df.describe(), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ------------------ EXPORT SECTION -----------------
        st.markdown("<h4>Export Charts</h4>", unsafe_allow_html=True)

        st.info("Plot exports work for the most recently generated chart.")

        export_type = st.selectbox(
            "Select Export Format",
            ["PNG"]
        )

        if "last_plot" in st.session_state:
          fig = st.session_state["last_plot"]
          lib = st.session_state.get("plot_lib", "")

          if lib in ["matplotlib", "seaborn"]:
           import io

           buf = io.BytesIO()
           fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
           buf.seek(0)

           st.download_button(
               label="Download Chart (PNG)",
               data=buf,
               file_name="chart.png",
               mime="image/png"
        )

          elif lib == "plotly":
           st.info("Plotly export handled separately")

        else:
          st.warning("No chart available to export.")


        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ------------------ INSIGHTS ------------------
        st.markdown("<h4>Analyst Notes</h4>", unsafe_allow_html=True)

        notes = st.text_area(
            "Write your insights or conclusions here:",
            height=150
        )

        if st.button("Save Notes"):
            st.session_state["notes"] = notes
            st.success("Insights saved.")

        if "notes" in st.session_state:
            st.markdown("### Saved Insights")
            st.write(st.session_state["notes"])

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ------------------ FINAL SUMMARY ------------------
        st.markdown("""
        <h4>Project Completion</h4>
        <p>
        This visualization studio demonstrates end-to-end data analysis:
        understanding data, choosing appropriate charts, generating visuals,
        and summarizing insights.
        </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
