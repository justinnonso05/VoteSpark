from django.contrib import admin
from .models import Candidate, Voter, Election, Position

admin.site.register(Candidate)
admin.site.register(Voter)
admin.site.register(Election)
admin.site.register(Position)