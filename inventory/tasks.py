from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.db.models import F
from .models import *


@shared_task
def low_stock_alert():
    products = Product.objects.filter(
        current_stock__lt=F('minimum_stock_level')
    )
    for product in products:
        html_message = f"""
        <html>
        <body>
        <h1 style=color: rgb(125, 125, 239);>Low Stock Alert</h1>
        <p style="font-size: medium; color:darkblue;">{product.name} stock is low .</p>
        <p style="font-size: medium; color:darkblue;">current stock: {product.current_stock}.</p>
        </body>
        </html>
        """   

 
        send_mail(
            subject="Low Stock Alert",
            message="stock low",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["devsalimraza@gmail.com"],
            html_message=html_message
        )
        
@shared_task
def stock_in_alert(stock_id):
    stock = StockIn.objects.get(id=stock_id)
    product = stock.product
    
    html_message = f"""
    <html>
    <body ">
    <h1 style=color: rgb(125, 125, 239);>Stock Increased</h1>
    <p style="font-size: medium; color:darkblue;">{product.name} stock updated.</p>
    <p style="font-size: medium; color:darkblue;">new stock quantity: {stock.quantity}.</p>
    <p style="font-size: medium; color:darkblue;">Current stock: {product.current_stock}.</p>
    </body>
    </html>
    """
    send_mail(
        subject="Stock Increased", 
        message="Stock updated",    
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["devsalimraza@gmail.com"],
        html_message=html_message   
    )