import bottle
import json
import ChessAPI


@bottle.route("/")
def index_html():
    return bottle.static_file("index.html", root=".")


@bottle.route("/scripts.js")
def myscripts_js():
    return bottle.static_file("scripts.js", root=".")


@bottle.route("/ajaxhelper.js")
def ajaxhelper():
    return bottle.static_file("ajaxhelper.js", root=".")


@bottle.get("/get_elo")
def get_elo_route(player):
    elodata = ChessAPI.get_game_ratings(player)
    return json.dumps(elodata)

@bottle.get("/get_countries")
def get_countries_route(player):
    countriesdata = ChessAPI.get_oponent_nationalities(player)
    return json.dumps(countriesdata)

@bottle.post("/update_elo")
def update_elo():
    content = bottle.request.body.read().decode()
    data = json.loads(content)
    return get_elo_route(data)

@bottle.post("/update_nationalities")
def update_nationalities():
    content = bottle.request.body.read().decode()
    data = json.loads(content)
    return get_countries_route(data)


bottle.run(host="0.0.0.0", port=8080, debug=True)