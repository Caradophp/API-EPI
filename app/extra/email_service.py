import smtplib
from email.message import EmailMessage

class Email:
    
    @staticmethod
    def enviar_email_acesso(nome_usuario, nome_acesso, senha_acesso, email_destinatario):
        msg = EmailMessage()
        msg['Subject'] = 'Acesso ao sistema'
        msg['From'] = 'contatolucianofriebe@gmail.com'
        msg['To'] = email_destinatario
        
        msg.add_alternative(f"""
                            
                            Olá, <strong>{nome_usuario}</strong>, segue abaixo o o seu usuário e senha para acesso ao sistema, esse é um email automático, por favor não responda.
                            <br><br>
                            Usuário: {nome_acesso}<br>
                            Senha: {senha_acesso}
                            
                            """, subtype='html')
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('contatolucianofriebe@gmail.com', 'upnv kpow uwyj aohv ')
            server.send_message(msg)