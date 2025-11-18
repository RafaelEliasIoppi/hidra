from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

# Senha correta para o ambiente de teste
SENHA_CORRETA = "segredo123"
HASH_CORRETA = hashlib.sha256(SENHA_CORRETA.encode()).hexdigest()

# HTML do formulário de login
HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Login de Teste</title>
</head>
<body>
    <h2>Login de Teste</h2>
    <form method="POST" action="/login">
        <label for="usuario">Usuário:</label>
        <input type="text" id="usuario" name="usuario" placeholder="Usuário"><br><br>

        <label for="senha">Senha:</label>
        <input type="password" id="senha" name="senha" placeholder="Senha"><br><br>

        <input type="submit" value="Entrar">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    # Entrega o formulário
    return render_template_string(HTML)

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    senha = request.form.get("senha", "")

    # Validação simples
    if hashlib.sha256(senha.encode()).hexdigest() == HASH_CORRETA:
        return f"Login bem-sucedido! Bem-vindo, {usuario}."
    else:
        return "Senha incorreta."

if __name__ == "__main__":
    # Rodar no Codespaces na porta 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
