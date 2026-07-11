# -----------------------------------------------------------------------------
# Demo Dash app to visualize the Electricity Tariffs Costa Rica Kaggle Dataset
# (https://www.kaggle.com/datasets/slothkong/electricity-tariffs-costa-rica)
#
# NOTE: Inspired on community example (https://hellodash.pythonanywhere.com/)
# -----------------------------------------------------------------------------

from dash import Dash, dcc, html, Input, Output, ClientsideFunction, clientside_callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_ag_grid as dag
import pandas
import random
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Global variables
# -----------------------------------------------------------------------------

COLOR_MAPPING = {
    "CAR": 'rgb(95, 70, 144)',
    "CG": 'rgb(15, 133, 84)',
    "CL": 'rgb(29, 105, 150)',
    "CNFL": 'rgb(225, 124, 5)',
    "CS": 'rgb(115, 175, 72)',
    "ESPH": 'rgb(56, 166, 165)',
    "ICE": 'rgb(237, 173, 8)',
    "JASEC": 'rgb(204, 80, 62)'
}

SYMBOLS = (
        "circle",
        "square",
        "diamond",
        "cross",
        "x",
        "triangle-up",
        "triangle-down",
        "triangle-left",
        "triangle-right",
        "triangle-ne",
        "triangle-se",
        "triangle-sw",
        "triangle-nw",
        "pentagon",
        "hexagon",
        "hexagon2",
        "octagon",
        "star",
        "hexagram",
        "star-triangle-up",
        "star-triangle-down",
        "star-square",
        "star-diamond",
        "diamond-tall",
        "diamond-wide",
        "hourglass",
        "bowtie",
        "arrow",
        "arrow-wide"
    )

DASHES = ("dot", "dash", "longdash", "dashdot", "longdashdot")

BASELINES = ("Primeros", "Bloque 0", "a.")


df = pandas.read_csv("../../kaggle/input/datasets/slothkong/electricity-tariffs-costa-rica/electricity-tariffs-costa-rica.csv")
unique_years_months = sorted(df["annio_mes"].unique())
unique_distributors = df["distribuidor"].unique()
unique_tariff_types = df["tipo_de_tarifa"].unique()

load_figure_template(["sketchy", "sketchy_dark"])

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def choose_symbol_or_dash_or_width(tariff_block, selection_mode="symbols"):
    is_baseline = tariff_block.startswith(BASELINES[0]) or tariff_block.startswith(BASELINES[1]) or tariff_block.startswith(BASELINES[2])
    
    if selection_mode == "dashes" and is_baseline:
        return "solid"

    elif selection_mode == "dashes" and not is_baseline:
        return random.choice(DASHES)

    elif selection_mode == "symbols" and is_baseline:
        return None
    
    elif selection_mode == "symbols" and not is_baseline:
        return random.choice(SYMBOLS)

    elif selection_mode == "widths" and is_baseline:
        return 4
    
    elif selection_mode == "widths" and not is_baseline:
        return 1

    else:
        raise RuntimeError(f"Unexpected exception occurred. Got tariff_block: '{tariff_block}', selection_mode: '{selection_mode}'")

def plot_figure(dataframe, template=None):
    fig = go.Figure()

    for distributor in dataframe["distribuidor"].unique():
        distributor_mask = (dataframe["distribuidor"] == distributor)
        
        for tariff_type in dataframe[distributor_mask]["tipo_de_tarifa"].unique():
            tariff_type_mask = (dataframe["tipo_de_tarifa"] == tariff_type)

            for tariff_block in dataframe[distributor_mask & tariff_type_mask]["bloque_de_tarifa"].unique():
                tariff_block_mask = dataframe["bloque_de_tarifa"] == tariff_block
                
                name = f"{distributor} - {tariff_block}"
                x = dataframe[distributor_mask & tariff_type_mask & tariff_block_mask]["annio_mes"]
                y = dataframe[distributor_mask & tariff_type_mask & tariff_block_mask]["colones_por_unidad_de_cobro"]
                
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=y,
                        name=name,
                        line=dict(
                                width=choose_symbol_or_dash_or_width(tariff_block, selection_mode="widths"),
                                color=COLOR_MAPPING.get(distributor),
                                dash=choose_symbol_or_dash_or_width(tariff_block, selection_mode="dashes")
                        ),
                        mode="lines+markers",
                        marker=dict(
                            symbol=choose_symbol_or_dash_or_width(tariff_block, selection_mode="symbols"),
                        )
                    )
                )

    fig.update_layout(
        template=template,
        title=dict(
            text='Price (CRC) per Billing Unit'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-1.05,
            xanchor="center",
            x=0.5
        ),
    )

    return fig

def vertical_mark(label):
    return {
        "label": label,
        "style": {
            "writingMode": "vertical-rl",
            "textOrientation": "mixed",
            "whiteSpace": "nowrap",
        },
    }


