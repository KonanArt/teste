# Middleware WebService Criptografia

Rodar legado:
uvicorn legacy_system:legacy --port 9000

Rodar middleware:
uvicorn main:app --reload

Token:
Authorization: TOKEN123


# **Visão geral**

O projeto tem 2 serviços:

Cliente → Middleware (FastAPI) → Sistema Legado Simulado


### ✔ O *Cliente* (Postman, Insomnia ou frontend) envia JSON.

### ✔ O *Middleware* converte para XML + criptografa CPF.

### ✔ O *Sistema Legado* recebe XML → devolve XML.

### ✔ O Middleware descriptografa e devolve JSON ao cliente.



# **1. Como o código funciona (explicação por arquivos)**



# **main.py — O Middleware (sua API REST)**

É o serviço principal. Ele expõe:

### **POST /api/clientes** → Cadastrar cliente

### **GET /api/clientes/{id}** → Consultar cliente

Toda requisição precisa do token:


Authorization: TOKEN123


### **Fluxo do cadastro (POST)**

1. Recebe JSON:


{
  "nome": "João",
  "email": "joao@gmail.com",
  "cpf": "12345678900"
}


2. Criptografa o CPF → AES
3. Converte dados para XML
4. Envia o XML para o legado:


POST http://localhost:9000/legacy/cadastrar


5. O legado retorna XML com:


<Resposta><status>OK</status><id>1</id></Resposta>


6. Middleware devolve JSON:

{
  "mensagem": "Cliente cadastrado",
  "id": "1"
}



### **Fluxo da consulta (GET)**

1. Recebe `/api/clientes/1`
2. Monta XML:

<Consulta><id>1</id></Consulta>


3. Envia ao legado
4. Legado devolve XML com CPF criptografado
5. Middleware descriptografa o CPF
6. Devolve JSON ao cliente:

{
  "nome": "João",
  "email": "joao@gmail.com",
  "cpf": "12345678900"
}



#  **legacy_system.py — Sistema Legado Simulado**

Ele recebe XML e:

* no **cadastrar**, guarda o cliente em um *banco fake* (`FAKE_DATABASE`)
* no **consultar**, devolve o cliente em XML

Ele não entende JSON.
Ele não sabe criptografar.
Ele **só recebe e devolve XML**.



#  **crypto.py — Criptografia AES**

Aqui ficam as funções:

* `encrypt_text()` → criptografa um texto (CPF)
* `decrypt_text()` → descriptografa o texto

Usa AES-256 com CBC + PKCS7 padding.

Exemplo:


"12345678900" → "Ad31XaB7...."




#  **xml_utils.py — Conversão XML ↔ Dict**

* `dict_to_xml()` → transforma JSON/dict em XML
* `xml_to_dict()` → transforma XML em dict

Exemplo:

Dict:


{ "nome": "João" }

Vira XML:

<Cliente><nome>João</nome></Cliente>




#  **2. Como rodar o projeto**

### 1️ Rodar o sistema legado:


uvicorn legacy_system:legacy --port 9000


### 2️ Rodar o middleware:


uvicorn main:app --reload




#  **3. Como cadastrar um cliente**

Use Postman ou Insomnia:

### **POST**


http://localhost:8000/api/clientes


### **Headers**


Authorization: TOKEN123
Content-Type: application/json


### **Body (JSON)**

{
  "nome": "Maria Silva",
  "email": "maria@gmail.com",
  "cpf": "98765432100"
}


### ✔ Resposta esperada:

{
  "mensagem": "Cliente cadastrado",
  "id": "1"
}




#  **4. Como consultar um cliente**

### **GET**


http://localhost:8000/api/clientes/1


### **Headers**


Authorization: TOKEN123


###  Resposta esperada:

{
  "nome": "Maria Silva",
  "email": "maria@gmail.com",
  "cpf": "98765432100"
}



#  **5. Exemplos completos dos XML**

### **XML que o Middleware envia para o Legado (cadastro)**

<Cliente>
    <nome>Maria Silva</nome>
    <email>maria@gmail.com</email>
    <cpf>KF88asd8...==</cpf>
</Cliente>


### **XML do Legado (resposta)**

<Resposta>
    <status>OK</status>
    <id>1</id>
</Resposta>


### **XML da consulta enviado ao Legado**

<Consulta>
    <id>1</id>
</Consulta>


### **XML que o legado devolve**

<Resposta>
    <Cliente>
        <nome>Maria Silva</nome>
        <email>maria@gmail.com</email>
        <cpf>KF88asd8...==</cpf>
    </Cliente>
</Resposta>
