import json
import re
import smtplib
from email.message import EmailMessage
from os import path


class User():
    """Classe User representa o usuário do sistema de estoque do Kumon Passaré. O usuário tem
    como atributos, nome, email e senha."""

    def __init__(self, nome=None, email=None, senha=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.log = False

    @property
    def nome(self):
        # Retorna nome
        if self._nome is None:
            return None
        return self._nome.title()

    @nome.setter
    def nome(self, nome):
        # Validação do atributo nome
        if nome is None:
            self._nome = nome
        else:
            if nome and nome.strip():
                # Verifica se strings não são vazias = "" ou = " "
                self._nome = nome.lower()
            else:
                print("Preencha todos os campos")

    @property
    def email(self):
        # Retorna email
        if self._email is None:
            return None
        return self._email

    @email.setter
    def email(self, email):
        # Validação do atributo email
        if email is None:
            self._email = email
        else:
            if email and email.strip():
                # Verifica se strings não são vazias = "" ou = " "
                emailregex = re.compile(r"[^@]+@[^@]+\.[^@]+")
                if not emailregex.match(email):
                    print("Email Inválido!")
                else:
                    self._email = email
            else:
                print("Preencha todos os campos")

    @property
    def senha(self):
        # Retorna senha
        if self._senha is None:
            return None
        return self._senha

    @senha.setter
    def senha(self, senha):
        # Validação do atributo senha
        if senha is None:
            self._senha = senha
        else:
            if senha and senha.strip():
                # Verifica se strings não são vazias = "" ou = " "
                if len(str(senha)) >= 5:
                    self._senha = str(senha)
                else:
                    print("Senha muito pequena!")
            else:
                print("Preencha todos os campos")

    @property
    def log(self):
        # Retorna log
        return self._log

    @log.setter
    def log(self, log):
        # 'Setta' log
        self._log = log

    def cadastrar(self):
        # Método responsável por adicionar o objeto a um arquivo json
        if None in vars(self).values():
            print("Não é possível cadastrar usuário!")
            return
        try:
            with open(path.join(".", "models", "Cadastrados.json"), "r") as js:
                user = json.load(js)
                for dicts in user["Users"]:
                    if self._email in dicts.values():
                        print("Email já cadastrado!")
                        return
                userDict = vars(self).copy() # O mesmo que self.__dict__
                del userDict["_log"]
                user["Users"].append(userDict)
            dados = json.dumps(user, indent=4)
            try:
                with open(path.join(".", "models", "Cadastrados.json"), "w") as js:
                    js.write(dados)
            except FileNotFoundError:
                print("Arquivo 'Cadastrados.json' não encontrado!")
        except FileNotFoundError:
            print("Arquivo 'Cadastrados.json' não encontrado!")

    @staticmethod
    def mandarEmail(email, senha):
        # Método auxiliar responsável por enviar o email com a senha correspondente ao User
        msg = EmailMessage()
        msg.set_content(f'Sua senha é: {senha}')
        msg['Subject'] = 'Senha Estoque-Kumon'
        msg['From'] = "recuperasenhakumon@gmail.com"
        msg['To'] = email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("recuperasenhakumon@gmail.com", "kumon32891044")
        server.send_message(msg)
        server.quit()
        return f"Senha enviada para o email {email}"

    def recuperarPass(self, email):
        # Método para recuperar a senha a partir do email
        try:
            with open(path.join(".", "models", "Cadastrados.json"), "r") as js:
                dados = json.load(js)
                for dicts in dados["Users"]:
                    if dicts["_email"] == email:
                        return self.mandarEmail(email, dicts["_senha"])
                print("Email não cadastrado!")
        except FileNotFoundError:
            print("Arquivo 'Cadastrados.json' não encontrado!")

    def login(self, email, senha):
        # Método responsável por logar User
        if self.log is True:
            print("Usuário já está logado!")
        else:
            try:
                with open(path.join(".", "models", "Cadastrados.json"), "r") as js:
                    dados = json.load(js)
                    for dicts in dados["Users"]:
                        if dicts["_email"] == email and dicts["_senha"] == senha:
                            self.nome = dicts["_nome"]
                            self.email = dicts["_email"]
                            self.log = True
                            return
                    print("Email ou senha inválidos!")
            except FileNotFoundError:
                print("Arquivo 'Cadastrados.json' não encontrado!")

    def logout(self):
        # Método de logout do User
        if self.log is False:
            print("Usuário não está logado!")
        else:
            self.log = False

    def __str__(self):
        return f"User: {self.nome} - Logado? {self.log}"

    def __repr__(self):
        return f"User: {self.nome} - Logado? {self.log}"


'''if __name__ == "__main__":
    a = User("Rafael de Almeida Menezes", "rafael@gmail.com", "123456")
    a.cadastrar()'''
