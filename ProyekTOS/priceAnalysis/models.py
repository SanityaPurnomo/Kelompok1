from django.db import models

class Cabe(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Bulan(models.Model):
    cabe = models.ForeignKey(Cabe, on_delete=models.CASCADE)
    bulan = models.IntegerField()
    tahun = models.IntegerField()

    def __str__(self):
        return str(self.bulan) + str(self.tahun)

class Harga(models.Model):
    tgl = models.ForeignKey(Bulan, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.price)

class DataCabe(models.Model):
    data = models.FileField()
