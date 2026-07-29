from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  #Prevents deleting a category that still has products
        related_name="products",   #Allows category.products.all().
    )
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    material = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_uz


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="products/",
    )
    is_primary = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.product} Image"