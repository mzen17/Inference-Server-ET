from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os

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

@app.get("/")
async def root():
    return {"message": "Working Fine, hash: 0x1234567890"}


@app.post("/encode")
async def encode(input: BasicReq):
    print(secret)
    if (secret is not None and input.key != secret):
        raise HTTPException(status_code=401, detail="Invalid Key")
    return {"embedding":encoder.getEmbeddings(input.message)}


@app.post("/emotion")
async def emotiongen(input: BasicReq):
    print(secret)
    if (secret is not None and input.key != secret):
        raise HTTPException(status_code=401, detail="Invalid Key")
    return {"emotion": emotion.get_emotion(input.message)}

@app.get("/test-emotion")
async def test_emotion_gen():
    return {"emotion": emotion.get_emotion("Hi!!!")}



@app.post("/completion")
async def llamaRequest(input: LlamaReq):
    print(secret)
    if (secret is not None and input.key != secret):
        raise HTTPException(status_code=401, detail="Invalid Key")
    return {"response":llama.sendReq(input.message, input.max, input.temp)}

