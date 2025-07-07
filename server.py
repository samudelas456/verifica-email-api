from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import json
import random
import smtplib
from urllib.parse import parse_qs

# Armazena os códigos temporariamente
codigos = {}

# CONFIGURAÇÕES DO SEU E-MAIL
EMAIL = "vipcinebr@gmail.com"
SENHA = "boao kxzz hqhr unau"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        dados = parse_qs(post_data)

        if self.path == "/enviar_codigo":
            email = dados.get("email", [None])[0]
            if not email:
                self._responder(400, {"erro": "Email não enviado"})
                return

            codigo = str(random.randint(100000, 999999))
            codigos[email] = codigo
            self._enviar_email(email, codigo)
            self._responder(200, {"status": "código enviado"})

        elif self.path == "/verificar_codigo":
            email = dados.get("email", [None])[0]
            codigo = dados.get("codigo", [None])[0]

            if codigos.get(email) == codigo:
                self._responder(200, {"status": "verificado"})
            else:
                self._responder(200, {"status": "inválido"})

        else:
            self._responder(404, {"erro": "Rota não encontrada"})

    def _responder(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        resposta = json.dumps(data)
        self.wfile.write(resposta.encode())

    def _enviar_email(self, para, codigo):
        msg = f"Seu código de verificação é: {codigo}"
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, SENHA)
            server.sendmail(EMAIL, para, f"Subject: Código de Verificação\n\n{msg}")

# Inicia o servidor
print("Servidor rodando em http://localhost:8080")
httpd = HTTPServer(('0.0.0.0', 8080), Handler)
httpd.serve_forever()
