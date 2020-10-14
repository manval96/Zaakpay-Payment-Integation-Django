import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(response):
    """ updates the repo """
    if request.method == 'POST':
        repo_loc = "manvall.pythonanywhere.com/"
        repo = git.repo(repo_loc)
        origin = repo.remotes.origin
        
        origin.pull() 
        
        return HttpResponse("Code Updated in %s" %repo_loc)
    else:
        return HttpResponse("Couldn't updates the code on %s" %repo_loc)     
