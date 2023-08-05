from llama_cpp import Llama
import os
if ("RUNTIME" in os.environ and os.environ["RUNTIME"] == "GPU"):
    llm = Llama(model_path="./models/llama-13B.q4_0.bin", n_gpu_layers=1, n_ctx=2048 )
else:
    llm = Llama(model_path="./models/llama-13B.q4_0.bin", n_ctx=2048)

def sendReq(input: str, max: int = 32, temp: float = 0.5):
    output = llm.create_completion(input, max_tokens=max, temperature=temp)
    print(output)
    return output["choices"][0]["text"]