from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Albumtable, Songstable, Ratingtable
from operator import itemgetter, attrgetter, methodcaller
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min,Count
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def albummethod(request):
    ialbum = Albumtable()

    ialbum.album_name = re.sub(' +', ' ', request.POST.get('albumname').strip())
    #re.sub  whitespacing
    #strip  trim


    #for capitalization of album name
    ialbum.album_name = ialbum.album_name[:1].upper() + ialbum.album_name[1:]


    ialbum.album_year = request.POST['albumyear']
    ialbum.save()


@login_required
def createnewalbum(request):

        if request.method == 'POST':
            recordexists = Albumtable.objects.filter(album_name=request.POST.get('albumname'))\
                           &Albumtable.objects.filter(album_year=request.POST.get('albumyear'))
            if recordexists:
                existingerror = True
                return render(request, 'mysongs/Createnewalbum.html', {'existingerror': existingerror})
            else:
                albummethod(request)
                return HttpResponseRedirect("/mysongs/createnewsong")
        else:
            #return HttpResponseRedirect("hi")
            return render(request, 'mysongs/Createnewalbum.html')

@login_required
def createnewsong(request):
    album_value_list = Albumtable.objects.all()


    albumrecord_list = sorted(album_value_list, key=lambda Albumtable:Albumtable.album_name)

    duplicate_album_list = Albumtable.objects.values('album_name').annotate(Count('album_name')).filter(album_name__count__gt=1)


    if request.method == 'POST':
        form_action = request.POST['form_action']

        if form_action == 'createsong':
            isongs = Songstable()

            isongs.song_name = re.sub(' +', ' ', request.POST.get('songname').strip())
            isongs.song_name = isongs.song_name[:1].upper() + isongs.song_name[1:]

            isongs.artist_name = re.sub(' +', ' ', request.POST.get('artistname').strip())
            isongs.artist_name = isongs.artist_name[:1].upper() + isongs.artist_name[1:]

            ialbum = Albumtable.objects.get(album_id=request.POST.get('currentalbum'))
            ialbum.save()
            isongs.album_id = ialbum
            isongs.save()
            return HttpResponseRedirect("/mysongs/albumdetails")

        else:
            recordexists = Albumtable.objects.filter(album_name=request.POST.get('albumname'))\
                           &Albumtable.objects.filter(album_year=request.POST.get('albumyear'))
            if recordexists:
                existingerror = True
                return render(request, 'mysongs/Createsong.html', {'existingerror': existingerror, 'duplicate_album_list': duplicate_album_list})
            else:
                albummethod(request)
                return HttpResponseRedirect("/mysongs/createnewsong")

    else:
        return render(request, 'mysongs/Createsong.html', {'Albumrecord_list': albumrecord_list,
                                                           'duplicate_album_list': duplicate_album_list})

@login_required
def albumdetails(request):
    album_value_list = Albumtable.objects.all()
    album_list = sorted(album_value_list, key=lambda Albumtable: Albumtable.album_name)
    return render(request, 'mysongs/Albumdetails.html', {'album_list': album_list})

@login_required
def songsview(request, album_id):
    songs_list = Songstable.objects.filter(album_id=album_id)
    album_instance = Albumtable.objects.filter(album_id=album_id)[0]
    request.session['temp_album_id'] = album_id
    return render(request, 'mysongs/Songsview.html', {'songs_list': songs_list, 'album_instance': album_instance})

@login_required
def songdetails(request, song_id):
    album_instance = Albumtable.objects.filter(album_id=request.session['temp_album_id'])[0]
    song_info = Songstable.objects.get(song_id=song_id)
    iuser = User.objects.get(username=request.user.username)
    rating_list = Ratingtable.objects.filter(song_id=song_id,user_id=iuser)
    song_info.view_count += 1


# Html update part
    if request.method == 'POST':
        if len(rating_list) != 0:
            update_inst = Ratingtable.objects.filter(song_id=song_id)[0]
            update_inst.user_rating = request.POST.get('userrating')
            update_inst.save()
            return HttpResponseRedirect('/mysongs/songsview/' + str(request.session['temp_album_id']))
        else:
            isong = Songstable.objects.get(song_id=song_id)
            iuser = User.objects.get(username=request.user.username)
            irating = Ratingtable()
            irating.song_id = isong
            irating.user_id = iuser
            irating.user_rating = request.POST.get('userrating')
            irating.save()
            return HttpResponseRedirect('/mysongs/songsview/' + str(request.session['temp_album_id']))

# Rendering html
    if len(rating_list) != 0:
        song_info.save()
        return render(request, 'mysongs/Songdetails.html', {'rating': int(rating_list[0].user_rating),
                                    'song_info': song_info, 'values': [1, 2, 3, 4, 5],'album_instance': album_instance})
    else:
        song_info.save()
        return render(request, 'mysongs/Songdetails.html', {'song_info': song_info, 'album_instance': album_instance})

@login_required
def topviewedsong(request):

    topviewedsong = Ratingtable.objects.values('song_id', 'song_id__song_name', 'song_id__artist_name', 'song_id__view_count').\
         annotate(average_rating=Avg('user_rating')).order_by('-average_rating')

    viewedvalue = topviewedsong.order_by('song_id__view_count').reverse()

    return render(request, 'mysongs/Topviewedsong.html', {'value': viewedvalue},)


@login_required
def topratedsong(request):

    topratingavg = Ratingtable.objects.values('song_id', 'song_id__song_name', 'song_id__artist_name','song_id__view_count').\
        annotate(average_rating=Avg('user_rating')).order_by('-average_rating')
    return render(request, 'mysongs/Topratedsong.html', {'value1': topratingavg})


