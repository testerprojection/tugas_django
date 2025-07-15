from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from pos_app.models import (User,Layanan,JenisPembayaran,Pembayaran,StatusModel,Category)
from api.serializers import (RegisterUserSerializer,LoginSerializer,LayananSerializer,JenisPembayaranSerializer,PembayaranSerializer)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login,logout as django_logout
from django.http import HttpResponse , JsonResponse
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .paginators import CustomPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')

class LayananListAPIView(APIView):
    def get(self, request, *args, **kwargs):    
        layanan = Layanan.objects.all()
        serializer= LayananSerializer(layanan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data={
            'code':request.data.get('code'),
            'name':request.data.get('name'),
            'price':request.data.get('price'),
            'description':request.data.get('description'),
        }
        serializer=LayananSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                'status':status.HTTP_201_CREATED,
                'message':'Data Berhasil Dibuat....',
                'data':serializer.data,
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, *args, **kwargs):
        layanan=self.get_object(id)
        if not layanan:
            return Response({
                'status':status.HTTP_400_NOT_FOUND,
                'message':'Data tidak ada....'
            },status=status.HTTP_400_NOT_FOUND)
            
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'description': request.data.get('description'),
        }
        serializer = LayananSerializer(layanan, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LayananDetailAPIView(APIView):
    def get_object(self,pk):
        try:
            return Layanan.objects.get(pk=pk)
        except Layanan.DoesNotExist:
            return None
        
    def get(self, request, pk, *args, **kwargs):
        layanan=self.get_object(pk)
        if not layanan:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Data tidak ditemukan....'
            },status=status.HTTP_404_NOT_FOUND)
            
        serializer=LayananSerializer(layanan)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data ditemukan.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        layanan=self.get_object(pk)
        if not layanan:
            return Response({
                'status':status.HTTP_400_NOT_FOUND,
                'message':'Data tidak ada....'
            },status=status.HTTP_400_NOT_FOUND)
            
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'description': request.data.get('description'),
        }
        serializer = LayananSerializer(layanan, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        layanan = self.get_object(pk)
        if not layanan:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        layanan.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Data berhasil dihapus.'
        }, status=status.HTTP_204_NO_CONTENT)
        
class LayananGetPostAPIView(ListCreateAPIView):
    serializer_class = LayananSerializer
    queryset = Layanan.objects.all()
        
class LayananGetUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = LayananSerializer
    queryset = Layanan.objects.all()

class RegisterUserAPIView(APIView):
    serializer_class=RegisterUserSerializer

    def post(self,request,format=None):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response={
                'status':status.HTTP_201_CREATED,
                'message':'Selamat anda telah terdaftar....',
                'data':serializer.data,
            }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data':serializer.errors,
                },status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    serializer_class=LoginSerializer

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return JsonResponse({
            'status':200,
            'message':'Selamat Berhasil Masuk....',
            'data':{
                'token':token.key,
                'id':user.id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'is_active':user.is_active,
                'is_waitress':user.is_waitress,
            },
        })
        
class JenisPembayaranListAPIView(ListCreateAPIView):
    queryset = JenisPembayaran.objects.all()
    serializer_class = JenisPembayaranSerializer
    
    def get(self, request, *args, **kwargs):
        jenis_pembayaran = JenisPembayaran.objects.all()
        serializer = JenisPembayaranSerializer(jenis_pembayaran, many=True)
        
        response_data = {
            'status': 200,
            'message': 'Data Jenis Pembayaran',
            'data': serializer.data,
            'user': str(request.user),
            'auth': str(request.auth),
        }   
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = JenisPembayaranSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data berhasil dibuat.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return JenisPembayaran.objects.get(pk=pk)
        except JenisPembayaran.DoesNotExist:
            return None

    def put(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ada....'
        }, status=status.HTTP_404_NOT_FOUND)

        serializer = JenisPembayaranSerializer(jenis_pembayaran, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)

        jenis_pembayaran.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Data berhasil dihapus.'
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    
class JenisPembayaranFilterAPI(generics.ListAPIView):
    queryset = JenisPembayaran.objects.all()
    serializer_class = JenisPembayaranSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['status', 'create_on']
    ordering = ['create_on']

class JenisPembayaranDetailAPIView(APIView):
    def get_object(self,pk):
        try:
            return JenisPembayaran.objects.get(pk=pk)
        except JenisPembayaran.DoesNotExist:
            return None
        
    def get(self, request, pk, *args, **kwargs):
        jenis_pembayaran=self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status':status.HTTP_404_NOT_FOUND,
                'message':'Data tidak ditemukan....'
            },status=status.HTTP_404_NOT_FOUND)
            
        serializer=JenisPembayaranSerializer(jenis_pembayaran)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data ditemukan.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        jenis_pembayaran=self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status':status.HTTP_400_NOT_FOUND,
                'message':'Data tidak ada....'
            },status=status.HTTP_400_NOT_FOUND)
            
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'description': request.data.get('description'),
        }
        serializer = JenisPembayaranSerializer(JenisPembayaran, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        jenis_pembayaran.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Data berhasil dihapus.'
        }, status=status.HTTP_204_NO_CONTENT)
        
class PembayaranListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        jenis_pembayaran = JenisPembayaran.objects.all()
        serializer = JenisPembayaranSerializer(jenis_pembayaran, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'price': request.data.get('price'),
            'description': request.data.get('description'),
        }
        serializer = JenisPembayaranSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data berhasil dibuat.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PembayaranListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer

    def list(self, request, *args, **kwargs):  # ✅ Tidak ada spasi ekstra
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": 200,
            "message": "Data ditemukan.",
            "data": serializer.data
        })

class PembayaranRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer
    
class JenisPembayaranDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return JenisPembayaran.objects.get(pk=pk)
        except JenisPembayaran.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan....'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = JenisPembayaranSerializer(jenis_pembayaran)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data ditemukan.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ada....'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = JenisPembayaranSerializer(jenis_pembayaran, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)

        jenis_pembayaran.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Data berhasil dihapus.'
        }, status=status.HTTP_204_NO_CONTENT)
        
class PembayaranGetPostAPIView(ListCreateAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer
    
class PembayaranGetUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer

    def get_object(self, pk):
        try:
            return Pembayaran.objects.get(pk=pk)
        except Pembayaran.DoesNotExist:
            return None
    def get(self, request, pk, *args, **kwargs):
        jenis_pembayaran = self.get_object(pk)
        if not jenis_pembayaran:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = JenisPembayaranSerializer(jenis_pembayaran)
        response = {    
            'status': status.HTTP_200_OK,
            'message': 'Data ditemukan.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    

    
class PembayaranDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            pembayaran = Pembayaran.objects.get(pk=pk)
            serializer = PembayaranSerializer(pembayaran)
            return Response({   
                'status': status.HTTP_200_OK,
                'message': 'Data ditemukan.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Pembayaran.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk, *args, **kwargs):
        try:
            pembayaran = Pembayaran.objects.get(pk=pk)
            serializer = PembayaranSerializer(pembayaran, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Data berhasil diperbarui.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pembayaran.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, pk, *args, **kwargs):
        try:
            pembayaran = Pembayaran.objects.get(pk=pk)
            pembayaran.delete()
            return Response({
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Data berhasil dihapus.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Pembayaran.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data tidak ditemukan.'
            }, status=status.HTTP_404_NOT_FOUND)
            
            