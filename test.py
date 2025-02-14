import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"
EMPRESA_TESTE_ID = None
OBRIGACAO_TESTE_ID = None

@pytest.fixture(scope="module")
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

def test_create_empresa(client):
    global EMPRESA_TESTE_ID

    nova_empresa = {
        "nome": "Empresa Teste Nova",
        "email": "teste@email.com",
        "endereco": "Rua Teste, 123",
        "cnpj": "12345778000100",
        "telefone": "81973265467"
    }
    response = client.post("/empresas/", json=nova_empresa)

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == nova_empresa["nome"].lower()
    EMPRESA_TESTE_ID = data["id"]

def test_get_empresas(client):
    response = client.get("/empresas")
    assert response.status_code == 200
    data = response.json()
    assert any(emp["id"] == EMPRESA_TESTE_ID for emp in data)

def test_get_empresa(client):
    response = client.get(f"/empresas/{EMPRESA_TESTE_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == EMPRESA_TESTE_ID

def test_create_obrigacao(client):
    global OBRIGACAO_TESTE_ID

    obrigacao = {
        "nome": "Testing",
        "periodicidade": "Mensal",
        "empresa_id": EMPRESA_TESTE_ID
    }
    response = client.post("/obrigacoes/", json=obrigacao)

    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == obrigacao["nome"].lower()
    assert data["periodicidade"] == obrigacao["periodicidade"].lower()
    OBRIGACAO_TESTE_ID = data["id"]

def test_update_empresa(client):
    empresa_atualizada = {
        "nome": "Empresa Teste Atualizada",
        "email": "atualizado@email.com",
        "endereco": "Rua Nova, 456",
        "cnpj": "12345778000100",
        "telefone": "81973265467"
    }
    response = client.put(f"/empresas/{EMPRESA_TESTE_ID}", json=empresa_atualizada)

    assert response.status_code == 202
    data = response.json()
    assert data["nome"] == empresa_atualizada["nome"].lower()

def test_delete_empresa(client):
    response = client.delete(f"/empresa/{EMPRESA_TESTE_ID}")
    assert response.status_code == 200

    response = client.get(f"/empresas/{EMPRESA_TESTE_ID}")
    assert response.status_code == 404
