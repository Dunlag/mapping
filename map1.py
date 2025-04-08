import folium
import pandas
import json

data = pandas.read_csv("./Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"



map = folium.Map(
    location=[38.58, -99.09],
    zoom_start=6,
    tiles="CartoDB positron",
    attr="Map data © CartoDB contributors",
)

fgv = folium.FeatureGroup(name="Volcanoes")

# Agregar marcadores al mapa
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            popup=folium.Popup(f"Elevation: {el}m", parse_html=True),
            color=color_producer(el), fill=True, fill_color=color_producer(el), fill_opacity=1,        )
    )

fgp = folium.FeatureGroup(name="Population")

# Cargar archivo GeoJSON
with open("./world.json", "r", encoding="utf-8-sig") as f:
    geojson_data = json.load(f)  # Cargar el contenido del archivo como un objeto JSON

# Agregar GeoJSON al FeatureGroup
fgp.add_child(folium.GeoJson(
    data=geojson_data,
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 
        else 'red'
    }
))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

# Guardar el mapa en un archivo HTML
map.save("./Map1.html")
