import folium
import pandas

volcanoes = pandas.read_excel("indo_volcanoes.xlsx", sheet_name=0)
lat = list(volcanoes["Latitude"])
long = list(volcanoes["Longitude"])
elev = list(volcanoes["Elev"])
name = list(volcanoes["Volcano Name"])
html = """<h4>Volcano information:</h4>
<h3>%s</h3>
Height: %s m
"""


def color_picker(elevation):
    if elevation < -100:
        return "darkblue"
    elif -100 <= elevation < 0:
        return "blue"
    elif 0 <= elevation < 1000:
        return "green"
    elif 1000 <= elevation < 2000:
        return "darkgreen"
    elif 2000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


peta = folium.Map(location=[-1.7, 118.85], zoom_start=5, tiles="Cartodb Positron")
fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")

for lt, ln, nama, el in zip(lat, long, name, elev):
    iframe = folium.IFrame(html=html % (nama, str(el)), width=225, height=150)
    fgv.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=7,
            popup=folium.Popup(iframe),
            tooltip="%s" % nama,
            fill_color=color_picker(el),
            color="grey",
            fill_opacity=0.7,
        )
    )

fgp.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "yellow"
            if 10000000 <= x["properties"]["POP2005"] < 30000000
            else "orange"
            if 30000000 <= x["properties"]["POP2005"] <= 100000000
            else "red"
        },
    )
)

peta.add_child(fgp)
peta.add_child(fgv)
peta.add_child(folium.LayerControl())
peta.save("Interactive_Indonesia_volcanoes_map.html")
