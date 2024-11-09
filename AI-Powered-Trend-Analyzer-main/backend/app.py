from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Load LLaMA model and tokenizer
model_name = "meta-llama/LLaMA-2-7b-chat"  # Update to your specific model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

class UserInput(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(user_input: UserInput):
    inputs = tokenizer(user_input.text, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_length=150)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": response}
