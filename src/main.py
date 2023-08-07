from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
import time

from dotenv import load_dotenv
load_dotenv()  

type = os.environ["TYPE"] if "TYPE" in os.environ else ""
deploy = os.environ["NODE_ENV"] if "NODE_ENV" in os.environ else ""
secret = os.environ["SECRET"] if "SECRET" in os.environ else None


if secret is None:
    print("WARNING: No secret provided, all requests will be accepted. DO NOT DO THIS IN PRODUCTION")


from src.models.Requests import BasicReq, LlamaReq
if (type == "huggingface"):
    import src.huggingface.emotions as emotion
    import src.huggingface.encoders as encoder
elif (type == "llama"):
    import src.llama.llama as llama
else:
    import src.huggingface.emotions as emotion
    import src.huggingface.encoders as encoder
    import src.llama.llama as llama 


app = FastAPI()
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from prometheus_client import make_asgi_app
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Counter
from prometheus_client import Counter, Info, Gauge

def make_metrics_app():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return make_asgi_app(registry=registry)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Metrics for promotheus
req = Counter('total_requests', 'Total requests to the server.')
embed = Counter('total_embedds', 'Total requests to the embedding server.')
emot = Counter('total_emotions', 'Total requests to the emotion server.')
invalid = Counter('invalid_auth_count', 'Total number of authentication failures.')
llamaReq = Counter('total_llama', 'Total requests to the llama server.')

embed_response_time = Gauge('embed_response_time', 'Average Time for an embedding request to finish')
emotions_response_time = Gauge('emotions_response_time', 'Average Time for an embedding request to finish')
llama_response_time = Gauge('llama_response_time', 'Average Time for an embedding request to finish')


i = Info('sxis_system_data', 'Env variables for SXIS')
i.info({'version': '1.0.0', 'type':type})


@app.get("/")
async def root():
    req.inc()
    return {"message": "Working Fine, hash: 0x1234567890"}


@app.post("/encode")
async def encode(input: BasicReq):
    start = time.time()
    if (secret is not None and input.key != secret):
        invalid.inc()
        raise HTTPException(status_code=401, detail="Invalid Key")
    embed.inc()
    embeddings = encoder.getEmbeddings(input.message)
    embed_response_time.set(time.time() - start)
    return {"embedding":embeddings}


@app.post("/emotion")
async def emotiongen(input: BasicReq):
    start = time.time()
    if (secret is not None and input.key != secret):
        invalid.inc()
        raise HTTPException(status_code=401, detail="Invalid Key")
    emot.inc()
    emotions = emotion.get_emotion(input.message)
    emotions_response_time.set(time.time() - start)
    return {"emotion": emotions}


@app.post("/completion")
async def llamaRequest(input: LlamaReq):
    start = time.time()
    if (secret is not None and input.key != secret):
        invalid.inc()
        raise HTTPException(status_code=401, detail="Invalid Key")
    response = llama.sendReq(input.message, input.max, input.temp)
    llama_response_time.set(time.time() - start)
    return {"response":response}

