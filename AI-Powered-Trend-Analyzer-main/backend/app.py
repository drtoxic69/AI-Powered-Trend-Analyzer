from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from pymongo import MongoClient
import torch
import uuid
from typing import List

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_database"]
chat_collection = db["chats"]

# Load LLaMA model and tokenizer
model_name = "meta-llama/LLaMA-2-7b-chat"  # Update to your specific model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

class UserInput(BaseModel):
    text: str
    session_id: str = None  # Optional session ID to keep track of chat history

@app.post("/generate")
async def generate_text(user_input: UserInput):
    # If no session ID is provided, create a new one
    session_id = user_input.session_id or str(uuid.uuid4())

    # Process input with LLaMA
    inputs = tokenizer(user_input.text, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_length=150)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Save user input and model response in MongoDB
    chat_record = {
        "session_id": session_id,
        "user_message": user_input.text,
        "bot_response": response_text
    }
    chat_collection.insert_one(chat_record)

    return {"session_id": session_id, "response": response_text}

@app.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieve chat history for a specific session."""
    history = list(chat_collection.find({"session_id": session_id}, {"_id": 0}))
    return {"session_id": session_id, "history": history}

@app.get("/sessions")
async def get_all_sessions():
    """Retrieve all unique session IDs."""
    sessions = chat_collection.distinct("session_id")
    return {"sessions": sessions}
