import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..utils.logger import call_logger

class EmailService:
    def __init__(self, recipient: str, sender: str, password: str, smtp_server: str, smtp_port: int):
        """
        Initializes the ReportEmail class.

        Args:
            recipient (str): Recipient's email address.
            sender (str): Sender's email address.
            password (str): Sender's email password.
            smtp_server (str): SMTP server (e.g., smtp.gmail.com).
            smtp_port (int): SMTP server port (e.g., 587 for TLS).
        """
        self.recipient = recipient
        self.sender = sender
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    
    def template_order(self, data: dict) -> str:

        template_order = f'''
            <div class="order">
                <p class="info">Pedido ID: <span class="highlight">ID_PEDIDO</span></p>
                <p class="info">Cliente: <span class="highlight">CLIENTE</span></p>
                <p class="info">Data do Pedido: <span class="highlight">DATA_PEDIDO</span></p>
                <p class="info">Valor: <span class="highlight">R$ VALOR_PEDIDO</span></p>
            </div>
        '''

        fields = {
            'ID do Pedido': 'ID_PEDIDO',
            'Cliente': 'CLIENTE',
            'Data do Pedido': 'DATA_PEDIDO',
            'Valor Total': 'VALOR_PEDIDO'
        }


        for key, value in fields.items():
            template_order = template_order.replace(value, str(data[key]))

        
        return template_order

    @call_logger('email/load_template')
    def _load_template(self, template_path: str, data: dict) -> str:
        """
        Loads an HTML template from a file and replaces placeholders with actual values.

        Args:
            template_path (str): Path to the HTML template file.
            **kwargs: Key-value pairs to replace placeholders in the template.

        Returns:
            str: The HTML content with placeholders replaced.
        """

        

        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()

        content_block = ""
        for order in data:
            content_block += self.template_order(order)

        # Replace placeholders with actual values
        
        placeholder = '{{orders}}'
        template = template.replace(placeholder, content_block)

        return template


    @call_logger('email/envio')
    def send_email(self, html_content: str):
        """
        Sends an email using an HTML template.

        Args:
            template_path (str): Path to the HTML template file.
            total_orders (int): Total number of approved orders.
            total_amount (float): Total amount of approved orders.
        """
        # Load the HTML template and replace placeholders
       

        # Creating the email message
        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = self.recipient
        message["Subject"] = "Relatorio de Pedidos Aprovados"
        message.attach(MIMEText(html_content, "html"))  # Attach HTML content

        try:
            # Connecting to the SMTP server
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender, self.password)  # Authenticates with the server
                server.sendmail(self.sender, self.recipient, message.as_string())  # Sends the email
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
