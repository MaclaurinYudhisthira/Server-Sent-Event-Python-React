# main.py (FastAPI backend)
# from fastapi.staticfiles import StaticFiles
# from bson.objectid import ObjectId
# from starlette.requests import Request
from fastapi import FastAPI, Response, Request
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import asyncio

app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:5173/",  # Update with your React app's URL
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Store active SSE clients and their associated user IDs
active_clients = {}

# SSE endpoint
@app.get("/notifications/sse/{user_id}")
async def sse_endpoint(user_id: str, request: Request):
    async def event_generator():
        client_queue = asyncio.Queue()

        # Create an SSE event
        async def create_event(data):
            event = f"data: {data}\n\n"
            await client_queue.put(event)

        # Add the client and its associated user ID to the active clients dictionary
        active_clients[user_id] = create_event

        try:
            while True:
                event = await client_queue.get()
                yield event
        except asyncio.CancelledError:
            # Remove the client from the active clients dictionary when the connection is closed
            active_clients.pop(create_event, None)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/send_notification/{user_id}")
async def send_notification(user_id: str, notification: dict):
    '''
        Route to send a notification to a specific user
    '''
    if user_id in active_clients:
        asyncio.create_task(active_clients[user_id](notification))
    return {"message": f"Notification sent successfully {user_id}"}

# Homepage route
@app.get("/")
async def home(request: Request):
    return {"Status":"Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
