from django.http import JsonResponse
from collegedb.models import Student
from eventdb.models import Events
from eventdb.models import Hosts
from eventdb.models import EventHosts
from django.shortcuts import render
import requests



def chatbot(request):
    api_key="AIzaSyCuzylXl0lrmzl7UTwu01Ewbu7YRXuTGmU"
    query=request.GET.get('query',"")
    payload={
    "contents":[
        {
            "parts":[
                {
                    "text":"I want you to act as a experienced technical interviewer "
                },
                {"text":query}
            ]
        }
    ]
    }
    params={
        "key":api_key
    }
    result=requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                         params=params,json=payload)
    data=result.json()
    output_text = data["candidates"][0]["content"]["parts"][0]["text"]
    return JsonResponse({"output": output_text})

def chat_page(request):
    return render(request, "chat.html")

def fetch_events(request):
    result=Events.objects.all().values()
    #result=Events.objects.filter(name="python programming workshop").values()
    #result=Events.objects.filter(price__gte=200).values()
    #result=Events.objects.filter(host_id=2).values()
    #print(result.values())
    return render(request,"events.html",context={'events':list(result)})
    #return JsonResponse(list(result),safe=False)

def fetch_hosts(request):
    result1=Hosts.objects.all().values()
    
    return JsonResponse(list(result1),safe=False)

def fetch_eventhosts(request):
    result1=EventHosts.objects.all().values()
    return JsonResponse(list(result1),safe=False)

def update_event(request):
    name_value=request.GET.get('name')
    price_value=request.GET.get('price')
    desc_value=request.GET.get('desc')
    limit_value=request.GET.get('limit')
    
    event=Events.objects.get(name=name_value)
    event.price=price_value
    event.desc=desc_value
    event.limit=limit_value
    
    event.save()
    return JsonResponse({'message':'Event Updated','updated':{
        "name":event.name,
        "price":event.price,
        "desc":event.desc,
        "limit":event.limit
    }})

def add_event(request):
    name_value=request.GET.get('name')
    price_value=request.GET.get('price')
    desc_value=request.GET.get('desc')
    limit_value=request.GET.get('limit')
    
    Events.objects.create(
        name=name_value,
        price=price_value,
        desc=desc_value,
        limit=limit_value
    )
    return JsonResponse({'message':'Event Added'})
def update_host(request):
    event_id_value=request.GET.get('event_id')
    host_id_value=request.GET.get('host_id')
    
    event=Events.objects.get(event_id=event_id_value)
    host=Hosts.objects.get(host_id=host_id_value)
    EventHosts.objects.create(
        event_id=event,
        host_id=host
    )
    return JsonResponse({'message':'Host updated'})

def delete_event(request):
    name_value=request.GET.get('name')
    event=Events.objects.get(name=name_value)
    event.delete()
    return JsonResponse({'message':'Event Deleted'})

student_list = []
professor_list = []
facility_list = []


def add_student(request):
    name_value = request.GET.get('name')
    usn_value = request.GET.get('usn')
    phone_value = request.GET.get('phone')
    department_value = request.GET.get('department')

    student = {
        'name': name_value,
        'usn': usn_value,
        'phone': phone_value,
        'department': department_value
    }
    
    Student.objects.create(view_students)
    student_list.append(student)

    return JsonResponse({
        'message': 'Student added successfully!',
        'student_added': student
    })
def view_students(request):
    view_students=Student.objects.all().values('name','usn','gender')
    return JsonResponse({'students': list(view_students)})

def add_professor(request):
    name_value = request.GET.get('name')
    id_value = request.GET.get('id')
    subject_value = request.GET.get('subject')
    experience_value = request.GET.get('experience')
   

    professor = {
        'name': name_value,
        'id':id_value,
        'subject': subject_value,
        'experience': experience_value,
    
    }

    professor_list.append(professor)

    return JsonResponse({
        'message': 'Professor added successfully!',
        'professor_added': professor
    })
def view_professors(request):
    return JsonResponse({'professors': professor_list})
def add_facility(request):
    name_value = request.GET.get('name')
    location_value = request.GET.get('location')
    description_value = request.GET.get('description')

    facility = {
        'name': name_value,
        'location': location_value,
        'description': description_value
    }

    facility_list.append(facility)

    return JsonResponse({
        'message': 'Facility added successfully!',
        'facility_added': facility
    })
def view_facilities(request):
    return JsonResponse({'facilities': facility_list})
