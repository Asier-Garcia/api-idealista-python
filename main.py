import requests
import base64

# Variables Globales
client_id = 'b9lhgfyr9fkvojhpsl89p3bctizo2fk9'
client_secret = '8ud8lnorl5K0'

base_url = 'https://api.idealista.com/3.5/'
country = 'es'
language = 'es'
max_items = '50'
operation = 'rent'
property_type = 'homes'
order = 'priceDown'
center = '41.3851,2.1734'
distance = '90000'
sort = 'desc'
maxprice = '100000'


# Obtención del token de acceso
def get_access_token():
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    token_url = "https://api.idealista.com/oauth/token"
    data = {"grant_type": "client_credentials", "scope": "read"}
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    response = requests.post(token_url, data=data, headers=headers, timeout=10)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {response.status_code} - {response.text}")



# Construcción de la URL de búsqueda
def define_search_url(page_num=1):
    url = (
        f"{base_url}{country}/search?operation={operation}"
        f"&maxItems={max_items}&order={order}&center={center}&distance={distance}"
        f"&propertyType={property_type}&sort={sort}&numPage={page_num}&maxPrice={maxprice}&language={language}"
    )
    return url



# Función para realizar la búsqueda en la API
def search_api(url, token):
    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error en la búsqueda: {response.status_code} - {response.text}")



# Proceso principal
try:
    access_token = get_access_token()  # Obtención del token
    search_url = define_search_url()   # Definición de la URL de búsqueda
    result = search_api(search_url, access_token)  # Llamada a la API de búsqueda
    print(result)  # Imprime los resultados obtenidos
except Exception as e:
    print(e)
