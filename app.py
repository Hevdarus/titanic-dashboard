# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


def filter_dataframe(df, sexes, pclasses, agegroups):
    filtered_df = df[
        (df["Sex"].isin(sexes)) &
        (df["Pclass"].isin(pclasses)) &
        (df["AgeGroup"].isin(agegroups))
    ]
    return filtered_df


app = Dash()

df = pd.read_csv("processed_data.csv")

app.layout = html.Div(
    children=[
        # Title
        html.H1(
            "Titanic Survival Analysis Dashboard",
            style={"textAlign": "center"}
        ),

        html.P(
            "Interactive analytical dashboard exploring factors influencing passenger survival on the Titanic.",
            style={"textAlign": "center"}
        ),

        html.Hr(),

        # --------------------
        # Filters section
        # --------------------
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label("Sex"),
                        dcc.Dropdown(
                            id="sex-filter",
                            options=[
                                {"label": sex, "value": sex}
                                for sex in sorted(df["Sex"].unique())
                            ],
                            value=df["Sex"].unique().tolist(),
                            multi=True
                        ),
                    ],
                    className="filter",
                ),

                html.Div(
                    children=[
                        html.Label("Passenger Class"),
                        dcc.Dropdown(
                            id="pclass-filter",
                            options=[
                                {"label": f"Class {c}", "value": c}
                                for c in sorted(df["Pclass"].unique())
                            ],
                            value=df["Pclass"].unique().tolist(),
                            multi=True
                        ),
                    ],
                    className="filter",
                ),

                html.Div(
                    children=[
                        html.Label("Age Group"),
                        dcc.Dropdown(
                            id="agegroup-filter",
                            options=[
                                {"label": ag, "value": ag}
                                for ag in df["AgeGroup"].dropna().unique()
                            ],
                            value=df["AgeGroup"].dropna().unique().tolist(),
                            multi=True
                        ),
                    ],
                    className="filter",
                ),
            ],
            className="filters",
        ),

        html.Hr(),

        # --------------------
        # Charts section
        # --------------------
        html.Div(
            children=[
                html.Div(dcc.Graph(id="survival-by-sex"), className="card"),
                html.Div(dcc.Graph(id="survival-heatmap"), className="card"),
            ],
            className="row"
        ),

        html.Div(
            children=[
                html.Div(dcc.Graph(id="age-violin"), className="card"),
                html.Div(dcc.Graph(id="fare-distribution"), className="card"),
            ],
            className="row"
        ),

        html.Div(
            children=[
                html.Div(dcc.Graph(id="age-fare-scatter"), className="card"),
                html.Div(dcc.Graph(id="cabin-treemap"), className="card"),
            ],
            className="row"
        ),
    ],
    style={
        "margin": "5em auto"
    }
)


