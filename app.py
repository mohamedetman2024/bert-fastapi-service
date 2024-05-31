# from fastapi import FastAPI, Query
# from transformers import BertTokenizer, BertForSequenceClassification
# from pydantic import BaseModel
# import torch

# class Item(BaseModel):
#     text: str

# app = FastAPI()

# # Load your pre-trained BERT model and tokenizer
# tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)

# @app.get("/predict")
# async def predict(text: str = Query(None, min_length=1)):
#     inputs = tokenizer(text, return_tensors="pt")
#     with torch.no_grad():
#         outputs = model(**inputs)
#     prediction = outputs
#     return {"prediction": str(prediction)}

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the BERT NLP Model API"}



from fastapi import FastAPI, Query, BackgroundTasks
from transformers import BertTokenizer, BertForSequenceClassification
from pydantic import BaseModel
import torch
import asyncio
import queue

class Item(BaseModel):
    text: str

app = FastAPI()

# Load your pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)

# Define a queue to store incoming requests
request_queue = queue.Queue()

def process_batch(batch):
    results = []
    for text in batch:
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        prediction = outputs
        results.append({"text": text, "prediction": str(prediction)})
    return results

async def process_requests():
    while True:
        batch = []
        # Dequeue up to 30 requests from the queue or wait until at least one is available
        for _ in range(30):
            try:
                item = request_queue.get_nowait()
                batch.append(item["text"])
            except queue.Empty:
                break

        if batch:
            results = process_batch(batch)
            # Process the results - you might save them to a database, send via WebSocket, etc.
            # For simplicity, we print them here
            print("Processed batch results:", results)


@app.post("/predict")
async def predict(item: Item, background_tasks: BackgroundTasks):
    request_item = {"text": item.text}
    request_queue.put(request_item)
    return {"message": "Request received and added to queue"}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the BERT NLP Model API"}

# Start processing requests asynchronously
asyncio.create_task(process_requests())

