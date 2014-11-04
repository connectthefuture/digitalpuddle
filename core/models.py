import os
from os import path
import shutil
import subprocess

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from core.vagrant import Vagrant

class VirtualMachine(models.Model):
    #: Name of the virtual machine in digital puddle
    name = models.CharField(max_length = 128)
    #: Vagrant image which should be used to build this VM
    vagrant_image = models.CharField(max_length = 256)
    
    def to_vagrant_config(self):
        """
        Creates a vagrant template out of this model.
        """
        
        template = """\
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "{0}"
    config.vm.network "public_network"
end
"""
        return template.format(self.vagrant_image)
    
    def get_vagrant_dir(self):
        return path.join(settings.VM_DIR, str(self.pk))
        
    def __unicode__(self):
        return self.name
    

# Signals
@receiver(post_save, sender=VirtualMachine)
def update_vagrant_config(instance, created, **kwargs):
    """
    This hook will actually update the Vagrant file to
    make sure that the it is in sync with the model.
    """
    
    directory = instance.get_vagrant_dir()
    if created and not path.exists(directory):
        # Create directory
        os.makedirs(directory)
        
    vagrant_file = open(path.join(directory, 'Vagrantfile'), 'w')
    vagrant_file.write(instance.to_vagrant_config())
        
@receiver(post_delete, sender=VirtualMachine)
def delete_vagrant_config(instance, **kwargs):
    """
    Make sure we clean up a vagrant instance if we destroy
    the model.
    """
    
    Vagrant(instance.get_vagrant_dir()).destroy()
    shutil.rmtree(instance.get_vagrant_dir(),
                  ignore_errors=True)
        
    