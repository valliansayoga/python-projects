import justpy as jp
from pytz import UTC
from datetime import datetime
import pandas
from justpy.chartcomponents import HighCharts
from pandas.core.dtypes.common import classes

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data["Month"] = data["Timestamp"].dt.strftime("%Y - %m")
month_average_crs = data.groupby(["Month", "Course Name"]).mean().unstack()

chart_def = """
{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Average Rating per Course by Month'
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: false,
        borderWidth: 1,
        backgroundColor:
        '#F0F0F0'
    },
    xAxis: {
        categories: [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ''
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
    }]
}
"""
# Bermasalah di legend.background color karena syntaxnya jscript. Ganti dengan hex code aja
# Area spline di chart.type bisa diganti jadi spline
# Legendnya juga bisa dimatikan floatingnya


def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(
        a=wp, text="Analysis of Course Reviews", classes="text-h3 text-center q-pa-md"
    )
    p1 = jp.QDiv(
        a=wp,
        text="These graphs represent course review analysis",
        classes="text-body1 text-center q-pa-md",
    )

    hc = jp.HighCharts(a=wp, options=chart_def)
    hc.options.xAxis.categories = list(month_average_crs.index)
    hc_data = [
        {
            "name": v1,
            "data": [v2 for v2 in month_average_crs[v1]],
        }  # List comprehension series yang mengandung {NAME:V1, DATA:[V2 yang ada di kolom V1]}
        for v1 in month_average_crs.columns
    ]
    hc.options.series = hc_data  # Harus diubah
    return wp


jp.justpy(app)
