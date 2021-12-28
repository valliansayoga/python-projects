# pip3.9 install folium
# Folium convert Python script to HTML, JS, CSS for web
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

# elevation range < 0; 0-1000; 1000-2000; 2000-3000; 3000++
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


# Create a variable to store the data
# Latitude = 90 to -90
# Longitude = 180 to -180
peta = folium.Map(location=[-1.7, 118.85], zoom_start=5, tiles="Cartodb Positron")

# Menambah children / extra objects (icon, comments, dll)
# Bisa di add ke variabel "peta" langsung atau dimasukan ke variabel baru
fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")


# Bisa for loop nambah coordinates dari file
# zip() untuk iteration di banyak list
# Command popup=folium.Popup(str(el).parse_html=True) untuk jaga2 ada tanda petik satu
for lt, ln, nama, el in zip(lat, long, name, elev):
    iframe = folium.IFrame(html=html % (nama, str(el)), width=225, height=150)
    # fg.add_child(folium.Marker(location = [lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_picker(el), icon='circle', prefix='fa')))
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

# Add data from json
# Harus ditambah .read()
# bisa ditambah parameter lain
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
peta.save("Peta Sebaran Gunung Api dan Populasi Indonesia Th 2005.html")
