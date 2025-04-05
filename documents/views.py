from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser , JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class ProtectedCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Token valid"}, status=200)

class LoginViewSet(TokenObtainPairView):
    permission_classes = [AllowAny]  

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser , JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  
    filterset_fields = ['category']  
    search_fields = ['file', 'extracted_text']  
    ordering_fields = ['uploaded_at', 'confidence_score']

    def get_queryset(self):
        """Ensure users can only access their own documents."""
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Associate the uploaded document with the logged-in user."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Allow users to manually override the document category."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], permission_classes=[permissions.IsAuthenticated])
    def update_category(self, request, pk=None):
        """API Endpoint to update document category manually."""
        try:
            document = self.get_object()
            new_category = request.data.get("category")

            if new_category not in dict(Document.CATEGORY_CHOICES):
                return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

            document.category = new_category
            document.save()
            return Response({"message": "Category updated successfully", "category": document.category}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
