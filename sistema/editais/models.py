from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Municipio(models.Model):
    nome = models.CharField(max_length = 500)
    def __str__(self):
        return f"{self.nome}"


class Produto(models.Model):
    produto = models.CharField(max_length=200)
    descricao = models.TextField()
    def __str__(self):
        return f"{self.produto}"

class Preco(models.Model):
    produto = models.ForeignKey(Produto, on_delete= models.CASCADE)
    quantidade = models.CharField(max_length = 50)
    preco_minimo = models.DecimalField(max_digits=10, decimal_places=4)

class Edital(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete= models.CASCADE)
    numero = models.CharField(max_length=20)
    data_pregao = models.DateField()
    def __str__(self):
        return f"{self.municipio} - {self.numero}"
    class Meta:
         verbose_name_plural  = 'Editais'

class Item(models.Model):
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE)
    item = models.IntegerField()
    produto = models.ForeignKey(Produto, on_delete= models.CASCADE)
    quantidade = models.DecimalField(max_digits=6, decimal_places=3)
    unidade = models.CharField(max_length=2, 
                               choices= [
                                   ('un', 'un'),
                                   ('kg','kg'),
                                   ('g','g'),
                                   ])
    gramatura = models.CharField(max_length=10)
    valor_referencia = models.DecimalField(max_digits=6, decimal_places=3)
    valor_minimo = models.DecimalField(max_digits=6, decimal_places=3)
    valor_arrematado = models.DecimalField(max_digits=6, decimal_places=3)
    opcoes_colocacao= [
        ('1','1º'),
        ('2','2º'),
        ('3','3º'),
        ('4','< 4º',)
    ]
    dif = models.DecimalField(max_digits=4, decimal_places=3, blank= True, null = True)
    def save(self, *args, **kwargs):
        self.dif = self.valor_arrematado - self.valor_minimo
        super().save(*args, **kwargs)

    colocacao = models.CharField(max_length=2, choices=opcoes_colocacao, blank=True, null=True)

    valor_total = models.DecimalField(max_digits=6, decimal_places=3, blank= True, null = True)
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.quantidade is not None and self.valor_arrematado is not None:
            self.valor_total = self.quantidade * self.valor_arrematado
        super().save(force_insert=force_insert, force_update=force_update, *args, **kwargs)

    ganhador = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    obs = models.CharField(max_length=200)
   
    
    def __str__(self):
        return f'{self.item}- {self.edital}'
    class Meta:
        verbose_name_plural = 'Itens'