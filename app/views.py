from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import datetime
from app.models import *
from django.db import IntegrityError

def getFileID():
	x=1
	while SongData.objects.filter(file_id=x).exists() or PodcastData.objects.filter(file_id=x).exists() or AudiobookData.objects.filter(file_id=x).exists():
		x=x+1
	return x

@csrf_exempt
@api_view(["POST"])
def createaudio(request):
	data=request.data
	audioFileType=data['audioFileType']
	audioFileMetadata=data['audioFileMetadata']
	try:
		if audioFileType == 'Song':
			SongData(
				file_id=getFileID(),
				name=audioFileMetadata['name'],
				duration=int(audioFileMetadata['duration']),
				uploaded_time=audioFileMetadata['uploaded_time']
			).save()
			content = {'msg':'Song Created Successfully'}
			return Response(content, status=status.HTTP_200_OK)
		elif audioFileType == 'Podcast':
			id_=getFileID()
			PodcastData(
				file_id=id_,
				name=audioFileMetadata['name'],
				duration=int(audioFileMetadata['duration']),
				uploaded_time=audioFileMetadata['uploaded_time'],
				host=audioFileMetadata['host']
			).save()
			try:
				part=audioFileMetadata['participants']
			except:
				part=None
			if part != None and len(part) > 0:
				for x in audioFileMetadata['participants']:
					PodcastParticipantsData(
						file_id=id_,
						participant=x
					).save()
			content = {'msg':'Podcast Created Successfully'}
			return Response(content, status=status.HTTP_200_OK)
		elif audioFileType == 'Audiobook':
			AudiobookData(
				file_id=getFileID(),
				title=audioFileMetadata['title'],
				author=audioFileMetadata['author'],
				duration=int(audioFileMetadata['duration']),
				uploaded_time=audioFileMetadata['uploaded_time'],
				narrator=audioFileMetadata['narrator']
			).save()
			content = {'msg':'Audiobook Created Successfully'}
			return Response(content, status=status.HTTP_200_OK)
		else:
			content = {'msg':'Incorrect Audio FIle Type'}
			return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	except IntegrityError:
		content = {'msg':"Duration Can't be Negative"}
		return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["POST"])
def deleteaudio(request):
	data=request.data
	try:
		audioFileID=data['audioFileID']
	except KeyError:
		audioFileID=None
	try:
		audioFileType=data['audioFileType']
	except KeyError:
		audioFileType=None
	if audioFileID != None:
		SongData.objects.filter(file_id=audioFileID).delete()
		PodcastData.objects.filter(file_id=audioFileID).delete()
		PodcastParticipantsData.objects.filter(file_id=audioFileID).delete()
		AudiobookData.objects.filter(file_id=audioFileID).delete()
		content = {'msg':'Audio Deleted Successfully'}
		return Response(content, status=status.HTTP_200_OK)
	elif audioFileType != None:
		if audioFileType == 'Song':
			SongData.objects.all().delete()
		elif audioFileType == 'Podcast':
			PodcastData.objects.all().delete()
			PodcastParticipantsData.objects.all().delete()
		elif audioFileType == 'Audiobook':
			AudiobookData.objects.all().delete()
		else:
			content = {'msg':'Incorrect Audio FIle Type'}
			return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		content = {'msg':'Atleast One Input is Required'}
		return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["POST"])
def updateaudio(request):
	data=request.data
	audioFileID=data['audioFileID']
	audioFileMetadata=data['audioFileMetadata']
	try:
		if audioFileID != None:
			if SongData.objects.filter(file_id=audioFileID).exists():
				SongData.objects.filter(file_id=audioFileID).update(
					name=audioFileMetadata['name'],
					duration=int(audioFileMetadata['duration']),
					uploaded_time=audioFileMetadata['uploaded_time']
				)
			elif PodcastData.objects.filter(file_id=audioFileID).exists():
				PodcastData.objects.filter(file_id=audioFileID).update(
					name=audioFileMetadata['name'],
					duration=int(audioFileMetadata['duration']),
					uploaded_time=audioFileMetadata['uploaded_time'],
					host=audioFileMetadata['host']
				)
				try:
					part=audioFileMetadata['participants']
				except:
					part=None
				if part != None and len(part) > 0:
					PodcastParticipantsData.objects.filter(file_id=audioFileID).delete()
					for x in audioFileMetadata['participants']:
						PodcastParticipantsData(
							file_id=audioFileID,
							participant=x
						).save()
			elif AudiobookData.objects.filter(file_id=audioFileID).exists():
				AudiobookData.objects.filter(file_id=audioFileID).update(
					title=audioFileMetadata['title'],
					author=str(audioFileMetadata['author']),
					duration=int(audioFileMetadata['duration']),
					uploaded_time=audioFileMetadata['uploaded_time'],
					narrator=audioFileMetadata['narrator']
				)
			else:
				content = {'msg':'Incorrect Audio FIle ID'}
				return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			content = {'msg':'Audio File Updated Successfully'}
			return Response(content, status=status.HTTP_200_OK)
		else:
			content = {'msg':'Audio File ID is Required'}
			return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	except IntegrityError:
		content = {'msg':"Duration Can't be Negative"}
		return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["POST"])
