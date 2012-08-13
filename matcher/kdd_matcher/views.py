from datetime import datetime
import time
import random

from matcher import matcher
from models import Professor, Result, Algo
from .forms import QueryForm, ReviewForm

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
import lucene

BOOST_1 = {'interest':1.0,'processed_aff':2.0}
BOOST_2 = {'interest':2.0,'processed_aff':1.0}

def index(request):
    form = QueryForm()
    return render_to_response('index.html',
                            {'form': form},
                            context_instance=RequestContext(request))

def studentE(request):
    return render_to_response('studentE.html',
            context_instance=RequestContext(request))

def explain(request):
    student = request.session.get('student')
    info_list = request.session.get('info_list')
    return render_to_response('explain.html',
            {'student':student,'info_list':info_list})

def matchE(request):
    lucene.getVMEnv().attachCurrentThread()
    try:
        student = {}
        student['name'] = request.POST['student_name']
        student['interest'] = \
            request.POST['student_interest']
        student['affiliation'] = \
            request.POST['student_affiliation']
    except KeyError:
        return render_to_response('index.html',
                {'error_msg':'missing field'},
                context_instance=RequestContext(request))
    else:
        prof_matcher = matcher()
        prof_list = prof_matcher.getProfMatch(student)
        request.session['prof_list'] = prof_list
        request.session['student'] = student
	info_list = []
	for i,prof in enumerate(prof_list):
        	score,explainList = prof_matcher.explainPos(i+1)
		info_list.append((prof,score,explainList))
	for prof in prof_list:
            print prof['name']
            aff_count = prof['affiliation'].count(student['affiliation'])
            prof['co_count'] = aff_count
        student = request.session.get('student')
        print 'in match', student, prof_list[0].get('name')
        return render_to_response('explain.html', {'info_list':info_list,'student':student})
        #return HttpResponseRedirect(reverse('kdd_matcher.views.results'))


def match(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            interest = form.cleaned_data['interest']
            affiliation = form.cleaned_data['affiliation']
            try:
                result = Result.objects.get(stuname=name,
                                            stuaffiliation=affiliation,
                                            stuinterest=interest)
            except Result.DoesNotExist:
                lucene.getVMEnv().attachCurrentThread()
                student = {}
                student['name'] = name
                student['interest'] =interest
                student['affiliation'] = affiliation
                timestamp = int(time.time())
                algo_id = 1
                prof_matcher = matcher()
                if random.randint(1,1000) & 1:
                    boost = BOOST_1
                else:
                    boost = BOOST_2
                    algo_id = 2
                prof_result = prof_matcher.getProfMatch(student, boosts=boost)
                prof_list = []
                for result in prof_result:
                    name = result['name']
                    interest = result['interest']
                    print name, interest
                    professor = Professor.objects.get(name__icontains=name.split(' ')[0],
                            interest=interest)
                    prof_list.append(professor.id)
                result = Result(stuinterest=student['interest'],
                        stuname=student['name'], stuaffiliation=
                        student['affiliation'], date=datetime.now(),
                        pos1id=prof_list[0], pos2id=prof_list[1],
                        pos3id=prof_list[2],
                        algoid=Algo.objects.get(pk=algo_id))
                result.save()
            request.session['result_id'] = result.id
            return HttpResponseRedirect(reverse('kdd_matcher:results'))
    return render_to_response('index.html', 
                                {'form': form},
                                 context_instance=RequestContext(request))


def review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        print 'in review'
        print form
        if form.is_valid() and request.is_ajax():
            review = form.cleaned_data['review']
            resultid = form.cleaned_data['resultid']
            score = form.cleaned_data['score']
            result = Result.objects.get(pk=resultid)
            result.review = review
            result.rating = score
            result.save()
            return render(request, 'success.html')
        else:
            result = Result.objects.get(pk=form["resultid"].value)
            return render(request, 'review_form.html',
                            {'error':'Please don\'t leave a blank',
                            'form':form,
                            'result':result})



def results(request):
    result_id = request.session['result_id']
    result = Result.objects.get(id=result_id)
    prof_list = []
    for i in range(1,4):
        prof_id = getattr(result, "pos%did"%i, None)
        if prof_id and prof_id != '':
            professor = Professor.objects.get(id=prof_id)
            if result.stuaffiliation != '':
                professor.get_co_num(result.stuaffiliation)

            prof_list.append(professor)
    return render_to_response('results.html',
            {'prof_list':prof_list, 'result':result},
            context_instance=RequestContext(request))
