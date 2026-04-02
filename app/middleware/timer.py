import time
from fastapi import Request

async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Response Header မှာ ကြာချိန်ကို ထည့်ပေးခြင်း
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Path: {request.url.path} | Time: {process_time:.4f}s")
    return response