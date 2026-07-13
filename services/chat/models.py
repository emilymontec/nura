import hashlib
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Workspace(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='workspace')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.email}'s Workspace"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Fields from existing database schema
    plan = models.CharField(max_length=100, default="free")
    daily_messages = models.IntegerField(default=0)
    last_message_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"


class Dataset(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('valid', 'Válido'),
        ('invalid', 'Inválido'),
        ('processing', 'Procesando'),
    ]

    # File storage
    file = models.FileField(upload_to='datasets/%Y/%m/%d/')
    
    # Metadata
    original_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # in bytes
    file_type = models.CharField(max_length=50)  # csv, xlsx, json
    file_hash = models.CharField(max_length=64, unique=True)  # SHA-256
    
    # Timestamps & author
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='datasets')
    
    # Status & validation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    validation_errors = models.JSONField(default=list, blank=True)
    
    # Analysis context
    analysis_context = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} - {self.uploaded_by.email}"

    def save(self, *args, **kwargs):
        # Calculate file hash before saving
        if self.file and not self.file_hash:
            self.file_hash = self._calculate_file_hash()
        super().save(*args, **kwargs)

    def _calculate_file_hash(self):
        sha256_hash = hashlib.sha256()
        for chunk in self.file.chunks():
            sha256_hash.update(chunk)
        return sha256_hash.hexdigest()


class ChatSession(models.Model):
    session_id = models.CharField(max_length=120, unique=True)
    title = models.CharField(max_length=200, default="Nueva sesión")
    rolling_summary = models.TextField(blank=True, default="")
    dataset_context = models.JSONField(default=dict, blank=True)
    dataset_history = models.JSONField(default=list, blank=True)
    decision_notes = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_temporary = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_sessions')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_sessions')
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.session_id


class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ("system", "System"),
        ("user", "User"),
        ("assistant", "Assistant"),
    )

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.session.session_id}:{self.role}"
