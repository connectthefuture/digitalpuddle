import shutil
from os import path

from django.test import TestCase, override_settings, Client
from django.conf import settings
from django.core.urlresolvers import reverse

from core.models import VirtualMachine

@override_settings(VM_DIR='/tmp/vms')
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def tearDown(self):
         shutil.rmtree(settings.VM_DIR, ignore_errors=True)

    def test_create_virtual_machine(self):
        num_vms = VirtualMachine.objects.all().count()
        url = reverse('digitalpuddle.create_virtual_machine')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(url, {})
        self.assertFormError(response, 'form',
                             'name', 'This field is required.')
        
        response = self.client.post(url, {'name' : 'foobar',
                                'vagrant_image' : 'baz' })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VirtualMachine.objects.all().count(),
                         num_vms + 1)
                
@override_settings(VM_DIR='/tmp/vms')
class VirtualMachineTestCase(TestCase):
    
    def setUp(self):
        self.vm = VirtualMachine.objects.create(name="foo",
                                                vagrant_image="bar")
      
    def tearDown(self):
        shutil.rmtree(settings.VM_DIR, ignore_errors=True)
        
    def test_unicode(self):
        self.assertEqual(self.vm.__unicode__(),
                         "foo")
        
    def test_get_vagrant_dir(self):
        self.assertEqual(self.vm.get_vagrant_dir(),
                         path.join(settings.VM_DIR, str(self.vm.pk)))
        
    def test_to_vagrant_config(self):
        expected = """\
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "bar"
end
"""
        
        self.assertEqual(self.vm.to_vagrant_config(),
                         expected)
        
    def test_updates_vagrant_config(self):
        """
        Make sure the post save handler will create a directory
        and put the proper file in it.
        """
        
        directory = path.join(settings.VM_DIR, str(self.vm.pk))
        self.assertTrue(path.exists(directory))
        
    def test_delete_vagrant_config(self):
        """
        Make sure that if we delete an object it also cleans
        up the vagrant files.
        """
        
        vm = VirtualMachine.objects.create(name="foo",
                                           vagrant_image="bar")
        directory = path.join(settings.VM_DIR, str(vm.pk))
        self.assertTrue(path.exists(directory))
        
        vm.delete()
        
        self.assertFalse(path.exists(directory))