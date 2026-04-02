import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest
from app.storage import sf_client, groq1_client, groq2_client, get_youtube_videos, save_chat_to_db

router = APIRouter(prefix="/chat", tags=["AI Agents"])

@router.post("/roadmap_architect")  # Changed endpoint name
async def roadmap_architect_chat(request: ChatRequest):
    async def generate():
        full_response = ""
        
        # 1. Save User Message to DB
        asyncio.create_task(
            asyncio.to_thread(save_chat_to_db, 
                              request.user_id, "user", 
                              request.message, "roadmap_architect")
        )
        
        # 2. Define the Architect Persona
        Roadmap_system_prompt = (
            "You are an expert Roadmap Architect and Curriculum Designer. "
            "If the user greets you (e.g., 'hi', 'hello'), respond warmly and ask what skill or project they want to master. "
            "If the user provides a specific topic (e.g., 'Learn Python', 'Build a Startup'), "
            "provide a structured, step-by-step learning path or execution roadmap. "
            "Break it down into: Phase 1 (Foundations), Phase 2 (Core Skills), and Phase 3 (Advanced/Launch). "
            "Keep your tone professional, structured, and encouraging."
        )
        
        # 3. Video Search Logic (Kept existing logic)
        is_greeting = any(word in request.message.lower() for word in ["hi", "hello", "hey"])
        words_count = len(request.message.split())

        video_task = None
        if not is_greeting and words_count > 2:
            video_task = asyncio.create_task(
                asyncio.to_thread(get_youtube_videos, f"{request.message} tutorial roadmap 2025")
            )
        
        # 4. Call DeepSeek ONLY
        try:
            # Using DeepSeek-V3 (deepseek-chat) or R1 (deepseek-reasoner)
            response = await sf_client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1",  # Change to "deepseek-reasoner" if you want to test R1
                messages=[
                    {"role": "system", "content": Roadmap_system_prompt},
                    {"role": "user", "content": request.message}
                ],
                stream=False # Set to True if you want token-by-token streaming later
            )
            
            ai_text = response.choices[0].message.content
            full_response = ai_text
            yield ai_text

        except Exception as e:
            print(f"DeepSeek Error: {e}")
            error_msg = "⚠️ The Roadmap Architect is currently unavailable. Please check your connection."
            full_response = error_msg
            yield error_msg

        # 5. Video Logic Checking
        if video_task:
            try:
                videos = await video_task 
                # Check if the AI response implies a roadmap was generated
                has_roadmap = any(x in full_response.lower() for x in ["phase", "step", "roadmap", "learn"])
                
                if videos and has_roadmap:
                    video_text = "\n\n### 📺 Recommended Video Resources:\n"
                    for v in videos:
                        video_text += f"- [{v['title']}]({v['link']})\n"
                    
                    full_response += video_text
                    yield video_text
            except Exception as e:
                print(f"Video Error: {e}")

        # 6. Save Assistant Response to DB
        asyncio.create_task(
            asyncio.to_thread(save_chat_to_db, request.user_id, "assistant", full_response, "Roadmap Architect")
        )

    return StreamingResponse(generate(), media_type="text/plain")


# --- Lecturer (Async Streaming) ---
@router.post("/Lecturer")
async def lecturer_chat(request: ChatRequest):
    async def generate():
        full_response = ""
        
        lecturer_system_prompt = (
            "You are a highly knowledgeable University Lecturer. "
            "Your primary role is to provide academic explanations and answer student inquiries with high accuracy. "
            "Do not focus on motivational speeches or emotional support. "
            
            "Rule 1: If a student greets you, respond with a professional, brief acknowledgment and ask for their specific academic question. "
            "Rule 2: Provide clear, structured, and factual answers based on established curricula and industry standards. "
            "Rule 3: Use a formal, authoritative, and direct tone. Avoid slang or overly friendly language. "
            "Rule 4: If a student's question is vague, ask for clarification to provide a more precise academic response. "
            "Rule 5: Focus purely on teaching and explaining concepts. Stay on topic."
        )
        
        # Save User Message
        asyncio.create_task(
            asyncio.to_thread(save_chat_to_db, request.user_id, "user", request.message, "Lecturer")
        )

        try:
            # await ကို သုံးပြီး non-blocking ခေါ်ယူမယ်
            response = await groq1_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  
                messages=[
                    {"role": "system", "content": lecturer_system_prompt},
                    {"role": "user", "content": request.message}
                ],
                stream=True
            )
            
            # async for နဲ့ တစ်လုံးချင်းစီ stream လုပ်ပြီး UI ဘက်ကို ပို့မယ်
            async for chunk in response:
                # DeepSeek client structure ပေါ်မူတည်ပြီး choices[0].delta.content ကို ယူပါတယ်
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
                    
            # Save AI Response
            # 2. AI ဖြေတာ ပြီးသွားမှ Database မှာ သိမ်းမယ် (Background Task)
            asyncio.create_task(
                asyncio.to_thread(
                    save_chat_to_db, 
                    request.user_id, 
                    "assistant", 
                    full_response, 
                    "Lecturer (DeepSeek-V3)"
                )
            )
            
        except Exception as e:
            print(f"Lecturer Agent Error: {e}")
            yield f"Lecturer Error: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")

# --- Support (Async JSON Response) ---
@router.post("/support")
async def support_chat(request: ChatRequest):
    
    support_system_prompt = (
        "You are a helpful and professional Customer Support Assistant. "
        "Your goal is to provide clear, concise, and accurate information. "
        "If the user greets you, reply with a warm welcome and ask how you can assist them today. "
        "If they report an issue, be empathetic, acknowledge the problem, and offer a direct solution or next steps. "
        "Keep your responses short and professional."
    )
    
    # Save User Message    
    asyncio.create_task(
        asyncio.to_thread(save_chat_to_db, request.user_id, "user", request.message, "support")
    )
    
    try:
        # await သုံးလိုက်တဲ့အတွက် ဒီ API က အဖြေမပေးခင်မှာ တခြား request တွေကို လက်ခံနိုင်သွားပါပြီ
        response = await groq2_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": support_system_prompt},
                {"role": "user", "content": request.message}
            ]
        )
        
        reply = response.choices[0].message.content
        
        # 2. AI Response ကို Background မှာ သိမ်းမယ်
        asyncio.create_task(
            asyncio.to_thread(
                save_chat_to_db, 
                request.user_id, 
                "assistant", 
                reply, 
                "support (Llama)"
            )
        )
        
        return {"reply": reply}
    except Exception as e:
        print(f"Support Agent Error: {e}")
        return {"error": str(e)}