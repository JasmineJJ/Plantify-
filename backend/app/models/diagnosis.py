from tortoise.models import Model
from tortoise import fields

class Diagnosis(Model):
    id = fields.IntField(pk=True)
    
    # Relationship to plant
    plant = fields.ForeignKeyField(
        "models.Plant",
        related_name="diagnoses",
        on_delete=fields.CASCADE
    )
    
    # Diagnosis results
    disease_name = fields.CharField(max_length=200)
    confidence_score = fields.FloatField()  # 0.0 to 1.0
    image_path = fields.CharField(max_length=500)
    
    # Additional metadata
    notes = fields.TextField(null=True)
    is_healthy = fields.BooleanField(default=False)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "diagnoses"
    
    def __str__(self):
        return f"Diagnosis({self.disease_name} - {self.confidence_score:.2f})"