# Autor del Código: CGLMaster

#Insertar las credenciales de tu token de twitch
from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper("****************", "********************")

import requests
import json
import pandas as pd

# Igual que arriba introducir las credenciales de tu token
url = 'https://id.twitch.tv/oauth2/token'
myobj = {'client_id': '*********************',
          'client_secret': '*****************',
          'grant_type':'client_credentials'}

x = requests.post(url, data = myobj)

print(x.text)
i = x.json()

# Introduces el client_id de tu token
wrapper = IGDBWrapper("******************", i['access_token'])

# Obtencion de los juegos

print("Obtencion de los juegos")

# Num lo utilizo para obtener exactamente desde esa posición juegos, si cambias los valores, y quieres obtener muchos juegos, te recomiendo que lo hagas de 500 a 500
# ya que es el máximo de juegos que puedes obtener en una llamada, en el caso de que quieras añadir más valores a num abajo de explicaré que hacer por cada uno de los valores
# Seguramente haya una forma más óptima pero es la forma más sencilla que encontré y me funciona

num = [6000,6500,7000,7500,8000,8500]

# Código para obtener 3000 juegos
for n in num:
    
    # Por cada información que quieras obtener te recomiendo hacer este tipo de llamada y por cada atributo obtenerlo a través de 1 pto (cover.url)
    # f' ' se utiliza para poder introducir un atributo externo dentro de la llamada, en este caso yo lo uso para indicar con offset la posición inicial de la búsqueda
    # l o limit es para limitar el máximo, si no lo pones te sacará la API el límite por defecto
    # si solamente quieres obtener por ejemplo las plataformas tendrás que cambiar el tipo de import y la llamada, así por cada atributo que se encuentra en la API
    # es decir, si quieres solo obtener las plataformas sería de esta forma ( al ser menos de 500 si quieres obtener todas pon el límite de 500, una vez no haya más dejará de obtenerlas):
    # from igdb.igdbapi_pb2 import PlatformResult
    # byte_array2 = wrapper.api_request(
    #               'platforms', 
    #               'f name;'
    #             )

    from igdb.igdbapi_pb2 import GameResult
    byte_array = wrapper.api_request(
                'games', 
                f'f name, cover.url, involved_companies.company.name, genres.name, platforms.name, summary, release_dates.date; l 500; offset {n};'
              )
    games_message = GameResult()
    
    # Funcion para decodificar los bytes obtenidos en GameResult(), cargarlo como JSON y pasarlo a un DataFrame
    
    data = pd.json_normalize(json.loads(byte_array.decode('utf-8')))
    
    data = data.set_index('id')
    
    # Le cambio el nombre para luego resultarme más sencillo su introducción de datos ya sea en una base de datos o visualmente en el JSON
    data = data.rename(columns={'cover.url' : 'cover', 'cover.id' : 'image'})
    
    # Obtencion de los generos
    
    print("Obtencion de los generos")
    
    genres = data["genres"]
    gen = []
    for g in genres:
       if str(g) != 'nan':
            aux = []
            for ge in g:
                aux.append(ge["name"])
            gen.append(aux)
       else:
           gen.append(g)
    data["genres"] = gen
    
    # Obtencion de las plataformas
    
    print("Obtencion de las plataformas")
    
    platforms = data["platforms"]
    plat = []
    for pla in platforms:
       if str(pla) != 'nan':
            aux = []
            for p in pla:
                aux.append(p["name"])
            plat.append(aux)
       else:
           plat.append(pla)
    data["platforms"] = plat
    
    # Obtencion de las compañias
    
    print("Obtencion de las compañias")
    
    companies = data["involved_companies"]
    compa = []
    for com in companies:
       if str(com) != 'nan':
            aux = []
            for c in com:
                aux.append(c["company"]["name"])
            compa.append(aux)
       else:
           compa.append(com)
    data["involved_companies"] = compa
    
    # Obtencion de las portadas
    
    print("Obtencion de las portadas")
    
    covers = data["cover"]
    cov = []
    for co in covers:
        if str(co) != 'nan':
            # en este caso como yo quería también imagenes más grandes cambie a la que yo quería la url, por defecto te sale una cover pequeña
            a = co.replace('t_thumb', 't_cover_big')
            cov.append(a)
        else:
            cov.append(co)
    data["image"] = cov
    
    # Obtencion de las fechas
    
    print("Obtencion de las fechas")
    
    dates = data["release_dates"]
    dat = []
    for da in dates:
       if str(da) != 'nan':
           if len(da[0]) > 1:
                dat.append(da[0]["date"])
           else: dat.append(da)
       else:
           dat.append(None)
    data["release_dates"] = dat

    # Por cada variable del vector num, tienes que crear un data que almacenará los 500 juegos buscados, por más variables, más elif y datas tendras que crear
    if n == 6000:
        data1 = data
    elif n == 6500:
        data2 = data
    elif n == 7000:
        data3 = data
    elif n == 7500:
        data4 = data
    elif n == 8000:
        data5 = data
    else: data6 = data

# Ahora al final ya fuera del bucle lo que haces en concatenar todos los datas para tenerlos en un mismo dataframe
dataBase = pd.concat([data1, data2, data3, data4, data5, data6])
# Seguido de eso se transforma en JSON y se exporta al archivo que indiques en mi caso (games.json), en caso de que no exista lo crea en la misma carpeta que se encuentre
# este código guardado
dataBase.to_json("games.json", orient='index')
