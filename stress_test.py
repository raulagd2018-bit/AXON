# stress_test.py
import asyncio
import aiohttp
import time

URL = "http://localhost:8000/api/v1/create_post" # Ajusta según tu puerto

async def simulate_user(session, user_id):
    payload = {
        "user_id": f"user_{user_id}",
        "content_url": "http://video.test",
        "caption": "Prueba de fuego",
        "content_type": "video"
    }
    try:
        async with session.post(URL, json=payload) as response:
            return response.status
    except Exception:
        return 500

async def run_hell_test(n_users):
    async with aiohttp.ClientSession() as session:
        tasks = [simulate_user(session, i) for i in range(n_users)]
        start = time.time()
        results = await asyncio.gather(*tasks)
        end = time.time()
        
        success = results.count(200) + results.count(202)
        print(f"--- RESULTADOS DEL INFIERNO ---")
        print(f"Usuarios simulados: {n_users}")
        print(f"Éxito: {success} | Fallos: {len(results) - success}")
        print(f"Tiempo total: {end - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(run_hell_test(1000))
