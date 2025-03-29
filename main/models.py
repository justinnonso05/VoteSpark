from django.db import models
from django.contrib.auth.models import User


class Election(models.Model):
    name = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")
    is_ended = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.title

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    votes = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.position.title}"
    

class Voter(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voters')
    voting_id = models.CharField(max_length=12, unique=True)
    email = models.EmailField()
    is_voted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voter {self.voting_id} in {self.election.name}"

