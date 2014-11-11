
import os
import gevent
from subprocess import Popen, PIPE
import fcntl

#from gevent.subprocess import Popen, PIPE

from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace

from core.models import VirtualMachine
from core.vagrant import Vagrant

allowed_commands = ["up", "halt"]

def non_block_read(output):
    # Source: https://gist.github.com/sebclaeys/1232088
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

@namespace("/console")
class ConsoleNamespace(BaseNamespace):

    def initialize(self):
        """
        Mainly for debug.
        """

        print "Got socket connection."

    def on_command(self, data):
        """
        Called whenever the socket recieves a chat message. It
        will then broadcast the message to the rest of the channel.
        """
        try:
            vm = VirtualMachine.objects.get(id = data["vm"])
        except KeyError:
            self.emit('error', "Invalid vm")
            return

        if (data["command"] in allowed_commands):
            self.process_command(vm, data["command"])
        else:
            self.emit('error', "Called command with an invlaid command")
            return
        
    def process_command(self, vm, command):
        # TODO: Rewrite this to use the Vagrant class
        self.emit('console_data', "Running vagrant {0}\n".format(command))
        current_directory = os.getcwd()

        os.chdir(vm.get_vagrant_dir())
        p = Popen(['vagrant', command],
                  stdout = PIPE)

        # Make sure we change the state at the end
        os.chdir(current_directory)
        
        # Now we keep reading and emitting until the 
        # process exits
        while p.poll() is None:
            lines = non_block_read(p.stdout)
            #lines = p.stdout.readline()
            if (lines != ""):
                self.emit('console_data', lines)
            gevent.sleep(0.3)
        lines = non_block_read(p.stdout)   
        self.emit('console_data', lines)
        
        self.emit('console_data', "Finished running vagrant {0}\n".format(command))
        
        # Check if we should update the machine state
        if (command in ["up", "halt"]):
            vm.status = Vagrant(vm).status()
            vm.save()
            self.emit('status_change', vm.status)
            
        print "Done in here."