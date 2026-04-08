class Usuario:
    
    def __init__(self, nome, email, senha, telefone, usuario, status):
        self._nome = nome

        self._email = email
        self._senha = senha
        self._telefone = telefone
        self._usuario = usuario
        self._status = status

        @property
        def nome(self):
            return self._nome

        @nome.setter
        def nome(self, valor):
            self._nome = valor

        @property
        def email(self):
            return self._email

        @email.setter
        def email(self, valor):
            self._email = valor

        @property
        def senha(self):
            return self._senha

        @senha.setter
        def senha(self, valor):
            self._senha = valor

        @property
        def telefone(self):
            return self._telefone

        @telefone.setter
        def telefone(self, valor):
            self._telefone = valor

        @property
        def usuario(self):
            return self._usuario

        @usuario.setter
        def usuario(self, valor):
            self._usuario = valor

        @property
        def status(self):
            return self._status

        @status.setter
        def status(self, valor):
            self._status = valor
    