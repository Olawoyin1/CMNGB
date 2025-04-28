from django.db import models
from users.models import User


# Category choices
CATEGORY_CHOICES = [
    ('programming', 'Programming'),
    ('design', 'Design'),
    ('marketing', 'Marketing'),
    ('writing', 'Writing'),
    ('photography', 'Photography'),
    ('it_support', 'IT Support'),
    ('teaching', 'Teaching'),
    ('customer_service', 'Customer Service'),
]

# Nigerian states for location choices
NIGERIAN_STATES = [
    ('abia', 'Abia'), ('adamawa', 'Adamawa'), ('akwa_ibom', 'Akwa Ibom'),
    ('anambra', 'Anambra'), ('bauchi', 'Bauchi'), ('bayelsa', 'Bayelsa'),
    ('benue', 'Benue'), ('borno', 'Borno'), ('cross_river', 'Cross River'),
    ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('edo', 'Edo'),
    ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('gombe', 'Gombe'),
    ('imo', 'Imo'), ('jigawa', 'Jigawa'), ('kaduna', 'Kaduna'),
    ('kano', 'Kano'), ('katsina', 'Katsina'), ('kebbi', 'Kebbi'),
    ('kogi', 'Kogi'), ('kwara', 'Kwara'), ('lagos', 'Lagos'),
    ('nasarawa', 'Nasarawa'), ('niger', 'Niger'), ('ogun', 'Ogun'),
    ('ondo', 'Ondo'), ('osun', 'Osun'), ('oyo', 'Oyo'),
    ('plateau', 'Plateau'), ('rivers', 'Rivers'), ('sokoto', 'Sokoto'),
    ('taraba', 'Taraba'), ('yobe', 'Yobe'), ('zamfara', 'Zamfara'),
    ('fct', 'FCT - Abuja'),
]

# Job type choices
JOB_TYPE_CHOICES = [
    ('remote', 'Remote'),
    ('contract', 'Contract'),
    ('hybrid', 'Hybrid'),
    ('intern', 'Intern'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True, default='design')

    def __str__(self):
        return dict(CATEGORY_CHOICES).get(self.name, self.name)

class Job(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    company = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    location = models.CharField(max_length=100, choices=NIGERIAN_STATES, default='lagos')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='remote')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget_range = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title




    
class Proposal(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )


    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer')
    cover_letter = models.TextField()
    cv = models.FileField(upload_to='cvs/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
   
    def __str__(self):
        return f"{self.freelancer.username}'s Proposal for {self.job.title}"
    
    

# class Message(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)


#     class Meta:
#         ordering = ['timestamp']


#     def __str__(self):
#         return f"From {self.sender} to {self.recipient}: {self.content[:30]}"

