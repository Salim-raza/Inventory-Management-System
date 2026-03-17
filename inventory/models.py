from django.db import models
from accounts.models import CustomUser
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO
import qrcode
import uuid
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product/", blank=True, null=True)
    barcode = models.CharField(max_length=30, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    minimum_stock_level = models.PositiveIntegerField(default=10)
    current_stock = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def barcode_generate(self):
        string1 = "PRD"
        string2 = uuid.uuid4().hex[:8].upper()
        value = f"{string1}-{self.name[:3].upper()}-{string2}"
        self.barcode = value
    
    # def qrcode_generate(self, *args, **kwargs):
    #     data = self.barcode
    #     self.qr_code = qrcode.make(data)
    #     self.qr_code = self.qr_code.resize((250, 250))
    #     canvas = Image.new('RGB', (290, 290), 'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas_width, canvas_height = canvas.size
    #     qr_width, qr_height = self.qr_code.size
    #     position = ((canvas_width - qr_width) // 2, (canvas_height - qr_height) // 2)
    #     canvas.paste(self.qr_code, position)
    #     canvas.paste(self.qr_code)
    #     fname = f'qr_code-{self.name}'+'.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer, 'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)
    
    def qrcode_generate(self, *args, **kwargs):
        data = self.barcode
        qr_image = qrcode.make(data)
        qr_image = qr_image.resize((250, 250))
    
        # Create canvas
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas_width, canvas_height = canvas.size
        qr_width, qr_height = qr_image.size
        
        # Center the QR code on canvas
        position = ((canvas_width - qr_width) // 2, (canvas_height - qr_height) // 2)
        canvas.paste(qr_image, position)
        
        # Save to buffer
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        buffer.seek(0)  # Important: reset buffer position to beginning
        
        # Save to ImageField
        self.qr_code.save(fname, File(buffer), save=False)
        
        # Clean up
        canvas.close()
        
    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode_generate()
        if not self.qr_code:
            self.qrcode_generate()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}-{self.name}-{self.category}"
    
    
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    manager_contact = models.CharField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="warehouse")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier")
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product.name} -- {self.product.category}"
    
class StockOut(models.Model):
    REASON_CHOICE = [
        ('SALE', 'sale'),
        ('DAMAGE', 'damage'),
        ('EXPIRED', 'expired'),
        ('TRANSFER', 'transfer'),
        ('OTHER', 'other')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    reason = models.CharField(max_length=15, choices=REASON_CHOICE, default='SALE')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
    note = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    

    
    def save(self, *args, **kwargs):

        if self.pk:  # update
            old = StockOut.objects.get(pk=self.pk)
            diff = self.quantity - old.quantity
            self.product.current_stock -= diff
        else:  # create
            self.product.current_stock -= self.quantity

        self.total_price = self.quantity * self.unit_price
        self.product.save()

        super().save(*args, **kwargs)
        

