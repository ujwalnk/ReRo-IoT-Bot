from fastapi import FastAPI, UploadFile, File
from .runner import Runner
import aiofiles
import asyncio


app = FastAPI()
runner: Runner = Runner()

user_file_path: str = "/rero/iot_bot/app/user_file.py"

# Timeout in minutes
USER_TIMEOUT = 30

prepended_imports = [
    "from app.header.header import dump\n",
    "import signal\n",
    "import time\n",
]

appended_runner = f"""\n\ndef __runner__():
    def handler(signum, frame):
        raise TimeoutError("Function execution timed out")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm({USER_TIMEOUT * 60})

    try:
        main()
    except TimeoutError as e:
        dump("Exception:" + str(e))
    finally:
        signal.alarm(0)
"""


@app.post("/push_code")
async def save_file(file: UploadFile = File(...)):
    global user_file_path

    async with aiofiles.open(user_file_path, "wb") as out_file:
        while content := await file.read(1024):  # Read file in chunks
            await out_file.write(content)

    async with aiofiles.open(user_file_path, "r+") as out_file:
        content = await out_file.read()
        await out_file.seek(0)

        import_lines = "".join(prepended_imports)

        await out_file.write(import_lines + content + appended_runner)

    import importlib.util

    try:
        spec = importlib.util.spec_from_file_location("uf", user_file_path)
        uf = importlib.util.module_from_spec(spec)
        await asyncio.wait_for(
            asyncio.to_thread(spec.loader.exec_module, uf), timeout=1
        )

        global runner
        runner = Runner(uf.__runner__)
        runner.run()

    except asyncio.TimeoutError:
        return {"detail": "Importing user_file timed out"}
    except Exception as e:
        print(e)
        return {"detail": f"An error occurred: {str(e)}"}

    return {"detail": "File saved successfully & running"}


@app.get("/stop_code")
async def stop_bot():
    global runner
    runner.kill()
    print("Stopping code")
    return {"detail": "Bot stopped"}