@app.callback(
    Output("survival-by-sex", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_survival_by_sex(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    # Aggregation
    agg_df = (
        filtered_df
        .groupby(["Sex", "SurvivedLabel"])
        .size()
        .reset_index(name="Count")
    )

    # Total per sex
    totals = (
        filtered_df
        .groupby("Sex")
        .size()
        .reset_index(name="Total")
    )

    # Merge totals back
    agg_df = agg_df.merge(totals, on="Sex")

    fig = px.bar(
        agg_df,
        x="Sex",
        y="Count",
        color="SurvivedLabel",
        barmode="stack",
        custom_data=["Total", "SurvivedLabel"],
        title="Survival by Sex"
    )

    fig.update_traces(
        hovertemplate=
        "<b>Sex:</b> %{x}<br>" +
        "<b>%{customdata[1]}:</b> %{y}<br>" +
        "<b>Total:</b> %{customdata[0]}<extra></extra>"
    )

    fig.update_layout(
        legend_title_text="Survival Status"
    )

    return fig


@app.callback(
    Output("fare-distribution", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_fare_distribution(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    fig = px.box(
        filtered_df,
        x="SurvivedLabel",
        y="Fare",
        color="SurvivedLabel",
        title="Comparison of Ticket Fares for Survivors vs Non-Survivors",
        labels={
            "SurvivedLabel": "Survival Status",
            "Fare": "Ticket Fare"
        }
    )

    fig.update_traces(
        hovertemplate=
        "<b>Status:</b> %{x}<br>" +
        "<b>Fare:</b> %{y:.2f}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        transition_duration=300
    )

    return fig


@app.callback(
    Output("survival-heatmap", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_survival_heatmap(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    # Survival rate számítása
    heatmap_df = (
        filtered_df
        .groupby(["Sex", "Pclass"])["Survived"]
        .mean()
        .reset_index()
    )

    # Pivot -> 2x3 mátrix
    pivot_df = heatmap_df.pivot(
        index="Sex",
        columns="Pclass",
        values="Survived"
    )

    fig = px.imshow(
        pivot_df,
        text_auto=".2f",
        color_continuous_scale="Viridis",
        aspect="auto",
        labels=dict(
            x="Passenger Class",
            y="Sex",
            color="Survival Rate"
        ),
        title="Survival Rate Across Sex and Passenger Class"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[1, 2, 3],
        ticktext=["1", "2", "3"],
        range=[0.5, 3.5]
    )

    fig.update_layout(
        transition_duration=300
    )

    return fig


@app.callback(
    Output("age-fare-scatter", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_age_fare_scatter(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    fig = px.scatter(
        filtered_df,
        x="Age",
        y="Fare",
        color="SurvivedLabel",
        trendline="ols",
        opacity=0.6,
        title="Relationship Between Passenger Age and Ticket Fare by Survival Outcome",
        custom_data=["SurvivedLabel"]
    )

    fig.update_traces(
        hovertemplate=
            "<b>Age:</b> %{x}<br>" +
            "<b>Fare:</b> %{y:.2f}<extra></extra>"
    )

    fig.update_layout(
        transition_duration=300
    )

    return fig


@app.callback(
    Output("age-violin", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_age_violin(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    fig = px.violin(
        filtered_df,
        x="SurvivedLabel",
        y="Age",
        color="SurvivedLabel",
        box=True,
        points="outliers",
        title="Passenger Age Distribution for Survivors and Non-Survivors",
        labels={
            "SurvivedLabel": "Survival Status",
            "Age": "Age"
        }
    )

    fig.update_traces(
        hovertemplate=
            "<b>Survival Status:</b> %{x}<br>" +
            "<b>Age:</b> %{y}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        transition_duration=300
    )

    return fig


@app.callback(
    Output("cabin-treemap", "figure"),
    Input("sex-filter", "value"),
    Input("pclass-filter", "value"),
    Input("agegroup-filter", "value"),
)
def update_cabin_treemap(sexes, pclasses, agegroups):
    filtered_df = filter_dataframe(df, sexes, pclasses, agegroups)

    filtered_df["PclassLabel"] = "Class " + filtered_df["Pclass"].astype(str)
    filtered_df["HasCabinLabel"] = filtered_df["HasCabin"].map({
        1: "Has Cabin",
        0: "No Cabin"
    })

    treemap_df = (
        filtered_df
        .groupby(["PclassLabel", "HasCabinLabel", "SurvivedLabel"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.treemap(
        treemap_df,
        path=["PclassLabel", "HasCabinLabel", "SurvivedLabel"],
        values="Count",
        color="SurvivedLabel",
        color_discrete_map={
            "Survived": "#EF553B",
            "Did not survive": "#636EFA"
        },
        title="Passenger Composition by Class, Cabin Availability, and Survival"
    )

    fig.update_traces(
        textinfo="label+percent parent",
        hovertemplate=
        "<b>%{label}</b><br>"+
        "Passengers: %{value}<br>" +
        "Share of parent: %{percentParent:.1%}<extra></extra>"
    )

    fig.update_layout(
        margin=dict(t=50, l=10, r=10, b=10)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)