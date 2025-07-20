from rest_framework import serializers
from .models import CartItem, Order, OrderItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_detail']

    def get_product_detail(self, obj):
        return {
            "name": obj.product.name,
            "price": obj.product.price
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            raise serializers.ValidationError("Cart is empty")

        order = Order.objects.create(user=user, total_price=0)
        total = 0

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        cart_items.delete()  # Clear the cart after placing order
        return order













































# from rest_framework import serializers
# from .models import Order
# from product.models import Product

# class OrderSerializer(serializers.ModelSerializer):
#     products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'products', 'total_price', 'status', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'total_price', 'status', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         products = validated_data.pop('products')
#         user = self.context['request'].user
#         total_price = sum(product.price for product in products)

#         order = Order.objects.create(user=user, total_price=total_price)
#         order.products.set(products)
#         return order