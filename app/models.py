from django.db import models

class SongData(models.Model):
	file_id=models.PositiveIntegerField(primary_key=True)
	name=models.CharField(max_length=100)
	duration=models.PositiveIntegerField(default=0)
	uploaded_time=models.CharField(max_length=100)
	class Meta:
		db_table="SongData"

class PodcastData(models.Model):
	file_id=models.PositiveIntegerField(primary_key=True)
	name=models.CharField(max_length=100)
	duration=models.PositiveIntegerField(default=0)
	uploaded_time=models.CharField(max_length=100)
	host=models.CharField(max_length=100)
	class Meta:
		db_table="PodcastData"

class PodcastParticipantsData(models.Model):
	file_id=models.PositiveIntegerField()
	participant=models.CharField(max_length=100)
	class Meta:
		db_table="PodcastParticipantsData"

class AudiobookData(models.Model):
	file_id=models.PositiveIntegerField(primary_key=True)
	title=models.CharField(max_length=100)
	author=models.CharField(max_length=100)
	narrator=models.CharField(max_length=100)
	duration=models.PositiveIntegerField(default=0)
	uploaded_time=models.CharField(max_length=100)
	class Meta:
		db_table="AudiobookData"