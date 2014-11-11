from gevent.subprocess import Popen, PIPE
from os import environ

import re



class Vagrant(object):
    """
    Runs specified vagrant commands.
    """
    
    def __init__(self, vm):
        """
        VM should be a model that represents the VM
        """
        
        self.vm = vm
        
    def run_command(self, command, *args):
        """
        Run an actual command. Will set up a new
        enviornment with the VAGRANT_CWD set.
        """
        
        env = environ.copy()
        env['VAGRANT_CWD'] = self.vm.get_vagrant_dir()
        
        process = Popen(["vagrant", command] + list(args),
                        env=env, stdout=PIPE, stderr=PIPE)
        
        return process
        
    def up(self):
        """
        Runs the up command and returns the process
        that is running.
        """
        
        return self.run_command("up")
        
    def halt(self):
        """
        Runs the halt command and returns the 
        corresponding process.
        """
        
        return self.run_command("halt")
    
    def destroy(self):
        """
        Destroys the underlying VM.
        """
        
        return self.run_command("destroy")
    
    def status(self):
        """
        Gets the status of the underlying vagrant VM.
        """
        
        p = self.run_command("status", "--machine-readable")
        data = [x for x in p.stdout.readlines() if ",state," in x]
        return data[0].split(',')[-1].strip()
        
    def gather_ips(self):
        """
        SSH in and call ifconfig. Then we do some simple
        parsing here to extract the IP addresses. Returns
        a list of strings of IPs
        """
        
        p = self.run_command("ssh", "-c", "ifconfig")
        data = "".join(p.stdout.readlines())
        return [x in re.findall(r'inet addr:(\S+)', data)]