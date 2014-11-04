from django.shortcuts import render, redirect

from core.forms import VirtualMachineForm
from core.sockets import *

def index(request):
    return render(request,
                  "digitalpuddle/index.html",
                  {})

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