from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from ..services.meili import MeiliClient
import os

router = APIRouter(prefix="/index")

class IndexPayload(BaseModel):
    events: list

@router.post("/")
def index_events(payload: IndexPayload, background_tasks: BackgroundTasks):
    meili = MeiliClient()
    background_tasks.add_task(meili.index_documents, payload.events)
    return {"status": "indexing_started", "count": len(payload.events)}
