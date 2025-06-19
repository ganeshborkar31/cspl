
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class OrderNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
        
#         await self.channel_layer.group_add("orders", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("orders", self.channel_name)

#     async def receive(self, text_data):
#         pass  

#     async def send_order_notification(self, event):
#         await self.send(text_data=json.dumps(event["data"]))


# from channels.generic.websocket import AsyncWebsocketConsumer
# from urllib.parse import parse_qs
# from django.contrib.auth.models import AnonymousUser
# from rest_framework.authtoken.models import Token  # Use your token model if using JWT
# from channels.db import database_sync_to_async
# import json

# class OrderNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):

#         query_string = self.scope["query_string"].decode()
#         query_params = parse_qs(query_string)
#         token_key = query_params.get("token", [None])[0]

#         if not token_key:
#             await self.close(code=4001)  
#             return

#         try:
#             token = await self.get_token(token_key)
#             self.scope["user"] = token.user
#         except Exception:
#             await self.close(code=4001)
#             return

#         await self.channel_layer.group_add("orders", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("orders", self.channel_name)

#     async def receive(self, text_data):
#         pass  

#     async def send_order_notification(self, event):
#         await self.send(text_data=json.dumps(event["data"]))

#     @database_sync_to_async
#     def get_token(self, token_key):
#         return Token.objects.get(key=token_key)






from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.response import Response
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async
from django.utils.timezone import now
import json
import time

from .models import ExpireToken, Order

class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = await self.get_user()
        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001)  
        else:
            time.sleep(6)
            await self.channel_layer.group_add("orders", self.channel_name)
            await self.accept()
            print(f"Socket Name: {self.channel_name}")

        # orders = await self.get_orders(1, 10)
        # await self.send_json({"orders": orders})
        
        # await self.send_json({"message": "connected succesfully"})
        
        query_params = parse_qs(self.scope["query_string"].decode())

        page = int(query_params.get("page", [1])[0])
        page_size = int(query_params.get("page_size", [10])[0])
        is_paid = query_params.get("is_paid", [None])[0]
        order_id = query_params.get("order_id", [None])[0]

        if order_id is not None:
            try:
                order_id = int(order_id)
                
            except ValueError:
                order_id = None
                
        orders = await self.get_orders(page, page_size, is_paid, order_id)
        
        await self.send_json({"orders": orders})
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    async def receive(self, text_data):
        if isinstance(self.user, AnonymousUser):
            await self.send_json({"error": "Unauthorized"})
            return

        try:
            data = json.loads(text_data)
            action = data.get("action")

            if action == "get_orders":
                page = int(data.get("page", 1))
                page_size = int(data.get("page_size", 10))
                is_paid = data.get("is_paid", None)
                order_id = data.get("order_id", None)

                orders = await self.get_orders(page, page_size, is_paid, order_id)
                await self.send_json({"orders": orders})

            elif action == "send_message":
                message = data.get("message")
                if message:
                    await self.channel_layer.group_send("orders", {
                        "type": "send_order_notification",
                        "data": message
                    })
                else:
                    await self.send_json({"error": "Missing 'message'"})

            else:
                await self.send_json({"error": "Invalid action"})

        except json.JSONDecodeError as e:
            await self.send_json({"error": "Invalid JSON", "details": str(e)})
            
        except Exception as e:
            await self.send_json({"error": "Server error", "details": str(e)})

    async def send_order_notification(self, event):
        await self.send_json({"notification": event.get("data")})

    @sync_to_async
    def get_user(self):
        query_string = parse_qs(self.scope['query_string'].decode())
        token_key = query_string.get("token", [None])[0]

        if not token_key:
            return AnonymousUser()

        try:
            token = ExpireToken.objects.get(key=token_key)
            
            return token.user if not token.is_expire() else {"message": "Token expired"}
        
        except ExpireToken.DoesNotExist:
            return AnonymousUser()
    

    @sync_to_async
    def get_orders(self, page, page_size, is_paid, order_id):
        qs = Order.objects.select_related("customer").prefetch_related("ordered_items__product").order_by("-order_date")

        if is_paid is not None:
            if str(is_paid).lower() == "true":
                qs = qs.filter(is_paid=True)
            elif str(is_paid).lower() == "false":
                qs = qs.filter(is_paid=False)

        if order_id:
            qs = qs.filter(id=order_id)

        paginator = Paginator(qs, page_size)
        page_obj = paginator.get_page(page)

        result = []
        for order in page_obj:
            items = []
            for item in order.ordered_items.all():
                items.append({
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "qty": item.qty,
                    "price": float(item.price)
                })

            result.append({
                "order_id": order.id,
                "customer_name": order.customer.username,
                "status": order.status,
                "is_paid": getattr(order, "is_paid", False),
                "created_at": order.order_date.isoformat(),
                "items": items,
                "total": float(order.total_amount)
            })

        return {
            "orders": result,
            "page": page,
            "total_pages": paginator.num_pages,
            "total_orders": paginator.count
        }


    @sync_to_async
    def get_orders(self, page, page_size, is_paid=None, order_id=None):
        qs = Order.objects.select_related("customer", "payment").prefetch_related("items__product")

        if order_id:
            qs = qs.filter(id=order_id)

        if is_paid is not None:
            if str(is_paid).lower() == "true":
                qs = qs.filter(payment__status="COMPLETED")
                
            elif str(is_paid).lower() == "false":
                qs = qs.exclude(payment__status="COMPLETED")
        
        paginator = Paginator(qs, page_size)
        
        if page > paginator.num_pages:
            return {"message": f"total {paginator.num_pages} pages available of page size {page_size}"}
        
        page_obj = paginator.get_page(page)
        
        result = []
        for order in page_obj:
            items = []
            
            for item in order.items.all():
                items.append({
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price": float(item.price)
                })

            payment_status = getattr(order.payment, "status", "PENDING")

            result.append({
                "order_id": order.id,
                "customer_name": order.customer.username,
                "status": order.status,
                "is_paid": payment_status == "COMPLETED",
                "created_at": order.order_date.isoformat(),
                "items": items,
                "total": float(order.total_amount)
            })

        time.sleep(5)
        return {
            "orders": result,
            "page": page,
            "total_pages": paginator.num_pages,
            "total_orders": paginator.count
        }

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))

