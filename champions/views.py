from django.shortcuts import render
from django.http import HttpResponse
import requests
from decouple import config
from django.utils.safestring import mark_safe
import json

def home(request):
    return HttpResponse("Bienvenido a LoL Data!")

def riot_api_test(request):
    api_key = config('RIOT_API_KEY')
    rotation_url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
    ddragon_url = "https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/champion.json"
    icon_url_base = "https://ddragon.leagueoflegends.com/cdn/13.20.1/img/champion/"

    rotation_response = requests.get(rotation_url, headers={"X-Riot-Token": api_key})
    if rotation_response.status_code != 200:
        return HttpResponse(f"Error al obtener la rotación de campeones: {rotation_response.status_code}")

    ddragon_response = requests.get(ddragon_url)
    if ddragon_response.status_code != 200:
        return HttpResponse(f"Error al obtener datos de campeones: {ddragon_response.status_code}")

    champions_data = ddragon_response.json()
    rotation_data = rotation_response.json()
    free_champ_ids = rotation_data['freeChampionIds']

    champions = {int(champ['key']): champ for champ in champions_data['data'].values()}
    free_champs = [
        {
            'name': champions[champ_id]['name'],
            'icon': f"{icon_url_base}{champions[champ_id]['id']}.png"
        }
        for champ_id in free_champ_ids
    ]

    return render(request, 'riot_api_test.html', {'free_champs': free_champs})

def champions_list(request):
    ddragon_url = "https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/champion.json"
    response = requests.get(ddragon_url)
    if response.status_code != 200:
        return HttpResponse("Error al obtener la lista de campeones.")

    champions_data = response.json()
    champions = [
        {
            'id': champ['id'],
            'name': champ['name'],
            'title': champ['title'],
            'icon': f"https://ddragon.leagueoflegends.com/cdn/13.20.1/img/champion/{champ['id']}.png"
        }
        for champ in champions_data['data'].values()
    ]
    return render(request, 'champions_list.html', {'champions': champions})

def champion_detail(request, champion_id):
    # URLs para los datos
    ddragon_url = f"https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/champion/{champion_id}.json"
    items_url = "https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/item.json"

    # Realizar las solicitudes
    champion_response = requests.get(ddragon_url)
    items_response = requests.get(items_url)

    # Verificar errores en las solicitudes
    if champion_response.status_code != 200 or items_response.status_code != 200:
        return HttpResponse("Error al obtener los datos del campeón u objetos.")

    # Parsear los datos
    champion_data = champion_response.json()
    items_data = items_response.json()

    # Filtrar datos de botas
    boots = {key: value for key, value in items_data['data'].items() if 'Boots' in value.get('tags', [])}
    items = items_data['data']

    # Obtener datos del campeón
    champion = champion_data['data'][champion_id]
    levels = list(range(1, 19))  # Niveles disponibles para el cálculo de estadísticas

    # Renderizar la plantilla
    return render(request, 'champion_detail.html', {
        'champion': champion,
        'boots': json.dumps(boots),  # Serializar los datos de botas
        'items': json.dumps(items),  # Serializar los datos de objetos
        'levels': levels,            # Enviar niveles como datos de contexto
    })