def getaudio(request):
	data=request.data
	try:
		audioFileID=data['audioFileID']
	except KeyError:
		audioFileID=None
	try:
		audioFileType=data['audioFileType']
	except KeyError:
		audioFileType=None
	if audioFileID != None:
		if SongData.objects.filter(file_id=audioFileID).exists():
			data=SongData.objects.filter(file_id=audioFileID)[0]
			dic={
				'id':int(data.file_id),
				'name':str(data.name),
				'duration':str(data.duration),
				'uploaded_time':str(data.uploaded_time)
			}
			content = {'audioFileID':audioFileID, 'audioFileMetadata':dic}
			return Response(content, status=status.HTTP_200_OK)
		elif PodcastData.objects.filter(file_id=audioFileID).exists():
			data=PodcastData.objects.filter(file_id=audioFileID)[0]
			dic={
				'id':int(data.file_id),
				'name':str(data.name),
				'duration':str(data.duration),
				'uploaded_time':str(data.uploaded_time),
				'host':str(data.host)
			}
			participants=[]
			for x in PodcastParticipantsData.objects.filter(file_id=audioFileID):
				participants.append(x.participant)
			dic.update({'participants':participants})
			content = {'audioFileID':audioFileID, 'audioFileMetadata':dic}
			return Response(content, status=status.HTTP_200_OK)
		elif AudiobookData.objects.filter(file_id=audioFileID).exists():
			data=AudiobookData.objects.filter(file_id=audioFileID)[0]
			dic={
				'id':int(data.file_id),
				'title':str(data.title),
				'author':str(data.author),
				'narrator':str(data.narrator),
				'duration':str(data.duration),
				'uploaded_time':str(data.uploaded_time)
			}
			content = {'audioFileID':audioFileID, 'audioFileMetadata':dic}
			return Response(content, status=status.HTTP_200_OK)
		else:
			content = {'msg':'Incorrect Audio FIle ID'}
			return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	elif audioFileType != None:
		lt=[]
		dic={}
		if audioFileType == 'Song':
			for x in SongData.objects.all():
				dic={
					'id':int(x.file_id),
					'name':str(x.name),
					'duration':str(x.duration),
					'uploaded_time':str(x.uploaded_time)
				}
				lt.append(dic)
			content = {'audiodata':lt}
			return Response(content, status=status.HTTP_200_OK)
		elif audioFileType == 'Podcast':
			for x in PodcastData.objects.all():
				participants=[]
				for y in PodcastParticipantsData.objects.filter(file_id=x.file_id):
					participants.append(y.participant)
				dic={
					'id':int(x.file_id),
					'name':str(x.name),
					'duration':str(x.duration),
					'uploaded_time':str(x.uploaded_time),
					'host':str(x.host),
					'participants':participants
				}
				lt.append(dic)
			content = {'audiodata':lt}
			return Response(content, status=status.HTTP_200_OK)
		elif audioFileType == 'Audiobook':
			for x in AudiobookData.objects.all():
				dic={
					'id':int(x.file_id),
					'title':str(x.title),
					'author':str(x.author),
					'narrator':str(x.narrator),
					'duration':str(x.duration),
					'uploaded_time':str(x.uploaded_time)
				}
				lt.append(dic)
			content = {'audiodata':lt}
			return Response(content, status=status.HTTP_200_OK)
		else:
			content = {'msg':'Incorrect Audio FIle Type'}
			return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		content = {'msg':'Atleast One Input is Required'}
		return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)