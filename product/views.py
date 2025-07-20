from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from django.core.paginator import Paginator

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from django.db import connection
print(connection.settings_dict['ENGINE'])
print(connection.settings_dict['NAME'])

# ---------- CATEGORY ----------
class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- PRODUCT ----------
class ProductListCreateView(APIView):
    def get_permissions(self):
        # Public GET, Admin-only POST
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request):
        # --- Filtering ---
        category = request.GET.get('category')  # category id
        price_min = request.GET.get('price_gte')
        price_max = request.GET.get('price_lte')
        stock_gte = request.GET.get('stock_gte')  # e.g., 1 for in stock

        products = Product.objects.select_related('category').all()

        if category:
            products = products.filter(category__id=category)
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)
        if stock_gte:
            products = products.filter(stock__gte=stock_gte)

        # --- Pagination ---
        paginator = Paginator(products, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = ProductSerializer(page_obj.object_list, many=True)
        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': int(page_number),
            'results': serializer.data
        })

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







































