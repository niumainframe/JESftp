JESftp
==============

This is a script/module which automates the submission of JCL files to the [JES](http://publib.boulder.ibm.com/infocenter/zos/basics/topic/com.ibm.zos.zconcepts/zconc_whatisjes.htm) on z/OS mainframes with a compatible FTP server.

This tool will be especially handy for those experiencing NIU's CSCI 360 course.

###Example Usage
    
    $ JESftp.py assign3.jcl
  
The above will automatically do the following:

   1. Send assign3.jcl to the job queue and wait for it to execute.
   2. Save the output of the program in the same directory.
   3. Delete the job off your queue!

It also creates/reads a config file with your credientials.  I like to bind it to the F5 button on [Geany](http://www.geany.org/) for quick feedback.

It's rough around the edges with cross platform compatibility-- mostly with line endings and home directory paths.