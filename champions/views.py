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