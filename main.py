from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class URLInput(BaseModel):
    url: str

@app.post("/analyze/")
def analyze_url(input_data: URLInput):
    url = input_data.url
    try:
        # Starte das Python-Skript mit übergebener URL
        result = subprocess.run(
            ["python3", "bilder_downloader.py", url],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Debug-Ausgaben im Terminal
        print("SCRIPT STDOUT:\n", result.stdout)
        print("SCRIPT STDERR:\n", result.stderr)

        return {
            "message": "Analyse abgeschlossen.",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.CalledProcessError as e:
        print("FEHLER beim Skriptaufruf:\n", e.stderr)
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Ausführen von bilder_downloader.py: {e.stderr}"
        )
