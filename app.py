from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# read data
df = pd.read_csv('./test_facility_disruption_data.csv')

# clean data
threat_value_map = {
    'Heatwave': 'Heatwave',
    'Freeze': 'Freeze',
    'Drought/Water Stress': 'Drought',
    'Temperate Windstorm': 'Windstorm',
    'Flash Flood': 'Flood',
    'Coastal Flood': 'Flood',
    'Riverine Flood': 'Flood',
    'Tropical Windstorm': 'Windstorm'
}
mapped_values = df["physical_threat_type"].map(threat_value_map)
df["physical_threat_type"] = mapped_values


# initialise and lay out app
app = Dash()

app.layout = [
    html.Div(children=html.H1('Climate Disruption to Facilities'), className="page_header"),
    html.Div(children=[html.Div(children=[dcc.Dropdown(["Heatwave", "Freeze", "Drought", "Windstorm", "Flood"], "Heatwave", id="threat_dropdown")], className="filter"),
                       html.Div(children=[dcc.Dropdown(["Paris Agreement", "Stated Policy", "Current Policy", "No Policy"], "No Policy", id="pathway_dropdown")], className="filter")],
                       className="filters"),
    dcc.Graph(figure={}, id="type_graph", className="fig"),
    dcc.Graph(figure={}, id="facilities_map", className="fig")
    
]

# add dynamic filtering with callback
@callback(
        [Output(component_id = "type_graph", component_property = "figure"),
         Output(component_id = "facilities_map", component_property = "figure")],
        [Input(component_id = "pathway_dropdown", component_property = "value"),
         Input(component_id = "threat_dropdown", component_property = "value")]
    )
def update_charts(pathway, threat):
    filtered_df = df[(df['climate_pathway'] == pathway) & (df['physical_threat_type'] == threat)]

    chart = px.histogram(filtered_df,
                         x = 'facility_type',
                         y ='disruption_millions',
                         title = "Disruption by Facility Type",
                         labels = {"facility_type": "Facility Type", "disruption_millions": "disruption ($million)"})

    mapGraph = px.scatter_map(filtered_df,
                              lat = "latitude",
                              lon = "longitude",
                              title = "Disruption by Facility",
                              color = "disruption_millions", 
                              hover_name = "facility_name",
                              hover_data = ["disruption_millions", "physical_threat_type"],
                              labels = {
                                  "disruption_millions": "Disruption ($million)",
                                  "facility_name": "Facility name",
                                  "physical_threat_type": "Physical Threat Type"},
                              range_color = [0, 2],
                              color_continuous_scale = "turbo",
                              zoom = 1,
                              height = 800)
    return chart, mapGraph

# run app
if __name__ == '__main__':
    app.run(debug=True)