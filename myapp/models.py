from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    instock = models.BooleanField(default=True)
    # file
    picture = models.ImageField(upload_to="product", null=True, blank=True)
    specfile = models.FileField(upload_to="specfile", null=True, blank=True)

    def __str__(self):
        return self.title


class ContactList(models.Model):
    topic = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.topic


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100, default="member")
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Action(models.Model):
    contactList = models.ForeignKey(ContactList, on_delete=models.CASCADE)
    actionDetail = models.TextField()

    def __str__(self):
        return self.contactList.topic


class Prompt(models.Model):
    text = models.TextField()
    description = models.CharField(max_length=500, null=True, blank=True)
    version = models.CharField(max_length=50, default="1.0")
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to="prompt_attachments", null=True, blank=True)

    def __str__(self):
        return f"{self.description or 'Prompt'} v{self.version}"

    class Meta:
        ordering = ["-created_at"]


class TestCase(models.Model):
    EXPECTED_TYPE_CHOICES = [
        ("text", "Text"),
        ("json", "JSON"),
        ("python", "Python Code"),
        ("regex", "Regex"),
    ]

    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="test_cases"
    )
    input = models.TextField()
    expected_type = models.CharField(
        max_length=20, choices=EXPECTED_TYPE_CHOICES, default="text"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test case for {self.prompt.description or 'Prompt'}"

    class Meta:
        ordering = ["-created_at"]


class Result(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    output = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    reasoning = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.test_case} - Score: {self.score}/10"

    class Meta:
        ordering = ["-created_at"]
