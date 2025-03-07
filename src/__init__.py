from .service.email import EmailService
from .tasks.data import Pipeline, load_data


from dotenv import dotenv_values

ENV = dotenv_values("config.env")

def main():

    data = load_data(ENV['PATH_INPUT'])

    pipeline = Pipeline(data)

    pipeline.required([
        'Data do Pedido',
        'Status do Pedido',
        'Cliente',
        'Valor Total'
        'ID do Pedido'
    ])
    approveds = pipeline.approved()
    formatted_report = pipeline.formated_report_final(approveds)
    
    email = EmailService(
        recipient='yiwiyat698@dwriters.com',
        sender=ENV['EMAIL_USER'],
        password=ENV['EMAIL_PASSWORD'],
        smtp_server=ENV['EMAIL_HOST'],
        smtp_port=ENV['EMAIL_PORT']
    )

    content_block_template = email._load_template('data/template.html', formatted_report)
    email.send_email(content_block_template)
    