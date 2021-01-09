from django.db import models


class City(models.Model):
    title = models.CharField(max_length=64)


class Company(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='companies')


class Person(models.Model):
    name = models.CharField(max_length=64)
    photo = models.ImageField()
    passport_scan = models.FileField()
    phone = models.CharField(max_length=12)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='persons')
    timestamp = models.DateTimeField()
    email = models.CharField(max_length=64)
