from gevent.subprocess import Popen, PIPE
from os import environ

import re

class Vagrant(object):
    """
    Runs specified vagrant commands.
    """
    
    def __init__(self, path):
        """
        path should be the directory containing the Vagrantfile
        """
        
        self.path = path
        
    def run_command(self, command, *args):
        """
        Run an actual command. Will set up a new
        enviornment with the VAGRANT_CWD set.
        """
        
        env = environ.copy()
        env['VAGRANT_CWD'] = self.path
        
        process = Popen(["vagrant", command] + list(args),
                        env=env)
        
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
        
    def gather_ips(self):
        """
        SSH in and call ifconfig. Then we do some simple
        parsing here to extract the IP addresses. Returns
        a list of strings of IPs
        """
        
        p = self.run_command("ssh", "-c", "ifconfig")
        data = "".join(p.stdout.readlines())
        return [x in re.findall(r'inet addr:(\S+)', data)]