from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from xml_utils import xml_to_dict, dict_to_xml

legacy = FastAPI()
FAKE_DATABASE = {}


@legacy.post("/legacy/cadastrar", response_class=PlainTextResponse)
async def cadastrar(req: Request):
    xml = (await req.body()).decode()
    data = xml_to_dict(xml)["Cliente"]

    cid = str(len(FAKE_DATABASE) + 1)
    FAKE_DATABASE[cid] = data

    return dict_to_xml({"status": "OK", "id": cid}, root="Resposta")


@legacy.post("/legacy/consultar", response_class=PlainTextResponse)
async def consultar(req: Request):
    xml = (await req.body()).decode()
    req_data = xml_to_dict(xml)["Consulta"]

    cid = req_data["id"]

    if cid not in FAKE_DATABASE:
        return dict_to_xml({"erro": "Cliente não encontrado"}, root="Resposta")

    return dict_to_xml({"Cliente": FAKE_DATABASE[cid]}, root="Resposta")
