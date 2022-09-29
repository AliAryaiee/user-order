from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, permissions, status

from . import serializers, models


class OrderView(APIView):
    """
        docstring
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
            Register A New Order

            POST ~ /auth/order/register
            User Input Schema
            {
                "address": "Client's Address",
                "description": "Client's Description"
            }

            Response Schema
            status 200
            {
                "id": int,
                "client": int
                "address": "Client's Address",
                "description": "Client's Description",
                "client_score": 0,
                "expert_score": 0,
                "order_price": 0,
                "is_arrived": false,
                "status": 0,
                "comission": 0,
                "tax": 0,
                "payment": "CR",
                "register_time": "2022-09-29T05:12:20.629865Z",
                "finish_time": "2022-09-29T05:12:20.629865Z",
            }

        """
        init_data = {
            "client": request.user.id,
            "description": request.data["description"],
            "address": request.data["address"]
        }
        serialized_order = serializers.OrderSerializer(data=init_data)
        serialized_order.is_valid(raise_exception=True)
        serialized_order.save()

        return Response(serialized_order.data)


class UserOrders(APIView):
    """
        User Orders
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_user_orders(self, user_id: int):
        """
            docstring
        """
        try:
            return models.Order.objects.filter(client=user_id)
        except:
            return None

    def get(self, request):
        """
            Get List of User's Orders
        """
        orders = self.get_user_orders(request.user.id)
        serialized_orders = serializers.OrderSerializer(
            instance=orders,
            many=True
        )

        return Response(serialized_orders.data)
