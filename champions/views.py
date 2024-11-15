from django.shortcuts import render
from django.http import HttpResponse
import requests
from decouple import config

def home(request):
    return HttpResponse("Bienvenido a LoL Data!")

def riot_api_test(request):
    # API Key y URLs
    api_key = config('RIOT_API_KEY')
    rotation_url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
    ddragon_url = "https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/champion.json"
    icon_url_base = "https://ddragon.leagueoflegends.com/cdn/13.20.1/img/champion/"

    # Obtener la rotación gratuita
    rotation_response = requests.get(rotation_url, headers={"X-Riot-Token": api_key})
    if rotation_response.status_code != 200:
        return HttpResponse(f"Error al obtener la rotación de campeones: {rotation_response.status_code}")
    rotation_data = rotation_response.json()
    free_champ_ids = rotation_data['freeChampionIds']

    # Obtener datos de campeones desde Data Dragon
    ddragon_response = requests.get(ddragon_url)
    if ddragon_response.status_code != 200:
        return HttpResponse(f"Error al obtener datos de campeones: {ddragon_response.status_code}")
    champions_data = ddragon_response.json()
    champions = {int(champ['key']): champ for champ in champions_data['data'].values()}

    # Mapear IDs a nombres e íconos
    free_champs = [
        {
            'name': champions[champ_id]['name'],
            'icon': f"{icon_url_base}{champions[champ_id]['id']}.png"
        }
        for champ_id in free_champ_ids
    ]

    # Renderizar la plantilla
    return render(request, 'riot_api_test.html', {'free_champs': free_champs})

def champions_list(request):
    # Endpoint de Data Dragon para los datos de campeones
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

    # Renderiza la lista de campeones
    return render(request, 'champions_list.html', {'champions': champions})

def champion_detail(request, champion_id):
    # Endpoint de Data Dragon para los datos del campeón
    ddragon_url = f"https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/champion/{champion_id}.json"
    items_url = "https://ddragon.leagueoflegends.com/cdn/13.20.1/data/en_US/item.json"

    champion_response = requests.get(ddragon_url)
    items_response = requests.get(items_url)

    if champion_response.status_code != 200 or items_response.status_code != 200:
        return HttpResponse("Error al obtener los datos del campeón u objetos.")

    champion_data = champion_response.json()
    items_data = items_response.json()

    # Filtrar botas
    boots = {key: value for key, value in items_data['data'].items() if 'Boots' in value.get('tags', [])}
    items = items_data['data']

    # Generar listas
    levels = list(range(1, 19))
    main_items_slots = list(range(4))  # 4 casillas de objetos principales
    partial_items_slots = list(range(4))  # 4 casillas de objetos parciales

    champion = champion_data['data'][champion_id]

    # Renderizar plantilla con datos
    return render(request, 'champion_detail.html', {
        'champion': champion,
        'levels': levels,
        'boots': boots,
        'items': items,
        'main_items_slots': main_items_slots,
        'partial_items_slots': partial_items_slots,
    })


