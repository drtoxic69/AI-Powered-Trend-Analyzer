from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query_data import query_rag


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(user_input: UserInput):
    try:
        # Use query_rag directly instead of the previous implementation
        response = query_rag(user_input.text)

        return {
                    "response": response["response"],
                    "sources": response["sources"]
                }

    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
