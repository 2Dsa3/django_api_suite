from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
import datetime

# Create your views here.

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "leads"  # Nombre de la colección en Firebase Realtime Database
    
    def get(self, request):
        try:
            # Obtener una referencia a la colección en Firebase Realtime Database
            ref = db.reference(self.collection_name)
            
            # Utilizar el método get para obtener todos los elementos de la colección
            data = ref.get()
            
            # Si no hay datos, devolver un arreglo vacío
            if data is None:
                data = []
            elif isinstance(data, dict):
                # Convertir el diccionario a una lista de objetos con sus claves
                data = [{"id": key, **value} for key, value in data.items()]
            
            # Devolver un arreglo JSON con los datos y código de estado HTTP 200 OK
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error al obtener datos: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = request.data
            
            # Obtener una referencia a la colección en Firebase Realtime Database
            ref = db.reference(self.collection_name)
            
            # Obtener la fecha y hora actual y formatearla
            now = datetime.datetime.now()
            timestamp = now.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace("am", "a. m.").replace("pm", "p. m.")
            
            # Añadir la fecha formateada al objeto bajo el campo 'timestamp'
            data['timestamp'] = timestamp
            
            # Utilizar el método push para guardar el objeto en la colección
            new_ref = ref.push(data)
            
            # Devolver el ID del objeto guardado y código de estado HTTP 201 Created
            return Response(
                {"id": new_ref.key}, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": f"Error al guardar datos: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
