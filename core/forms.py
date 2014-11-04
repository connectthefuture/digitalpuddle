from django.forms import ModelForm

from core.models import VirtualMachine

class VirtualMachineForm(ModelForm):
    class Meta:
        model = VirtualMachine
        fields = ['name',
                  'vagrant_image']