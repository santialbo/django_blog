from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.db import models
from django.core.context_processors import csrf
from django.views.decorators.cache import cache_page
from blog.models import Author, Entry, Comment, Tag
from random import shuffle
from math import ceil
from datetime import datetime

def tag_cloud(max_items = 20, min_size = 12, max_size = 24):
    tags = Tag.objects.all().annotate(entry_count = models.Count('entry')).order_by('-entry_count')[:max_items]
    items = tags.count()
    if items == 0:
        return []
    max_count = tags[0].entry_count
    min_count = tags[items-1].entry_count
    cloud = []
    factor = (max_size - min_size)/(max_count - min_count)
    for tag in tags:
        cloud.append((tag.name, int(min_size + (tag.entry_count - min_count)*factor)))
    shuffle(cloud)
    return cloud

def latest_entries():
    return Entry.objects.all().order_by('-date')[:10]

def default_context(request):
    context = Context()
    context.update(csrf(request))
    context.update({'tag_cloud': tag_cloud(),
                    'latest_entries': latest_entries()})
    return context

def handle_entries_pagination(context, entries, page, entries_per_page = 3):
    if page == None:
        page = 1
    num_pages = int(ceil(len(entries)/float(entries_per_page)))
    if num_pages > 0:
        page = int(page)
        if page < 1:
            page = page % num_pages + 1
        elif page > num_pages:
            page = num_pages
        context.update({'page': page})
        context.update({'num_pages': num_pages})
        first = (page - 1) * entries_per_page
        last = first + entries_per_page
        context.update({'entries': entries[first:last]})

@cache_page(60)
def blog(request, page = 1):
    template = loader.get_template('entries.html')
    context = default_context(request)
    context.update({'url': '/blog/'})
    handle_entries_pagination(context, latest_entries(), page)
    return HttpResponse(template.render(context))

@cache_page(60)
def entry(request, entry_id):
    try:
        entry = Entry.objects.get(id = entry_id)
    except Entry.DoesNotExist:
        raise Http404
    template = loader.get_template('entry.html')
    context = default_context(request)
    context.update({'entry': entry})
    return HttpResponse(template.render(context))

def post_comment(request, entry_id):
    comment = Comment(entry_id = entry_id,
                      name = request.POST['name'],
                      comment = request.POST['comment'],
                      date = datetime.now())
    comment.save();
    return entry(request, entry_id)

def author(request, author_name, page = 1):
    author = Author.objects.get(name = author_name)
    author_entries = Entry.objects.all().filter(author = author).order_by('-date')
    template = loader.get_template('entries.html')
    context = default_context(request)
    context.update({'url': '/blog/author/' + author_name + '/'})
    handle_entries_pagination(context, author_entries, page)
    return HttpResponse(template.render(context))

def tag(request, tag_name, page = 1):
    tag = Tag.objects.get(name = tag_name)
    entries_by_tag = Entry.objects.all().filter(tags__in = [tag]).order_by('-date')
    template = loader.get_template('entries.html')
    context = default_context(request)
    context.update({'url': '/blog/tag/' + tag_name + '/'})
    handle_entries_pagination(context, entries_by_tag, page)
    return HttpResponse(template.render(context))

def search(request):
    search = request.POST['search']
    entries_by_search = Entry.objects.filter(text__search=search)
    template = loader.get_template('entries.html')
    context = default_context(request)
    context.update({'entries': entries_by_search})
    return HttpResponse(template.render(context))