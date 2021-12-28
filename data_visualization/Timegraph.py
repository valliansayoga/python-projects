# Call a function from mo_cap file
from bokeh.models.annotations import Title
from motion_cap import df  # df disimpan sebagai cache

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, sources

df["Start_string"] = df["Start"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)  # Membuat kolom baru untuk tanggal
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

p = figure(
    x_axis_type="datetime",
    height=100,
    width=500,
    sizing_mode="scale_both",
    title="Time Graph",
)
p.yaxis.minor_tick_line_color = None  # Menghilangkan garis minor di antara value utama
p.yaxis[
    0
].ticker.desired_num_ticks = 1  # Untuk menghilangkan garis vertikal # Solusi dari Q&A p.yaxis[0].ticker.desired_num_ticks=1

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q = p.quad(
    left="Start", right="End", bottom=0, top=1, color="red", source=cds
)  # Harus dihapus dulu yang df["COLUMN"] dan diganti jadi "Column aja"

output_file("Timegraph2.html")
show(p)
