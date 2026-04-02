from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: Optional[List[dict]] = []      #Type Hinting လို့ခေါ်တဲ့ နည်းလမ်းနဲ့ AI ကို ရှေ့ကပြောခဲ့တဲ့ စကားတွေကို မှတ်မိခိုင်းဖို့ (Memory ပေးဖို့) ရေး

class VideoResponse(BaseModel):
    title: str
    link: str