from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.forms import VirtualMachineForm
from core.sockets import *
from core.models import *

def index(request):
    paged_vms = Paginator(VirtualMachine.objects.all(), 25)
    
    page = request.GET.get('page')
    try:
        vms = paged_vms.page(page)
    except PageNotAnInteger:
        vms = paged_vms.page(1)
    except EmptyPage:
        vms = paged_vms.page(paged_vms.num_pages)
        
    return render(request,
                  "digitalpuddle/index.html",
                  {"vms" : vms})

def create_virtual_machine(request):
    if request.method == "POST":
        form = VirtualMachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('digitalpuddle.index')
    else:
        form = VirtualMachineForm()
    return render(request,
                  "digitalpuddle/create_virtual_machine.html",
                  {"form" : form})

def view_puddle(request, vm_id):
    vm = get_object_or_404(VirtualMachine, pk = vm_id)
    return render(request,
                  "digitalpuddle/view_puddle.html",
                  {"vm": vm})