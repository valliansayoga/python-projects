import justpy as jp
from pytz import UTC
from datetime import datetime
import pandas
from justpy.chartcomponents import HighCharts
from pandas.core.dtypes.common import classes

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data["Day"] = data["Timestamp"].dt.date
day_average = data.groupby(["Day"]).mean()

# chart def untuk menyimpan javascript chart dari highchart documentation
# copas dari curly bracket - curly bracket terbawah setelah "container, "
# inverted false = urutan axis (x,y)
chart_def = """
{
    chart: {
        type: 'spline',
        inverted: false 
    },
    title: {
        text: 'Atmosphere Temperature by Altitude'
    },
    subtitle: {
        text: 'guided by Ardit Sulce'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Average Rating'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Average Rating',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
"""


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
    # hc.options adalah object semacam dictionary yang enables accessing dict keys with "."
    hc = jp.HighCharts(a=wp, options=chart_def)
    hc.options.title.text = "Average Rating by Day"
    hc.options.xAxis.categories = list(
        day_average.index
    )  # x axis label dimasukan ke sini karena ga keluar kalo dimasukan ke .data

    # Menggabungkan x dan y dengan list(zip(x,y)), lalu masukan ke dalam hc.options[0].data =

    hc.options.series[0].data = list(
        day_average["Rating"]
    )  # Tidak perlu memasukan X ke dalam karena sudah dimasukan di hc.options.xAxis.categories
    # series adalah key yang bervalue list dan isinya dict. [0] untuk mengakses 1 itemnya (dict), kemudian .data untuk refer data keys
    return wp


jp.justpy(app)
