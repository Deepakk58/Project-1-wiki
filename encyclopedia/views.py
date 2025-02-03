from django.shortcuts import render
from . import util
from markdown2 import Markdown
from random import randint
from django import forms


class NewTaskForm(forms.Form):
    q = forms.CharField(label="Search")

markdowner = Markdown()

def index(request):    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random(request):
    entries = util.list_entries()
    n = randint(0, len(entries)-1)
    page = util.get_entry(entries[n])
    converted_page = markdowner.convert(page)
    
    return render(request, "encyclopedia/entry.html", {
        "page": converted_page,
        "name": entries[n].upper()
    })

def search(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["q"]
            page = util.get_entry(name)
            if page != None:
                
                converted_page = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html", {
                    "page": converted_page,
                    "name": name.upper()
                })
            
            else:
                entries = []
                for entry in util.list_entries():
                    if name.upper() in entry.upper():
                        entries.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "name": name,
                    "entries": entries
                })

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })


def loadEntry(request, name):

    page = util.get_entry(name)
    if page == None:
        return render(request, "encyclopedia/error404.html", {
            "name": name
        })
    
    converted_page = markdowner.convert(page)
    return render(request, "encyclopedia/entry.html", {
        "page": converted_page,
        "name": name.upper()
    })

def newEntry(request):
    return render(request, "encyclopedia/entry.html")