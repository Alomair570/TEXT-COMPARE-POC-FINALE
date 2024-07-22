
import operator
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import csv

from concurrent.futures import ThreadPoolExecutor
import asyncio

from ar_similarities import get_score

app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000",
#     "http://localhost:8000",
#     "localhost:8000",
#     "http://backend",
#     "backend",
#     "http://host.docker.internal:3000", 
#     "host.docker.internal:3000",
#     "http://localhost:8080",
#     "localhost:8080",
#     "http://njinx",
# ]

# #setup CORS 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials = True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# primary = ""
results = []

@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/comparison/{secondary}/{primary}")
async def return_result(secondary:str,primary: str, request: Request):
    my_header = request.headers.get('access-control-allow-origin')
    print(my_header)
    print("primary" + primary)
    print("secondady"+ secondary)
    score, reasons_list = get_score(primary, secondary)
    reasons = ", ".join(reasons_list)  # Join the list into a single string
    return {"score": score, "reasons": reasons}

@app.post("/uploadfile/{primary}")
async def run_task_in_background(primary: str, file: UploadFile = File(...)):
    # Create and start a background thread to run the task
    file_path = f"/tmp/{file.filename}"  # Save the file temporarily
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    results.clear()
    await create_upload_file(primary, file_path)
    # print(results)
    sorted_list = sorted(results, key=operator.itemgetter('score'))
    sorted_list.reverse()
    return sorted_list

# # Background task function
# async def run_background_task(primary: str, file: str):
    
    
def process_chunk(primary: str, chunk):
    for name in chunk:
        score, reasons_list = get_score(primary, name)
        reasons = ", ".join(reasons_list)  # Join the list into a single string
        if (score != 0):
            word = {"word": name, "score": score, "reasons": reasons}
            results.append(word)

async def create_upload_file( primary: str, file_path: str):
    # print(file.file.readlines())
    chunk_size = 300000  # Adjust as needed
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip header if present

        executor = ThreadPoolExecutor(max_workers=1)  # Adjust max_workers as needed
        loop = asyncio.get_running_loop()
        futures = []

        chunk = []
        for row in csv_reader:
            name = row[0]  # Assuming a single column CSV
            chunk.append(name)
            if len(chunk) >= chunk_size:
                futures.append(loop.run_in_executor(executor, process_chunk, primary, chunk[:]))
                chunk = []

        # Process the last chunk
        if chunk:
            futures.append(loop.run_in_executor(executor, process_chunk, primary, chunk[:]))

        # Wait for all futures to complete
        await asyncio.gather(*futures)