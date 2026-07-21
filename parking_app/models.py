from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('mall', 'Mall Owner'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class Mall(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='malls', null=True, blank=True)
    mall_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.mall_name

class Complaint(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='complaints')
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='complaints', null=True, blank=True)
    title = models.CharField(max_length=200, default="Feedback")
    text = models.TextField()
    reply = models.TextField(blank=True, null=True)
    is_forwarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint {self.id} by {self.user.full_name}"

# Models mapping to OpenCV parking.py raw SQL table structures:
class Vehicle(models.Model):
    # Mapping to `vehicle` table:
    vehicle_no = models.CharField(max_length=50)
    time_in = models.CharField(max_length=10) # Format: "HH:MM"
    date = models.CharField(max_length=15) # Format: "YYYY-MM-DD"
    
    class Meta:
        db_table = 'vehicle' # exact name expected by SQL script

    def __str__(self):
        return f"{self.vehicle_no} @ {self.date} {self.time_in}"

class Slot(models.Model):
    # Mapping to `slot` table:
    slno = models.CharField(max_length=10, primary_key=True) # Usually '1'
    a = models.CharField(max_length=10, default='0')
    b = models.CharField(max_length=10, default='0')
    c = models.CharField(max_length=10, default='0')
    d = models.CharField(max_length=10, default='0')

    class Meta:
        db_table = 'slot' # exact name expected by SQL script

    def __str__(self):
        return f"Slot Status {self.slno} (a={self.a}, b={self.b}, c={self.c}, d={self.d})"
