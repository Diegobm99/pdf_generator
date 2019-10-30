from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from post_api import serializers

#import pandas as pd
import csv
import base64
from fpdf import FPDF
import boto3
from botocore.client import Config
#import fpdf


a = []
with open("credentials.csv") as csvfile:
    data = csv.DictReader(csvfile)
    for r in data:
        a.append(r)
BUCKET_NAME = 'pdf.1'
ACCESS_KEY_ID = a[0]['Access key ID']
ACCESS_SECRET_KEY = a[0]['Secret access key']

def create_pdf(nome, cpf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", size=18)
    pdf.cell(95, 38, txt="Teste PDF 1 - Pessoa Física", ln=1, align="C")

    pdf.set_font("helvetica", "BI", size=12)
    pdf.set_x(15)
    pdf.cell(32, 20, txt="Nome: {}".format(nome), ln=1, align="L")
    pdf.set_x(15)
    pdf.cell(28, 0, txt="CPF: {}".format(cpf), ln=1, align="L")

    pdf.output("pdf_teste.pdf")



class HelloApiView(APIView):
    """Teste API View"""

    serializer_class = serializers.HelloSerializers

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function(get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            cpf = serializer.validated_data.get('cpf')

            message = f'Nome: {name}, CPF: {cpf}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class CSV(APIView):
    serializer_class = serializers.csv_input

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            cpf = serializer.validated_data.get('cpf')

            dados = f'Nome: {name}, CPF: {cpf}'

            create_pdf(name, cpf)

            data = open('pdf_teste.pdf', 'rb')

            s3 = boto3.resource(
                's3',
                aws_access_key_id=ACCESS_KEY_ID,
                aws_secret_access_key=ACCESS_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )
            s3.Bucket(BUCKET_NAME).put_object(Key='teste.pdf', Body=data, ACL='public-read')

            b64_pdf = base64.b64encode(open('pdf_teste.pdf', 'rb').read())

            return Response({'dados': dados, 'url': 'https://s3-sa-east-1.amazonaws.com/pdf.1/teste.pdf', 'b64': b64_pdf.decode("utf-8") })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
