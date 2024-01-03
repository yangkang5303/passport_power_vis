import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# 用您的Excel文件路径替换 'passport_data.xlsx'
excel_file_path = 'passport-power-2023-05-16.xlsx'

# 从Excel文件中读取数据
df = pd.read_excel(excel_file_path)

# 设置颜色映射
color_scale = px.colors.sequential.Greens

# 创建 Dash 应用
app = dash.Dash(__name__)

# 生成交互式地图布局
app.layout = html.Div([
    dcc.Graph(
        id='world-map',
        figure=px.choropleth(
            df,
            locations='origin',
            locationmode='country names',
            color='requirement_status',
            hover_name='destination',
            color_continuous_scale=color_scale,
            title='World Passport Requirements Map',
            projection='natural earth'
        ),
        style={'width': '1200px', 'height': '800px'}  # 设置图表宽度和高度
    )
])


# 回调函数，用于更新地图颜色
@app.callback(
    Output('world-map', 'figure'),
    [Input('world-map', 'clickData')]
)
def update_map(clickData):
    if clickData:
        # 获取点击的国家
        selected_country = clickData['points'][0]['location']

        # 更新颜色映射
        updated_figure = px.choropleth(
            df,
            locations='origin',
            locationmode='country names',
            color='requirement_status',
            hover_name='destination',
            color_continuous_scale=color_scale,
            title='World Passport Requirements Map',
            projection='natural earth'
        )

        # 高亮点击的国家
        updated_figure.update_geos(showcountries=True, countrycolor='Black')
        updated_figure.add_trace(
            px.choropleth(
                df[df['origin'] == selected_country],
                locations='destination',
                locationmode='country names',
                color='requirement_status',
                hover_name='destination',
                color_continuous_scale=color_scale,
                projection='natural earth'
            ).data[0]
        )

        return updated_figure

    # 如果没有点击，返回原始地图
    return px.choropleth(
        df,
        locations='origin',
        locationmode='country names',
        color='requirement_status',
        hover_name='destination',
        color_continuous_scale=color_scale,
        title='World Passport Requirements Map',
        projection='natural earth'
    )


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
