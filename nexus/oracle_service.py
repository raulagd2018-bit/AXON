import httpx

class OracleService:
    def __init__(self):
        # Base URL para una API gratuita de datos (ejemplo: CoinGecko para cripto)
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"

    async def process_search(self, query: str):
        # Convertimos la query a minúsculas para normalizar
        search_term = query.lower().strip()
        
        # Lógica de "Sentidos": Si busca bitcoin, llamamos a la API real
        if search_term == "bitcoin":
            async with httpx.AsyncClient() as client:
                try:
                    # Consultamos el precio real de Bitcoin
                    response = await client.get(
                        f"{self.api_url}?ids=bitcoin&vs_currencies=usd"
                    )
                    data = response.json()
                    price = data.get("bitcoin", {}).get("usd", "No disponible")
                    
                    return {
                        "result": f"El precio actual de Bitcoin es ${price} USD",
                        "source": "CoinGecko Real-Time API",
                        "confidence": 1.0
                    }
                except Exception as e:
                    return {"result": "Error al conectar con la fuente de datos", "error": str(e)}
        
        return {
            "result": f"Datos encontrados para: {search_term}",
            "source": "Axioma Oracle Engine (Default)",
            "confidence": 0.5
        }

oracle = OracleService()
