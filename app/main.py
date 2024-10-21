from fastapi import FastAPI, HTTPException, UploadFile, File

import aiofiles
import requests
import subprocess
import sys
import os

app = FastAPI()

user_file_path = "/rero/iot_bot/app/user_file.py"

@app.post("/push_code")
async def save_file(file: UploadFile = File(...)):
    global user_file_path

    async with aiofiles.open(user_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # Read file in chunks
            await out_file.write(content)

    async with aiofiles.open(user_file_path, 'r+') as out_file:
        content = await out_file.read()
        await out_file.seek(0)
        await out_file.write("from app.controller.header import dump\n" + content)

    # try:
    #     result = subprocess.run(["python3", f"/tmp/{file.filename}"], capture_output=True, text=True, check=True)
    #     push_2_server(result.stdout, "print")
    # except subprocess.CalledProcessError as e:
    #     push_2_server(e.stderr, "error")

    import os 

    print(os.getcwd())

    import app.user_file as uf
    uf.main()
        
    return {"detail": "File saved successfully & running"}


def push_2_server(value: str, type: str):
    """
    Push value to the server with type
    
    @param:
        - value (str): Value to be sent
        - type (str): Type of value being sent (error / print)

    """

    url = ""

    if type == "error":
        url = "http://localhost/iot/dump"
    elif type == "print":
        url = "http://localhost:8080/iot/exception"

    params = {"value": value}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to push to server")
    
    return response.json()