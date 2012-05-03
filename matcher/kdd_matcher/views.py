from django.template import Context, loader,RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect

def index(request):
    return render_to_response('index.html',
            context_instance=RequestContext(request))

def match(request):
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
        prof_list = get_prof(student)
        request.session['prof_list'] = prof_list
        request.session['student'] = student
        return HttpResponseRedirect(reverse('kdd_matcher.views.results'))

def results(request):
    student = request.session.get('student')
    print student
    prof_list = request.session.get('prof_list')
    return render_to_response('results.html',
            {'prof_list':prof_list, 'student':student})


def get_prof(student):
    return [
            {
                'name':'prof a',
                'interest':'data mining', 
                'affiliation':'U of M',
            },
            {
                'name':'prof b',
                'interest':'data mining', 
                'affiliation':'U of M',
            }
            ]

