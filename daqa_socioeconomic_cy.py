import requests, gzip, io, json

# for data mgmt
import pandas as pd
import ast

# for plotting
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

def fetch_small_data_from_github(fname):
    url = f"https://raw.githubusercontent.com/acd-engine/jupyterbook/master/data/analysis/{fname}"
    response = requests.get(url)
    rawdata = response.content.decode('utf-8')
    return pd.read_csv(io.StringIO(rawdata))

def fetch_data(filetype='csv', acdedata='organization'):
    urls = fetch_small_data_from_github('acde_data_gdrive_urls.csv')
    sharelink = urls[urls.data == acdedata][filetype].values[0]
    url = f'https://drive.google.com/u/0/uc?id={sharelink}&export=download&confirm=yes'
    
    response = requests.get(url)
    decompressed_data = gzip.decompress(response.content)
    decompressed_buffer = io.StringIO(decompressed_data.decode('utf-8'))

    try:
        if filetype == 'csv': df = pd.read_csv(decompressed_buffer, low_memory=False)
        else: df = [json.loads(jl) for jl in pd.read_json(decompressed_buffer, lines=True, orient='records')[0]]
        return pd.DataFrame(df)
    except: return None 

def fetch_all_DAQA_data():
    daqa_data_dict = dict()
    for entity in ['work']:
        daqa_this_entity = fetch_data(acdedata=entity)
        daqa_data_dict[entity] = daqa_this_entity[daqa_this_entity.data_source.str.contains('DAQA')]
    return daqa_data_dict

df_daqa_dict = fetch_all_DAQA_data() # 1 min if data is already downloaded
daqa_work = df_daqa_dict['work']

# get year data
daqa_works_years = []

for idx,row in daqa_work.iterrows():
    if isinstance(row['coverage_range'], str): 
        if "date_end" in row['coverage_range']:
            comp_yr = pd.json_normalize(ast.literal_eval(row['coverage_range'])['date_range'])['date_end.year'].values[0]
            daqa_works_years.append(int(comp_yr))

daqa_works_years.remove(min(daqa_works_years))

# Count the occurrences of each year
year_counts = {}
for year in sorted(daqa_works_years): year_counts[year] = year_counts.get(year, 0) + 1

# Separate the years and counts into separate lists
years = list(year_counts.keys())
counts = list(year_counts.values())

# load data
# socio_econ_cy = pd.read_csv('data/socioecon/SocioEcon_CY.csv')
socio_econ_cy = fetch_small_data_from_github('DAQA_socioecon_cy.csv')

# if 000 is in column name then multiply column values by 1000 and remove 000 from column name
for x_col in socio_econ_cy.columns:
    if '_000' in x_col: 
        socio_econ_cy[x_col] = socio_econ_cy[x_col] * 1000
        socio_econ_cy.rename(columns={x_col: x_col.replace('_000', '')}, inplace=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=years, y=counts, mode='lines', line=dict(color='red')))
fig1.update_layout(title="Completed Buildings by Year, Calendar Year", xaxis_title="Year", yaxis_title="Count")

fig2 = go.Figure()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    # style={'overflow-y': 'hidden'},
    children = [
    html.H3(id='heading', children="Set Year Range"),
    dcc.RangeSlider(
        id='year-slider',
        min=1820,
        max=2020,
        step=1,
        value=[1940, 1980],
        marks={str(year): str(year) for year in range(1820, 2021, 10)}
    ),
    dcc.Graph(id='plot1', figure=fig1),
    dcc.Dropdown(
        id='y-axis-limit',
        options=[
            {'label': '3.5', 'value': 3.5},
            {'label': '35', 'value': 35},
            {'label': '350', 'value': 350},
            {'label': '3.5k', 'value': 35*(10**2)},
            {'label': '35k', 'value': 35*(10**3)},
            {'label': '350k', 'value': 35*(10**4)},
            {'label': '3.5M', 'value': 35*(10**5)},
            {'label': '35M', 'value': 35*(10**6)},
            {'label': '350M', 'value': 35*(10**7)},
            {'label': '3.5B', 'value': 35*(10**8)},
            {'label': '35B', 'value': 35*(10**9)},
            {'label': '350B', 'value': 35*(10**10)},
            {'label': '3.5T', 'value': 35*(10**11)}
        ],
        value=350000,
        placeholder="Select a y-axis limit"
    ),
    dcc.Graph(id='plot2', figure=fig2)
])

@app.callback(
    Output('plot1', 'figure'),
    Output('plot2', 'figure'),
    Output('heading', 'children'),
    Input('year-slider', 'value'),
    Input('y-axis-limit', 'value')
)

def update_plot(year_range, y_axis_limit):
    start_year, end_year = year_range
    filtered_years = [year for year in years if start_year <= year <= end_year]
    filtered_counts = [count for year, count in zip(years, counts) if start_year <= year <= end_year]
    socio_econ_cy_thisperiod = socio_econ_cy[(socio_econ_cy['Calendar_Year'] >= start_year) & (socio_econ_cy['Calendar_Year'] <= end_year)]

    updated_fig1 = go.Figure()
    updated_fig1.add_trace(go.Scatter(x=filtered_years, y=filtered_counts, mode='lines', line=dict(color='red')))
    updated_fig1.update_layout(title="Completed Buildings by Year, Calendar Year", xaxis_title="Year", yaxis_title="Count")

    updated_fig2 = go.Figure()
    cols_used = []
    for x_col in socio_econ_cy.columns:
        if (x_col != 'Calendar_Year'):
            if socio_econ_cy_thisperiod[x_col].isnull().sum() != (end_year - start_year + 1):
                cols_used.append(x_col)
                updated_fig2.add_trace(go.Scatter(x=socio_econ_cy['Calendar_Year'], y=socio_econ_cy[x_col], mode='lines', name=x_col))
                updated_fig2.update_traces(hovertemplate="Year: %{x}<br>Count: %{y}")

    updated_fig2.update_layout(
        title="Socioeconomic Trends, Calendar Year",
        xaxis_title="Year",
        yaxis_title="Count",
        xaxis_range=[start_year, end_year],
        yaxis_range=[0, y_axis_limit],  # Use the selected y-axis limit
        height=800,

        # make legend text font smaller

        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-1.8,
                xanchor="center",
                x=0.5,
                font=dict(size=7.5)
            )
    )
    
    heading_text = f"Year Range: {start_year} - {end_year}"
    
    return updated_fig1, updated_fig2, heading_text

if __name__ == '__main__':
    app.run_server(debug=False)
