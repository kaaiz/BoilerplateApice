from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.models import Contact, ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

"""
The ContactsView will contain the logic on how to:
 GET, POST, PUT or delete the contacts
"""


class ContactsView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, contact_id=None):
        if contact_id is not None:
            contact = Contact.objects.get(Contact, pk=contact_id)
            serializer = ContactSerializer(contact, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            contacts = Contact.objects.all()
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user_id'] = request.user_id
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, contact_id):
        contact = Contact.objects.get(Contact, pk=contact_id)
        data = request.data
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, contact_id):
        contact = Contact.objects.get(Contact, pk=contact_id)
        contact.delete()
        return Response(status=status.HTTP_200_OK)

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'first_name': user.first_name,
            'Last_name': user.Last_name,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_active': user.is_active
        })

    def Logout(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
