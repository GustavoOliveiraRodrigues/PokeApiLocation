import requests 
import pandas as pd
import os

base_url = 'https://pokeapi.co/api/v2/'


def extractIdPokemon(pokemon_url):
    return pokemon_url.rstrip("/").split("/")[-1]

def allpokemon():
    url = f"{base_url}/pokemon?limit=1302"
    req = requests.get(url)

    if req.status_code == 200:
        data = req.json()
        pokemon_list = []
        
        for pokemon in data['results']:
            pokemonId = extractIdPokemon(pokemon['url'])
            pokemon_list.append({
                "id" : pokemonId,
                "name": pokemon["name"],
                "url": pokemon["url"]
            })

        df = pd.DataFrame(pokemon_list)
        df.to_csv(r"G:\Vscode projetos\AnalistaDeDadosPokemon\csv\pokemons.csv", index=False)

def locationPokemon(pokemon_id):
    url = f"https://pokeapi.co/api/v2/location/{pokemon_id}/"
    req = requests.get(url)
    
    if req.status_code == 200:
        data = req.json()
        city_name = next((name['name'] for name in data.get('names', []) if name['language']['name'] == 'en'), None)
        return city_name
    else:
        print(f"Erro ao buscar localização para Pokémon ID {pokemon_id}: {req.status_code}")
        return None

def extractionLocation (csv_file, output_file):
    df = pd.read_csv(csv_file)
    
    with open(output_file, 'w') as f:
        f.write("id,name,location,url\n")

    for index, row in df.iterrows():
        pokemonId = row["id"]
        localition = locationPokemon(pokemonId)

        temp_df = pd.DataFrame({
            "id":[pokemonId],
            "name": [row['name']],
            "location": [localition],
            "url":[row["url"]]
        })
        temp_df.to_csv(output_file, mode='a', header=False, index=False)
        print(f"Dados de localização para Pokémon ID {pokemonId} salvos.")


def main():
    allpokemon()

    csv_file = r"G:\Vscode projetos\AnalistaDeDadosPokemon\csv\pokemons.csv"
    output_file = r"G:\Vscode projetos\AnalistaDeDadosPokemon\csv\pokemons_locations.csv"
    extractionLocation(csv_file, output_file)



if __name__ == '__main__':
    main()

