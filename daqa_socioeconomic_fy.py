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

years = [1819, 1857, 1858, 1859, 1861, 1862, 1863, 1864, 1865, 1866, 1868, 1869, 1870, 1871, 1873, 1875, 1876, 1878, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2028]

counts = [1, 1, 1, 1, 1, 5, 3, 5, 3, 3, 2, 2, 1, 2, 3, 4, 1, 1, 2, 1, 2, 9, 2, 2, 4, 13, 10, 5, 4, 2, 1, 4, 4, 1, 1, 4, 4, 7, 3, 4, 5, 4, 7, 5, 7, 5, 5, 4, 5, 7, 16, 3, 3, 8, 9, 10, 8, 4, 10, 13, 11, 7, 10, 11, 15, 4, 11, 2, 6, 11, 22, 20, 29, 23, 13, 11, 10, 2, 1, 1, 1, 5, 2, 2, 2, 3, 6, 11, 10, 13, 13, 24, 22, 21, 48, 15, 22, 26, 35, 39, 35, 27, 40, 37, 27, 8, 18, 10, 6, 11, 13, 11, 3, 10, 9, 15, 13, 9, 8, 8, 8, 8, 15, 9, 14, 5, 4, 4, 3, 6, 8, 5, 4, 6, 12, 5, 3, 4, 5, 5, 3, 3, 5, 2, 4, 5, 7, 5, 7, 5, 3, 10, 4, 1, 5, 1, 1]

# load data

socio_econ_fy = fetch_small_data_from_github('DAQA_socioecon_fy.csv')
socio_econ_fy['Year'] = socio_econ_fy['Year_Financial'].str[:4].astype(int)

years_financial = [str(year)[-2:] + '-' + str(year+1)[-2:] for year in years if year != 0]

# if 000 is in column name then multiply column values by 1000 and remove 000 from column name
for x_col in socio_econ_fy.columns:
    if '_Millions' in x_col: 
        socio_econ_fy[x_col] = socio_econ_fy[x_col] * 1000000
        socio_econ_fy.rename(columns={x_col: x_col.replace('_Millions', '')}, inplace=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=years, y=counts, mode='lines', line=dict(color='steelblue')))
fig1.update_layout(title="Completed Buildings by Year, Financial Year", xaxis_title="Year", yaxis_title="Count")

fig2 = go.Figure()

app2 = dash.Dash(__name__)
server = app2.server

app2.layout = html.Div(
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
        value=350000000,
        placeholder="Select a y-axis limit"
    ),
    dcc.Graph(id='plot2', figure=fig2)
])

@app2.callback(
    Output('plot1', 'figure'),
    Output('plot2', 'figure'),
    Output('heading', 'children'),
    Input('year-slider', 'value'),
    Input('y-axis-limit', 'value')
)

def update_plot(year_range, y_axis_limit):
    start_year, end_year = year_range
    filtered_years = [year for year in years if start_year <= year <= end_year]
    filtered_years_financial = [str(year)[-2:] + '-' + str(year+1)[-2:] for year in years if start_year <= year <= end_year]
    filtered_counts = [count for year, count in zip(years, counts) if start_year <= year <= end_year]
    socio_econ_fy_thisperiod = socio_econ_fy[(socio_econ_fy['Year'] >= start_year) & (socio_econ_fy['Year'] <= end_year)]

    
    updated_fig1 = go.Figure()
    updated_fig1.add_trace(go.Scatter(x=filtered_years, y=filtered_counts, mode='lines', line=dict(color='steelblue')))
    updated_fig1.update_layout(title="Completed Buildings by Year, Financial Year", xaxis_title="Year", yaxis_title="Count")
    updated_fig1.update_traces(hovertemplate="Year: %{text}<br>Count: %{y}", text=filtered_years_financial)

    # show less ticks on x-axis when ticks are ticktext
    updated_fig1.update_xaxes(ticktext=filtered_years_financial, tickvals=filtered_years)
    updated_fig1.update_xaxes(tickmode='array', tickangle=-45, tickfont=dict(size=10))

    # show year as financial year i.e., 2020-21

    updated_fig2 = go.Figure()
    cols_used = []
    for x_col in socio_econ_fy.columns:
        if (x_col != 'Year_Financial') & (x_col != 'Year'):         
        # if (x_col != 'Year_Financial') & (x_col != 'Year') & \
        # ('rate' not in x_col) & ('YoY_change' not in x_col) & ('ercentage' not in x_col) & ('Index' not in x_col):
            if socio_econ_fy_thisperiod[x_col].isnull().sum() != (end_year - start_year + 1):
                cols_used.append(x_col)
                updated_fig2.add_trace(go.Scatter(x=socio_econ_fy['Year'], y=socio_econ_fy[x_col], mode='lines', name=x_col))
                # add 'Year_Financial' to hovertemplate
                updated_fig2.update_traces(hovertemplate="Year: %{text}<br>Count: %{y}", text=socio_econ_fy['Year_Financial'])

    updated_fig2.update_layout(
        title="Socioeconomic Trends, Financial Year",
        xaxis_title="Year",
        yaxis_title="Count",
        xaxis_range=[start_year, end_year],
        yaxis_range=[0, y_axis_limit],  # Use the selected y-axis limit
        height=650,
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.75,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
                )

        )
    
    # show corresponding "Year_Financial" on x-axis as opposed to "Year"
    updated_fig2.update_xaxes(ticktext=socio_econ_fy['Year_Financial'].str.replace("19",""), tickvals=socio_econ_fy['Year'])

    # show less ticks on x-axis when ticks are ticktext
    updated_fig2.update_xaxes(tickmode='array', tickangle=-45, tickfont=dict(size=10))


    heading_text = f"Year Range: {start_year} - {end_year}"
    
    return updated_fig1, updated_fig2, heading_text

if __name__ == '__main__':
    app2.run_server()
