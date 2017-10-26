# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_registration.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="subcategories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ForeignKey(Category, related_name="products")
    subcategory = models.ManyToManyField(Subcategory, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)