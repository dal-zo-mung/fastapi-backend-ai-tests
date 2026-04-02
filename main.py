from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# app folder ထဲက file တွေကို ခေါ်ယူခြင်း
from app.routes import issues
from app.middleware.timer import add_process_time_header
import os 
import uvicorn

# Vercel အတွက် အဓိကကျတဲ့ App Instance
app = FastAPI(title="EduBridge AI API")

# Middleware 
@app.middleware("http")
async def process_time_middleware(request, call_next):
    return await add_process_time_header(request, call_next)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "online", 
        "message": "EduBridge AI API is running on Vercel"
    }
    
# Routes - Prefix သတ်မှတ်ချက်
app.include_router(issues.router, prefix="/api/v1")

# Local မှာ စမ်းသပ်ဖို့အတွက်သာ (Vercel ပေါ်မှာဆိုရင် ဒီအပိုင်းကို ကျော်သွားပါလိမ့်မယ်)
if name == "main":
    PORT = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
