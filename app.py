import functools
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests
import json
import os
import math

os.chdir(os.path.dirname(__file__))

#ke spuštění je potřeba si nainstalovat flask, requests a změnit cestu k souboru se zastávkami-viz níže (řád. 34,35)
#vzhledem k tomu, že se data stahují živě ze serveru, je potřeba mít internetové připojení

app = Flask(__name__)
app.secret_key = os.urandom(24)

#API klíč
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjEzOCwiaWF0IjoxNjk1NDU2MjAwLCJleHAiOjExNjk1NDU2MjAwLCJpc3MiOiJnb2xlbWlvIiwianRpIjoiOTNkY2M4N2ItODYyMC00Njc0LWFkOGYtNTZkNzdlNDUyNTBiIn0.a4rd76M7XzjbQYWYgFaOz2yWXoZbfpCHlxMeC9Vct7k"

STOP_ID = "" 
# U1308Z2 lii smer ladvi (jen poznámka pro testování)
# U2268Z1 bast bastek smer ladvi (jen poznámka pro testování)
# U78Z4P ladvi smer strizkov platforma D (jen poznámka pro testování)

url = "https://api.golemio.cz/v2/pid/departureboards"
headers = {
    "X-Access-Token": API_KEY
}
params = {
    "ids[]": STOP_ID,  # GTFS ID zastavky
    "minutesBefore": 1,  # x minut pred aktualnim casem
    "minutesAfter": 100,   # x minut po aktualnim case
    "limit": 20,  #kolik vysledku stahnu ze serveru
    #"includeMetroTrains": False,-rozbije kod
    "mode": "departures",
    "order": "real"}

@functools.cache
def load_station_data():
    with open("outp_zast.txt", encoding="utf8") as f:
        return json.load(f)
def getDelay(linka):
    if not linka["delay"]["is_available"]: return "xx:xx"
    sekundy = linka["delay"]["seconds"]
    sign = '- ' if sekundy < 0 else ''
    sekundy = abs(sekundy)
    return f'{sign}{sekundy // 60}:{sekundy % 60:02}'

def get_departures(LINE_ID=""):
    departures = []  #seznam na presun dat do html
    gtfsid = session.get("gtfsid")
    params["ids[]"]=gtfsid
    response = requests.get(url, headers=headers, params=params)
    departures_data = response.json().get('departures', []) #získání dat ze serveru
    
    for linka in departures_data:
        if LINE_ID!="":
            #filtr busu dle linky
            if linka["route"]["short_name"] != LINE_ID:
                continue
        #příprava dat na přesun        
        departures.append({
            "line": linka['route']['short_name'],
            "destination": linka['trip']['headsign'],
            "depart_time": linka["departure_timestamp"]["predicted"][11:19],
            "time_to_depart": linka["departure_timestamp"]["minutes"],
            "delay": getDelay(linka)
        })
    return departures

@app.route('/', methods=["GET"])
def index():
    gtfsid = session.get("gtfsid")
    if not gtfsid: #pokud není kod stanice, tak si ji uzivatel musi zvolit
        return redirect(url_for("select_station"))

    station = session.get("station")
    line_filter = request.args.get("linka", "").strip()
    departures = get_departures(line_filter)
    destinations = (line[1] for line in station['lines'])
    destinations = ', '.join(set(destinations))
    linesRender = ', '.join([' ⇒ '.join(line) for line in station['lines']])
    return render_template(
        "departures.html",
        departures=departures,
        linka=line_filter,
        station_name=session.get("station_name"),
        station=station,
        destinations=destinations,
        lines=linesRender,
        similar_stations=session.get("similar_stations"),
    )

def getMatchingStations(stations, search_query):
    if not search_query: return []
    return [
        station for station in stations if station["altIdosName"].lower().startswith(search_query)
    ][:20] # číslo omezí počet výsledků->aby netrvalo hledání moc dlouho

@app.route('/select_station', methods=["GET", "POST"])
def select_station():
    gtfsid = request.form.get("station_gtfsid")
    stations = load_station_data()
    if gtfsid:
        selected_station = next((s for s in stations if s["gtfsIds"] == gtfsid), None)
        if selected_station:
            session["gtfsid"] = gtfsid
            session["station_name"] = selected_station["altIdosName"]
            session["station"] = selected_station
            session["similar_stations"] = [s for s in stations if s['altIdosName'] == selected_station['altIdosName']]
            return redirect(url_for("index"))

    search_query = request.args.get("station", "").strip().lower()
    return render_template(
        "select_station.html",
        stations=getMatchingStations(stations, search_query),
        search_query=search_query
    )

def haversineDistance(stop, lat, lon):
    '''eastimate of distance on curved surface of Earth'''
    lat2, lon2 = stop['coords']
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat)
    dlon = math.radians(lon2 - lon)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c # distance in km

@app.route('/get_stops_nearby', methods=["GET"])
def get_stops_nearby(min_count=7):
    try:
        lat = float(request.args["lat"])
        lon = float(request.args["lon"])
    except (KeyError, ValueError):
        return "Error při hledání nejbližších zastávek"
    stations = load_station_data()
    count = int(request.args.get('count', '0'))
    nearby = sorted(stations, key=lambda stop: haversineDistance(stop, lat, lon))[:max(count, min_count)]
    return render_template(
        "render_stops.html",
        stations=nearby,
        search_query=""
    )

@app.route('/refresh_departures', methods=["GET"])
def refresh_departures(): #automatická aktualizace odjezdů
    linka_filtruj=request.args.get("linka","").strip()
    if linka_filtruj:
        departures=get_departures(linka_filtruj)
    else:
        departures = get_departures()
    return jsonify(departures)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
