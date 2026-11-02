from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    edition = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.title

class Address(models.Model):
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city


class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name


class Lab9Book(models.Model):
    title = models.CharField(max_length=100)

    price = models.FloatField(default=0.0)

    quantity = models.IntegerField(default=1)

    pubdate = models.DateTimeField()

    rating = models.SmallIntegerField(default=1)

    publisher = models.ForeignKey(
        Publisher,
        null=True,
        on_delete=models.SET_NULL
    )

    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title