import json
import random
import requests
import datetime

def get_asmaul_husna():
    # Load the data from the JSON file
    with open('lib/asmaul_husna.json', 'r', encoding='utf-8') as file:
        asmaul_husna_data = json.load(file)

    # Get a random index
    random_index = random.randint(0, len(asmaul_husna_data) - 1)
    
    # Get the corresponding data
    asmaul_husna = asmaul_husna_data[random_index]
    arab = asmaul_husna['ar']
    # Construct JSON response
    response_json = {
        "status": 200,
        "message": "success",
        "result": {
           "index": asmaul_husna['index'],
           "ar": arab,
           "id": asmaul_husna['id'],
           "en": asmaul_husna['en']
        }
    }

    return json.dumps(response_json, indent=4, ensure_ascii=False)

def get_quran_audio(Surah, Ayat=None):
    try:
        if Ayat is None:
            api_url = f"https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/{Surah}.mp3"
            print(api_url)
            return api_url
        else:
            api_url = f"https://api.alquran.cloud/v1/surah/{Surah}/ar.alafasy"
            response = requests.get(api_url)
            data = response.json()
            audio_url = data['data']['ayahs'][Ayat-1]['audio']
            print(audio_url)
            return audio_url  
    except Exception as e:
        print("Error:", e)
        return None

def get_ayat_quran(Surah, Ayat=None):
    try:
        if Ayat is None:
            arabic_api_url = f"https://api.alquran.cloud/v1/surah/{Surah}/ar.alafasy"
            response = requests.get(arabic_api_url)
            data = response.json()
            print(data)
            arabic_ayat = [ayah['text'] for ayah in data['data']['ayahs']]
            
            # Fetch Indonesian (id) ayahs
            indonesian_api_url = f"https://api.alquran.cloud/v1/surah/{Surah}/id.indonesian"
            response = requests.get(indonesian_api_url)
            data = response.json()
            indonesian_ayat = [ayah['text'] for ayah in data['data']['ayahs']]
            
            # Fetch English ayahs
            english_api_url = f"https://api.alquran.cloud/v1/surah/{Surah}/en.ahmedali"
            response = requests.get(english_api_url)
            data = response.json()
            english_ayat = [ayah['text'] for ayah in data['data']['ayahs']]
            
            # Construct JSON response
            response_json = {
                "status": 200,
                "message": "success",
                "result": {
                   "index": Surah,
                   "ar": arabic_ayat,
                   "id": indonesian_ayat,
                   "en": english_ayat
                }
            }

            return json.dumps(response_json, indent=4, ensure_ascii=False)
        else:
            arabic_api_url = f"https://api.alquran.cloud/v1/ayah/{Surah}:{Ayat}/ar.alafasy"
            response = requests.get(arabic_api_url)
            data = response.json()
            print(data)
            arabic_ayat = data["data"]["text"]
            
            # Fetch Indonesian (id) ayahs
            indonesian_api_url = f"https://api.alquran.cloud/v1/ayah/{Surah}:{Ayat}/id.indonesian"
            response = requests.get(indonesian_api_url)
            data = response.json()
            indonesian_ayat = data["data"]["text"]
            
            # Fetch English ayahs
            english_api_url = f"https://api.alquran.cloud/v1/ayah/{Surah}:{Ayat}/en.ahmedali"
            response = requests.get(english_api_url)
            data = response.json()
            english_ayat = data["data"]["text"]
            
            # Construct JSON response
            response_json = {
                "status": 200,
                "message": "success",
                "result": {
                   "index": Surah,
                   "ar": arabic_ayat,
                   "id": indonesian_ayat,
                   "en": english_ayat
                }
            }

            return json.dumps(response_json, indent=4, ensure_ascii=False)
        
    except Exception as e:
        print("Error:", e)
        return None
    
def get_list_quran():
    with open("lib/daftar_surah.json", 'r') as file:
        data = json.load(file)
    result = []
    for entry in data["data"]:
        surah_id = str(entry['id'])
        surat_name = entry['surat_name']
        result.append(f"{surat_name}")  # Append formatted string

    response_json = {
        "status": 200,
        "message": "success",
        "result": result
    }

    return json.dumps(response_json, indent=4, ensure_ascii=False)

def get_jadwal(city):
    url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country=Indonesia&method=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            timings = data['data']['timings']
            imsak = timings.get('Imsak', 'N/A')
            terbit = timings.get('Sunrise', 'N/A')
            dzuhur = timings.get('Dhuhr', 'N/A')
            ashar = timings.get('Asr', 'N/A')
            maghrib = timings.get('Maghrib', 'N/A')
            isya = timings.get('Isha', 'N/A')
            tahajud = timings.get('Midnight', 'N/A')
            
            # Parse imsak time string to datetime object
            imsak_time = datetime.datetime.strptime(imsak, "%H:%M")
            # Subtract 2 hours from imsak time
            sahur_time = imsak_time - datetime.timedelta(hours=2)
            # Convert sahur time back to string format
            sahur = sahur_time.strftime("%H:%M")
            
            # Calculate dhuha time
            terbit_time = datetime.datetime.strptime(terbit, "%H:%M")
            dhuha_time = terbit_time + datetime.timedelta(minutes=15)
            dhuha = dhuha_time.strftime("%H:%M")
            
            response_json = {
                "status": 200,
                "message": "success",
                "result": {
                   "wilayah": city,
                   "tanggal": data['data']['date']['readable'],
                   'sahur': sahur,
                   'imsak': imsak,
                   'terbit': terbit,
                   'dhuha': dhuha,
                   'dzuhur': dzuhur,
                   'ashar': ashar,
                   'maghrib': maghrib,
                   'isya': isya,
                   'tahajud': tahajud
                }
            }

            return json.dumps(response_json, indent=4, ensure_ascii=False)
    return None