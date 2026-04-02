from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import issues
from app.middleware.timer import add_process_time_header
import os 
import uvicorn

app = FastAPI(title="EduBridge AI API")

# Middleware 
app.middleware("http")(add_process_time_header)

# CORS Setup (frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "online", "message": "EduBridge AI API is running"}
    
# Routes 
app.include_router(issues.router, prefix="/api/v1")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)