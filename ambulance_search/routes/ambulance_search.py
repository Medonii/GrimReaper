from fastapi import FastAPI

ambulance_search = FastAPI()

@ambulance_search.get("/")
    async def get_best_ambulance():



