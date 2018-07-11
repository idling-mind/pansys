"""
Interactive Ansys

Maintained & Created by : Najeem Muhammed 

"""
import os
import re
from datetime import datetime
import pexpect

import pandas as pd

from .utility_functions import return_value

class Ansys(object):
    """Ansys session class
    
    Ansys class to create an interactive ansys session. You can interact with
    an ansys session with the help of this class.

    Prerequisites: 
        * Ansys should be installed in your computer. 
        * Ansys should have a interactive commandline interface.
    
    To initiate, create an instance of the class as shown below:

        >>> ans = Ansys()

    This will create an instance of ansys v.15 in a newly created folder.
    You can change the start command of ansys by setting the ``startcommand`` as
    shown below:

        >>> ans = Ansys(startcommand="ansys130")
        
    You can also change the folder where you want Ansys to start by setting the
    ``startfolder`` parameter.

    Args:
        startcommand (str): Ansys start command. The linux command corresponding to the 
            version of ansys you want to open. You can give the license 
            type as well along with the ansys command.
        startfolder (str): The folder in which you want to start ansys. The folder should
            be existing already. If left blank, a new folder of the format
            ``YYYYMMDDHHSS`` will be started in the location where python is
            running and ansys will be started inside that.
        cleanup (bool): If true will delete the ansys working directory after the ansys
            has exited. Will not delete if an existing start folder was given.
        host (str): The system in which you want to start the Ansys session. You can pass
            in the format ``user@system`` where user is the username you want to use to 
            connect to the system and system is the network name of the system or the
            ip-address of the system to which you want to connect to. You can omit the user
            part if you want to connect to the remote machine with the current login itself.
            It is expected that you have set up ssh-keys in the remote system for this to work.

    """
    def __init__(self, startcommand = "ansys150", startfolder=None, cleanup=False, host=None):
        self._startcommand = startcommand #The command that wil be used to open ansys
        self.cleanup = cleanup # If True delete the working directory after exiting ansys
        """bool: Flag if set to True will delete the directory where ansys was
        running"""
        # List of ansys prompts which will mark the end of a command
        self.expect_list = [' BEGIN:\r\n', 
                            ' PREP7:\r\n', 
                            ' POST1:\r\n', 
                            ' SOLU_LS1:\r\n', 
                            ' POST26:\r\n', 
                            ' AUX12:\r\n', 
                            ' AUX15:\r\n', 
                            ' AUX2:\r\n', 
                            ' AUX3:\r\n']
        self.warn_list = ['WARNING','NOTE','ERROR']
        # Checking and setting the ansys working directory
        if startfolder is None:
            #If start folder is not existing, create a folder with current data
            #and time as the name.
            self._wd = os.path.join(os.getcwd(),"pansys_" +  
                                   datetime.now().strftime("%Y%m%d%H%M%S"))
            try:
                os.makedirs(self._wd)
            except:
                OSError("Could not create folder at given location. Check if you have write access.")
        elif os.path.exists(startfolder):
            self._wd = startfolder
            self.cleanup = False
        else:
            raise OSError("The folder {} doesn't exist".format(startfolder))

        curdir = os.getcwd()
        os.chdir(self._wd)
        # Starting the ansys session. timeout set to None so that the process
        # will wait as long as required for a command to finish
        try:
            if host is None:
                self.process = pexpect.spawn(self._startcommand, 
                                         maxread=10000, 
                                         searchwindowsize=100,
                                         timeout=None, 
                                         encoding="utf-8")
            else:
                self.process = pexpect.spawn("ssh {} -t 'cd {} && {}'".format(
                                            host, self._wd, self._startcommand),
                                         maxread=10000, 
                                         searchwindowsize=100,
                                         timeout=None, 
                                         encoding="utf-8")
        except pexpect.exceptions.ExceptionPexpect:
            raise OSError("The command {} was not found".format(self._startcommand))
        os.chdir(curdir)
        # A blank command is sent since ansys asks to press <CR> in the
        # beginning of an interactive session
        self.process.sendline() 
        # Setting some defaults
        self.send("""      
            /PAGE,99999999,256,99999999,240
            /HEADER,OFF,OFF,OFF,OFF,ON,OFF
            /FORMAT,12,E,16,8
            /RGB,INDEX,100,100,100,0
            /RGB,INDEX,0,0,0,15
        """)
        try:
            if self.process.expect(self.expect_list) == 0:
                self._output = "{} started in directory {}".format(self._startcommand, self._wd)
                # print("{} started in directory {}".format(self._startcommand, self._wd))
        except pexpect.EOF:
            raise OSError("Ansys did not start! Check the command or start_folder.")
        
    def __repr__(self):
        """Representation of the object"""
        return "<pyansys.Ansys object started in {} with command {}>".format(
                self._wd, self._startcommand) 

    def __del__(self):
        """Destructor function for ansys exiting"""
        try:
            self.send("""
                finish
                /exit,nosav
                """)
        except AttributeError:
            pass
        if self.cleanup:
            import shutil
            shutil.rmtree(self._wd)
    
    def send(self,command_string, **kwargs):
        """Sending a command to ansys
        
        Function to send commands to interactive ansys session.
        Commands can be single line or multiline.

        Example:
            >>> ans.send('/post1')
            >>> ans.send('''
            ...     file,results,rst
            ...     set,last
            ...     esel,s,mat,,1
            ...     ''')

        You can process the output from any ansys command using the
        ``output_function`` argument.

        Example:
            >>> def parseout(line):
            ...     if "WARNING" in line:
            ...         print("Found a warning")
            ...     else:
            ...         pass
            ...  
            >>> ans.send("set, last", silent=False, output_function=parseout)

        In the above scenario, "Found a warning" string will be printed for 
        every occurance of a warning for the ansys command ``set,last``. 
        For other lines, no action will be taken.

        Args:
            command_string (str): Required. The string containing ansys command
            silent (bool): Optional. Boolean value which when set true will print the
                output from ansys after executing ``command_string``
            output_function (function): Optional. A function which will process the output
                from ansys. The output will be passed line by line
                to this function. silent option should be set to True
                for this to work.

        Returns:
            None

        """
        # Commands are split in to separate commands and executed recursively
        commands = command_string.split("\n")
        if len(commands) > 1:
            for command in commands:
                self.send(command, **kwargs)
        elif commands and len(commands) == 1:
            # Sending the command to ansys
            self.process.sendline(commands[0])
            # self._output will contain the output of last executed command
            self._output = ""
            for line in self.process:
                self._output += line
                # Checking if the command was executed silently or not
                if not kwargs.get("silent", True):
                    # Function to process output, default is print function
                    ofunc = kwargs.get("output_function", print)
                    ofunc(line.strip())
                if any(x in line for x in self.expect_list):
                    break
            return
    
    def plot(self,command_string):
        """Plot anything in ansys
        
        Function to return an image with a plot from Anys.

        Example: 
        
            >>> ans.plot("eplot")
        
        Args:
            command_string (str): The command for plotting in ansys
            
        Returns:
            str: The path to the image file.
        """
        #Enable JPEG output from ansys plot commands
        self.send("/SHOW,JPEG")
        if command_string:
            self.send(command_string)
        else:
            # If not command string was passed, just replot the window
            self.send("/replot")
        # Extract the image file name from ansys output
        image_name = re.search("WRITTEN TO FILE (\w*.jpg)", 
                             self._output).group(1)
        if image_name:
            image_file = os.path.join(self._wd, image_name)
            self.send("/SHOW,CLOSE")
            return image_file
        else:
            return None

    def get(self, entity, entnum, item1, it1num="", item2="", it2num=""):
        """Wrapper for ansys ``*GET`` command
        
        Function to execute the ``*get`` command of ansys. Sequence of input data
        is same as in ansys.

        Args:
            entity (str):
            entnum (str):
            item1 (str): 
            it1num (str): 
            item2 (str):
            it2num (str): 
            
        .. note:: 
            All arguments are in the same order as per ansys ``*get`` documentation.

        Returns:
            Output of ``*get``. Can be int, float, exponential or string.
        """
        if not entnum: entnum=0
        self.send("*del,mypar__")
        self.send("*get,mypar__,{},{},{},{},{},{}".format(
                          entity, entnum, item1, it1num, item2, it2num))
        self.send("/com,%%mypar__%")
        mypar = self._output.split("\n")[1].strip()
        if "mypar__" in mypar:
            raise ValueError("The *get command did not yield any value")
        return return_value(mypar)
    
    @property
    def version(self):
        """The version of ansys for the current active session."""
        return self.get("active", "", "rev")

    @property
    def wd(self):
        """Current working directory where Ansys is running."""
        return self._wd

    @property
    def output(self):
        """The output of the last executed Ansys command"""
        return self._output

    def get_output(self, command_string, persist=False):
        """Function to get ansys output as a file
        
        The function uses ``/output`` command in ansys to redirect the output to a
        file. The path to this file will be returned from the command.
        
        Args:
            command_string (str): The command(s) to be executed for which the output
                is sought.
            persist (bool): If True, will create a unique file which will not be
                overwritten because of subsequent call of this function.
                Default is False which will write the output to a file
                ``out.out`` in the ansys working directory.  

        Returns:
            str: Path to a file which contains the output of the ansys command call.
        """
        if persist:
            from uuid import uuid4
            output_file = str(uuid4())
        else:
            output_file = "out.out"

        self.send("/output,{}".format(output_file))
        self.send(command_string)
        self.send("/output")
        return os.path.join(self._wd, output_file)

    def get_list(self, command_string, **kwargs):
        """Extract any list from ansys
        
        Function to get any ansys list as a :class:`pandas.DataFrame`.
        
        Example: 

            >>> a.get_list("nlist") 

        .. note:: 
            The function assumes that the ``command_string`` will return a 
            column data.  

            For example, instead of using ``a.get_list("elist")`` you should use 
            ``a.get_list("elist,,,,1")`` For getting element list.

        This function passess all keyword arguments directly to
        :func:`pandas.read_table` function. The default values of
        ``delim_whitespace`` is ``True`` and ``skiprows`` is 2. 
        
        Args:
            command_string (str): The Ansys command which will output a column data
            **kwargs: All keyword arguments for the read_table function in
                pandas is applicable for this function as well.
        
        Returns:
            pandas.Dataframe: A :class:`pandas.DataFrame` with the data that ansys returned when
            ``command_string`` was passed.
        """
        f = self.get_output(command_string)
        if "delim_whitespace" not in kwargs:
            kwargs["delim_whitespace"]=True
        if "skiprows" not in kwargs:
            kwargs["skiprows"] = 2
        return pd.read_table(os.path.join(self._wd,"out.out"), **kwargs)
