from django.http import HttpResponse,Http404
import datetime

def hello(request): 
	return HttpResponse("Hello world")

def current_datetime(request): 
	now = datetime.datetime.now() 
	html = "现在的时间是 %s." % now 
	return HttpResponse(html)

def hours_ahead(request, offset): 
	# try:
	# 	offset = int(offset)
	# except ValueError: 
	# 	raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	#assert False
	html = "In %s hour(s), it will be %s. " % (offset, dt)
	return HttpResponse(html)