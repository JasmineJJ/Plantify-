from tortoise.models import Model
from tortoise import fields

class Plant(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    species = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    
    # Relationship to user
    user = fields.ForeignKeyField(
        "models.User", 
        related_name="plants",
        on_delete=fields.CASCADE
    )
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "plants"
    
    def __str__(self):
        return f"Plant({self.name} - {self.species})"