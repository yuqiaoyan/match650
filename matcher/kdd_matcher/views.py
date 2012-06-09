from datetime import datetime

from matcher import matcher
from models import Professor, Result, Algo

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import lucene

def index(request):
    return render_to_response('index.html',
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
    lucene.getVMEnv().attachCurrentThread()
    try:
        student = {}
        student['name'] = request.POST['student_name']
        student['interest'] = \
            request.POST['student_interest']
        student['affiliation'] = \
            request.POST['student_affiliation']
        result = Result.objects.get(stuname=student['name'],
                stuaffiliation=student['affiliation'],
                stuinterest=student['interest'])
    except KeyError:
        return render_to_response('index.html',
                {'error_msg':'missing field'},
                context_instance=RequestContext(request))
    except Result.DoesNotExist:
        prof_matcher = matcher()
        prof_result= prof_matcher.getProfMatch(student)
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
                pos3id=prof_list[2], algoid=Algo.objects.get(pk=1))
        result.save()
        #return render_to_response('results.html', {'prof_list':prof_list, 'student':student})
    request.session['result_id'] = result.id
    return HttpResponseRedirect(reverse('kdd_matcher:results'))

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