# -----------------------------------------------------------------------------
# Dashboard configuration
# -----------------------------------------------------------------------------

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
theme_name = "sketchy"

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.FONT_AWESOME, dbc_css])


color_mode_switch =  html.Span(
    [
        dbc.Label(class_name="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, class_name="d-inline-block ms-1", persistence=True),
        dbc.Label(class_name="fa fa-sun", html_for="switch"),
    ]
)

theme_controls = html.Div([color_mode_switch], className="hstack gap-3 mt-2")

header = html.H4(
    "", className="bg-primary p-2 mb-2 text-center"
)

table = dag.AgGrid(
    id="table",
    columnDefs=[{"field": i} for i in df.columns],
    rowData=df.to_dict("records"),
    defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
    dashGridOptions={"rowSelection": "multiple"},
)


dropdown = html.Div(
    [
        dbc.Label("※ Pick a tariff type", size='lg'),
        dcc.Dropdown(
            unique_tariff_types,
            "T-RE",
            id="tariff_type",
            clearable=False,
        ),
    ],
    className="mb-4",
)

checklist = html.Div(
    [
        dbc.Label("※ Select distribution companies", size='lg'),
        dbc.Checklist(
            id="distribuidor",
            options=unique_distributors,
            value=["ICE"],
            inline=True,
        ),
    ],
    className="mb-4",
)


mark_step = max(len(unique_years_months) // 12, 1)  # ~12 visible labels regardless of data size
marks = {i: vertical_mark(ym) for i, ym in enumerate(unique_years_months) if i % mark_step == 0}

marks[len(unique_years_months) - 1] = vertical_mark(unique_years_months[-1])

slider = html.Div(
    [
        dbc.Label("※ Specify a time range", size='lg'),
        dcc.RangeSlider(
            0,
            len(unique_years_months) - 1,
            1,
            id="years_months",
            marks=marks,
            allow_direct_input=False,
            value=[len(unique_years_months) - 5, len(unique_years_months) - 1],
            className="p-0",
        ),
    ],
    className="mb-4",
)


control1 = dbc.Card(
    [checklist],
    body=True,
    class_name="h-100"
)

control2 = dbc.Card(
    [dropdown],
    body=True,
    class_name="h-100"
)
control3 = dbc.Card(
    [slider],
    body=True,
    class_name="h-100"
)


tab1 = dbc.Tab(
    [
        dcc.Graph(
            id="chart",
            figure=go.Figure(),
            config={"responsive": True},
        )
    ],
    label="Chart",
    tab_id="chart-tab",
    className="p-4",
)

tab2 = dbc.Tab(
    [table],
    label="Table",
    className="p-4",
    tab_id="table-tab",
)

tabs = dbc.Card(
    dbc.Tabs(
        [tab1, tab2],
        id="tabs",
        active_tab="chart-tab",
    ),
)


app.layout = dbc.Container(
    [
        header,
        dbc.Row([dbc.Col([theme_controls],  xs=12, md=4, lg=2, class_name="h-100",),]),
        dbc.Row([
            dbc.Col([control1],  xs=12, md=4, lg=4, class_name="h-100",),
            dbc.Col([control2],  xs=12, md=4, lg=2, class_name="h-100",),
            dbc.Col([control3],  xs=12, md=4, lg=6, class_name="h-100",),
            ],
        class_name="g-3",
        align="stretch"
        ),
        dbc.Row([
            dbc.Col([tabs], xs=12, md=4, lg=12),
            ], 
        class_name="flex-grow-1 mt-4"
        ),
    ],
    fluid=True,
    class_name="dbc dbc-ag-grid d-flex flex-column p-3",
)


@app.callback(
    Output("chart", "figure"),
    Output("table", "dashGridOptions"),
    Input("tariff_type", "value"),
    Input("distribuidor", "value"),
    Input("years_months", "value"),
    Input("switch", "value")
)
def update(tariff_type, distributor, year_month, color_mode_switch_on):
    if distributor == [] or distributor is None:
        return {}, {}

    lo, hi = unique_years_months[year_month[0]], unique_years_months[year_month[1]]
    dff = df[df["annio_mes"].between(lo, hi)]
    dff = dff[dff["distribuidor"].isin(distributor)]
    dff = dff[dff["tipo_de_tarifa"] == tariff_type]
    

    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"
    fig = plot_figure(dff, template_name)

    grid_filter = f"{distributor}.includes(params.data.distribuidor) &&  params.data.tipo_de_tarifa == '{tariff_type}' && params.data.annio_mes >= '{lo}' && params.data.annio_mes <= '{hi}'" 
    dashGridOptions = {
        "isExternalFilterPresent": {"function": "true"},
        "doesExternalFilterPass": {"function": grid_filter},
    }
    
    return fig, dashGridOptions

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize_chart"),
    Output("chart", "style"),
    Input("tabs", "active_tab"),
)

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="toggle_theme"),
    Output("switch", "id"),
    Input("switch", "value"),
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=8050)
