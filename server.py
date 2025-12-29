import os, re
from decimal import Decimal
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import dropbox

app = FastAPI()

DBX_TOKEN = os.environ["DROPBOX_ACCESS_TOKEN"]
SECRET = os.environ["RENAMER_SECRET"]

dbx = dropbox.Dropbox(DBX_TOKEN)

class Rename(BaseModel):
    dropbox_path: str
    vendor: str
    amount: float
    date_mmddyyyy: str

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"

@app.post("/rename")
def rename(r: Rename, x_renamer_secret: str = Header("")):
    if x_renamer_secret != SECRET:
        raise HTTPException(401)

    vendor = clean(r.vendor)
    amount = f"${Decimal(str(r.amount)):.2f}"
    new_name = f"{vendor}_{amount}_{r.date_mmddyyyy}.pdf"

    folder = r.dropbox_path.rsplit("/", 1)[0]
    new_path = f"{folder}/{new_name}"

    dbx.files_move_v2(r.dropbox_path, new_path, autorename=True)

    return {"status": "ok", "new_name": new_name}
