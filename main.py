import requests
import base64

# Variables Globales
client_id = 'b9lhgfyr9fkvojhpsl89p3bctizo2fk9'
client_secret = '8ud8lnorl5K0'

BASE_URL = 'https://api.idealista.com/3.5/'
COUNTRY = 'es'
LANGUAGE = 'es'
OPERATION = 'sale' # rent para alquiler
PROPERTY_TYPE = 'homes' # offices, garages, commercial
ORDER = 'priceDown' # priceUp
CENTER = '41.424,2.178'
SORT = 'desc'
DISTANCE = 5000  # Buscar en un radio de 10 km

MAX_ITEMS = 50
MIN_PRICE = 80000
MAX_PRICE = 160000
MIN_SIZE = 50  # m²
MAX_SIZE = 150  # m²
MIN_ROOMS = 2
MAX_ROOMS = 3
# HAS_TERRACE = True
# HAS_LIFT = True
# NEW_DEVELOPMENT = False  # Excluir obra nueva
# FURNISHED = True  # Solo amueblados
# HAS_POOL = False  # Sin piscina
# distance = '90000'
# maxprice = '100000'


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
    """Construye la URL con los filtros personalizados"""
    url = (
        f"{BASE_URL}{COUNTRY}/search?"
        f"operation={OPERATION}&propertyType={PROPERTY_TYPE}&order={ORDER}"
        f"&sort={SORT}&maxItems={MAX_ITEMS}&numPage={page_num}&language={LANGUAGE}"
        f"&maxPrice={MAX_PRICE}&minPrice={MIN_PRICE}"
        f"&minSize={MIN_SIZE}&maxSize={MAX_SIZE}"
        f"&minRooms={MIN_ROOMS}&maxRooms={MAX_ROOMS}"
        # f"&hasTerrace={str(HAS_TERRACE).lower()}"
        # f"&hasLift={str(HAS_LIFT).lower()}"
        f"&center={CENTER}&distance={DISTANCE}"
        # f"&newDevelopment={str(NEW_DEVELOPMENT).lower()}"
        # f"&furnished={str(FURNISHED).lower()}"
        # f"&hasPool={str(HAS_POOL).lower()}"
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


def fetch_and_display_results(pages=1, min_photos=5):
    """Obtiene y muestra propiedades con al menos `min_photos` fotos"""
    try:
        token = get_access_token()

        for page in range(1, pages + 1):
            url = define_search_url(page)
            results = search_api(url, token)

            for property in results.get("elementList", []):
                num_photos = property.get("numPhotos", 0)  # 📷 Número de fotos
                if num_photos < min_photos:
                    continue  # ❌ Saltar anuncios con menos fotos

                property_url = property.get("url", "No disponible")
                address = property.get("address", property.get("neighborhood", "Ubicación no disponible"))
                price = property.get("price", "No disponible")

                print(f"📷 {num_photos} fotos | 🏠 {address} - 💰 {price}€\n🔗 {property_url}\n{'-'*50}")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    fetch_and_display_results(pages=2, min_photos=5)  # 🔍 Buscar con al menos 5 fotos
