import folium
import pandas

data = pandas.read_csv("NZ-volcanoes.txt")
lat = list(data["Lat"])
lon = list(data["Lon"])
name = list(data["Name"])

map = folium.Map(location=[-40.9006, 174.8860], zoom_start=6, tiles="Stamen Terrain")

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

fgv = folium.FeatureGroup(name="My Map")

for  lt, ln, nm in zip(lat, lon, name):
    iframe = folium.IFrame(html=html % (nm, lt, ln), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, ln], popup=nm, icon=folium.Icon(color='green')))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <=  x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("index.html")
