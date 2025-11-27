from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from crypto import encrypt_text, decrypt_text
from xml_utils import dict_to_xml, xml_to_dict

API_TOKEN = "TOKEN123"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LEGACY_URL = "http://localhost:9000/legacy"


def verify_token(t):
    if t != API_TOKEN:
        raise HTTPException(401, "Token inválido")


@app.post("/api/clientes")
async def cadastrar(payload: dict, Authorization: str = Header("")):
    verify_token(Authorization)
    payload["cpf"] = encrypt_text(payload["cpf"])
    xml_req = dict_to_xml(payload, root="Cliente")
    print("DEBUG XML enviado:", xml_req)
    r = requests.post(f"{LEGACY_URL}/cadastrar", data=xml_req)
    resp = xml_to_dict(r.text)["Resposta"]
    return {"mensagem": "Cliente cadastrado", "id": resp["id"]}


@app.get("/api/clientes/{cid}")
async def consultar(cid: str, Authorization: str = Header("")):
    verify_token(Authorization)
    xml_req = dict_to_xml({"id": cid}, root="Consulta")
    r = requests.post(f"{LEGACY_URL}/consultar", data=xml_req)
    data = xml_to_dict(r.text)["Resposta"]
    if "erro" in data:
        return {"erro": data["erro"]}
    cli = data["Cliente"]
    cli["cpf"] = decrypt_text(cli["cpf"])
    return cli
