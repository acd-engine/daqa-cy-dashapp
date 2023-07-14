import requests, io

# for data mgmt
import pandas as pd

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

years = [1820, 1858, 1859, 1860, 1862, 1863, 1864, 1865, 1866, 1867, 1869, 1870, 1871, 1872, 1874, 1875, 
         1876, 1877, 1879, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 
         1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 
         1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 
         1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1944, 1945, 
         1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 
         1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 
         1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 
         1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 
         2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2022, 2029]

counts = [1, 1, 1, 1, 2, 4, 5, 4, 2, 3, 2, 2, 1, 2, 3, 1, 3, 1, 1, 2, 1, 2, 9, 2, 2, 9, 14, 7, 4, 3, 1, 1, 
          5, 3, 2, 1, 4, 6, 5, 2, 7, 2, 5, 7, 7, 4, 7, 4, 3, 6, 7, 16, 2, 3, 8, 9, 10, 8, 6, 8, 16, 8, 9, 
          11, 9, 15, 6, 8, 2, 6, 21, 20, 26, 22, 20, 11, 13, 8, 1, 1, 2, 4, 2, 3, 2, 4, 7, 10, 10, 15, 15, 
          19, 28, 24, 42, 17, 23, 25, 33, 40, 40, 18, 44, 37, 23, 9, 17, 12, 3, 11, 13, 11, 4, 10, 8, 16, 
          13, 9, 7, 9, 8, 7, 15, 10, 15, 3, 4, 4, 4, 6, 7, 6, 4, 6, 14, 2, 3, 4, 5, 5, 3, 4, 5, 2, 6, 3, 
          8, 7, 3, 5, 5, 8, 4, 1, 5, 1, 1]

# load data
socio_econ_cy = fetch_small_data_from_github('DAQA_socioecon_cy.csv')

# if 000 is in column name then multiply column values by 1000 and remove 000 from column name
for x_col in socio_econ_cy.columns:
    if '_000' in x_col: 
        socio_econ_cy[x_col] = socio_econ_cy[x_col] * 1000
        socio_econ_cy.rename(columns={x_col: x_col.replace('_000', '')}, inplace=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=years, y=counts, mode='lines', line=dict(color='red')))
fig1.config.doubleClick = False
fig1.update_layout(title="Completed Buildings by Year, Calendar Year", xaxis_title="Year", yaxis_title="Count")

fig2 = go.Figure()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        'transform': 'scale(0.7)',
        'transform-origin': 'top left',
        'width': '125%',  # Adjust the width to fit the zoomed content
        'height': '125%',  # Adjust the height to fit the zoomed content
    },
    children = [
    html.H2(id='heading', children="Set Year Range"),
    dcc.RangeSlider(
        id='year-slider',
        min=1820,
        max=2020,
        step=1,
        value=[1940, 1980],
        # marks={str(year): str(year) for year in range(1820, 2021, 10)}
    	marks={
            1820: {'label': '1820', 'style': {'font-size': '20px'}},
            1830: {'label': '1830', 'style': {'font-size': '20px'}},
            1840: {'label': '1840', 'style': {'font-size': '20px'}},
            1850: {'label': '1850', 'style': {'font-size': '20px'}},
            1860: {'label': '1860', 'style': {'font-size': '20px'}},
            1870: {'label': '1870', 'style': {'font-size': '20px'}},
            1880: {'label': '1880', 'style': {'font-size': '20px'}},
            1890: {'label': '1890', 'style': {'font-size': '20px'}},
            1900: {'label': '1900', 'style': {'font-size': '20px'}},
            1910: {'label': '1910', 'style': {'font-size': '20px'}},
            1920: {'label': '1920', 'style': {'font-size': '20px'}},
            1930: {'label': '1930', 'style': {'font-size': '20px'}},
            1940: {'label': '1940', 'style': {'font-size': '20px'}},
            1950: {'label': '1950', 'style': {'font-size': '20px'}},
            1960: {'label': '1960', 'style': {'font-size': '20px'}},
            1970: {'label': '1970', 'style': {'font-size': '20px'}},
            1980: {'label': '1980', 'style': {'font-size': '20px'}},
            1990: {'label': '1990', 'style': {'font-size': '20px'}},
            2000: {'label': '2000', 'style': {'font-size': '20px'}},
            2010: {'label': '2010', 'style': {'font-size': '20px'}},
            2020: {'label': '2020', 'style': {'font-size': '20px'}}}
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
        height=700,

        # make legend text font smaller

        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-1.2,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            )
    )

    updated_fig2.config.doubleClick = False
    heading_text = f"Year Range: {start_year} - {end_year}"
    
    return updated_fig1, updated_fig2, heading_text

if __name__ == '__main__':
    app.run_server(debug=False)
