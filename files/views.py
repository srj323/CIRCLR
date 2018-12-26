from django.shortcuts import render,HttpResponse
from files.models import FileModel
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    if request.method == "POST" and "uploadedfile" in request.FILES :
        filename = request.FILES["uploadedfile"].name
        print("--------------"+filename)
        uploadedfile = request.FILES["uploadedfile"]
        if not FileModel.objects.filter(file_id=request.user.username+filename):
            FileModel.objects.create(owner = request.user.username, file_id=request.user.username+filename, name = filename,file=uploadedfile)
            return render(request, 'files/index.html', {
                'upload_status':'File Uploaded',
                'file_list':FileModel.objects.filter(owner = request.user.username),
            })
        else:
            return render(request, 'files/index.html', {
                'upload_status':'File Aready Exists. Please Rename and Upload',
                'file_list':FileModel.objects.filter(owner = request.user.username),
            })
    else:
        return render(request, 'files/index.html', {
            'upload_status':'Please Upload File',
            'file_list':FileModel.objects.filter(owner = request.user.username),
        })

def filedisplay(request,file_id):
    return render(request,'files/display.html' ,{
        'file': FileModel.objects.filter(file_id=file_id)[0]

    })
