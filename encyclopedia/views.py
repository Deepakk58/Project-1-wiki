from django.shortcuts import render
from . import util
from markdown2 import Markdown
from random import randint
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
import re


class SearchForm(forms.Form):
    q = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'title', 'placeholder': 'Title'}))
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'class': 'content', 'placeholder': 'Write Page Content Here'}))
    

class EditEntryForm(forms.Form):
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'class': 'content', 'placeholder': 'Write Page Content Here'}))

markdowner = Markdown()

def HTMLtoText(html):
    html = markdowner.convert(html)
    html = re.sub(r"<h1>.*?</h1>", "", html, flags=re.DOTALL)
    text = BeautifulSoup(html)
    text = text.get_text()
    return text[1:]

def Addtitle(html, title):
    return "#"+title+'\n'+html

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
        "name": entries[n].capitalize()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["q"]
            page = util.get_entry(name)
            if page != None:
                
                converted_page = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html", {
                    "page": converted_page,
                    "name": name.capitalize()
                })
            
            else:
                entries = []
                for entry in util.list_entries():
                    if name.upper() in entry.upper():
                        entries.append(entry)
                if entries == []:
                    return render(request, "encyclopedia/error404.html", {
                        "name": name
                    })
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
        "name": name.capitalize()
    })

def newEntry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = Addtitle(content, title)
            if util.get_entry(title) != None:

                return render(request, "encyclopedia/errorAlreadyExist.html", {
                    "name": title.capitalize()
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:loadEntry", kwargs={"name": title})) 

        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form
            })

    return render(request, "encyclopedia/newEntry.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            content = Addtitle(content, title)
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:loadEntry", kwargs={"name": title})) 

        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })
    text = HTMLtoText(util.get_entry(title))
    return render(request, "encyclopedia/edit.html", {
        "form" : EditEntryForm(initial={'content': text}),
        "title": title
    })