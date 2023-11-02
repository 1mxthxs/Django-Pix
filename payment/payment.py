import crcmod
import qrcode
import os
import base64
from io import BytesIO


class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId, diretorio=''):
        
        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor.replace(',', '.')
        self.cidade = cidade
        self.txtId = txtId
        self.diretorioQrCode = diretorio

        self.nome_tam = len(self.nome)
        self.chavepix_tam = len(self.chavepix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)
        print(self.txtId)
        #print(self.valor_tam)

        self.merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{self.chavepix_tam:02}{self.chavepix}'
        self.transactionAmount_cents = (float(self.valor))
        print(self.transactionAmount_cents)
        self.transactionAmount_tam = f'{self.transactionAmount_cents:02}'
        print(self.transactionAmount_tam)
        self.addDataField_tam = f'05{self.txtId_tam:02}{self.txtId}'

        self.nome_tam = f'{self.nome_tam:02}'
        self.cidade_tam = f'{self.cidade_tam:02}'

        self.payloadFormat = '000201'
        self.merchantAccount = f'26{len(self.merchantAccount_tam):02d}{self.merchantAccount_tam}'
        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.transactionAmount = f'54{len(self.transactionAmount_tam):02d}{self.transactionAmount_tam}'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.nome_tam}{self.nome}'
        self.merchantCity = f'60{self.cidade_tam}{self.cidade}'
        self.addDataField = f'62{len(self.addDataField_tam):02d}{self.addDataField_tam}'
        self.crc16 = '6304'

    def gerarQrCodeBase64(self, payload):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return f'data:image/png;base64,{img_str}'
  
  
   
    def gerarPayload(self):
        # Cria o payload do PIX
        self.payload = (
            f'{self.payloadFormat}'
            f'{self.merchantAccount}'
            f'{self.merchantCategCode}'
            f'{self.transactionCurrency}'
            f'{self.transactionAmount}'
            f'{self.countryCode}'
            f'{self.merchantName}'
            f'{self.merchantCity}'
            f'{self.addDataField}'
            f'{self.crc16}'
        )

        # Gera e anexa o CRC16 ao payload
        self.gerarCrc16(self.payload)
        
        # Retorna a imagem do QR Code em base64
        self.qrcode_base64 = self.gerarQrCodeBase64(self.payload_completa)
        return self.qrcode_base64
      

    
    def gerarCrc16(self, payload):
        crc16_func = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)


        self.crc16Code = hex(crc16_func(str(payload).encode('utf-8')))
  
        self.crc16Code_formatado = str(self.crc16Code).replace('0x', '').upper().zfill(4)


        self.payload_completa = f'{payload}{self.crc16Code_formatado}'


    def gerarPayloadString(self):
        # Retorna o payload PIX como uma string
        return self.payload_completa
    
    def gerarQrCode(self, payload, diretorio):
        dir = os.path.expanduser(diretorio)
        self.qrcode = qrcode.make(payload)
        self.qrcode.save(os.path.join(dir, 'payment', 'qrcode', 'pixqrcodegen.png'))

        
        return print(payload)

"""
if __name__ == '__main__':
    # 12345678900 seria o formato do CPF sem pontos e traços
    
    Payload('Matheus Ricardo', 'matheusricardo164@gmail.com', '13.78', 'Manacapuru', 'Ciborg').gerarPayload()
    
"""
