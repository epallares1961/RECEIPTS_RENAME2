import os, re
from decimal import Decimal
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import dropbox

app = FastAPI()

DBX_TOKEN = os.environ["sl.u.AGNWa-Sc0YDlGleA3tsGEBcT6KYzaqWbC5W1BYKIJmaoeWO7omCIuhBpNdPhI8upGc7Yuadmm4Dil2bjvG6Hc-Eja-t8WHR7EDgfLvqHYk9h6QW6lJQVDUeKMBRQYoGqBol6j7CeDDU2VDa6r-IxNc3rA6XEqStK5QlZt5Knw-JDO6Tp2BV8T55FrpktJB2Kv3Ix9lI_GnuGMuDIROCpY5qORLDt2laAJEizyi3Wee7wfP9cqxsQn2rlWU3ApoPLvbwtlyQdN8U9fcKRtkewHGOhbH0nl7vjm3www76Psa--ElMNaiACc-WLME1PWaRf0Y0vun6r0SqV-8PVvXItv3BJwE-yeVc2-njl6sYWCk1wNgwa3-SqgT1a7O1NqoPb1MmJ_J5YJgrUzZcVna-LxbwVFa15SCA1GMDSxabZ7e8ziQKZd38nuTmeK4bTRc9IDw_o_8JN1qhKeQiwCs9H42ft9Ta7mkcY7SA6Auis8dFfD31v8lbDa_kEZO67CEjgvayps-PDZTBwZkfCCYjxZYFpDGRIIlp-K-0NKjK121hrysIyA7kxID5Sbh3LdmtIU1BFCUF0uQoTxCWHldpSmVuPhAyB35-oO5z9xdvijGoMyHB3wH187yFerhrde4680GNbK27Aw4g9JyCV4F9vj6g84JseCPnXVrZqwGRaPq9GnnxlvMssLDeZms7HyfVRSb2-atQr_aXOY6x3A4T9w3O2aiNSVlyR1Ptkce9AQgJRnd3ya_MdJIYaH4aIGeiGT6xCAu6dsNad1Y_R63oJIzL-dwtgDU4lxjK8uDZlxO3jKZKrU1FcqyhyOn8CRZfsXjQcMO1Ep9JdX0-qpncx0eov_Zf0Cda3fkFUnMERPqLnST92kso4onrZZtjqjTx_tRhZ50IUhlnjuq-g_pLt5H1ifO0bx0Lj0cFxJ7a4WI09p9Ri0ot1OtK4Z8EJBik9ocdSApwlNWaDWI-aQsZ0qwSwkoQyvua2OhXSt7JRcXfqZddka4vzpIf6GCEqinqFdZhCEIVqaRmLOVJQIOe1Sj8th4finNnzCVtUrQ268atF3NtOOgXUKOK2YTqADIEDA419ekNeRg6NG542Ui7wsblIz62OzcY7ZqySudhsIepuvwMLeIC-ZpDojw8nQrw6enVL5779XXwBZ-Ya9PqzDIiv628qeoSKtZ-6Ewf9rLV8XiHmZi8egzyVrlfHNXSVthjLxgeDdEs34anLz3uWAH5WOrA573n5eWrz9QkRgeAzxfwKcbtgQeEAjACb0Lmdu5ycOf8WVlD9pniBHMe6G6QgF0rzjZiNxpbZtObZMJ8L3NKqtZvbSaFYabO11g7lIPI"]
SECRET = os.environ["mysecret123"]

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
