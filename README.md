JESftp
==============

This is a script/module which automates the submission of JCL files to the [JES](http://publib.boulder.ibm.com/infocenter/zos/basics/topic/com.ibm.zos.zconcepts/zconc_whatisjes.htm) on z/OS mainframes with a compatible FTP server.
It is written in Python 2.7.

This tool will be especially handy for those experiencing NIU's CSCI 360 course.  It allows one to have a much more
flexible workflow when writing and debugging assembler programs on a remote mainframe.

###Example Usage
    
    $ JESftp.py assign3.jcl
  
The above will automatically do the following:

   1. Send assign3.jcl to the job queue and wait for it to execute.
   2. Save the output of the program in the same directory (with txt extension).
   3. Delete the job off your queue!

It also creates/reads a config file with your credientials so that you don't have to type them in.  It looks in your home directory or the directory of the script for this file.

###Quick install on department servers (or other unix systems)
Simply run this command in your terminal:

      wget https://raw.github.com/scvnc/JESftp/master/JESftp-install.sh -q -O - | bash

This will download the latest version of JESftp.py and place it in your ~/bin directory.
After that, it will work as a command for your user.  You may have to relogin to your terminal.

###Important Notes for student use
*  **Make sure that you are using spaces instead of tabs.**  
   Many text editors allow you to define what occurs when the tab key is pressed.  Make sure to configure your editor
   to insert spaces instead of tabs.  This is important because the mainframe assembler does not handle the tab character as whitespace 
   and will complain of an invalid character of sorts.
   
*  **Character encoding issues reported by your editor.**    
It was noticed that if your Job produces characters that do not translate to ASCII/UTF-8, 
the remote server will still return those invalid characters. This is problematic with some 
editors such as Geany and Gedit that will display an error message. You can open the file in a more forgiving
editor such as vi and the unknown characters will be represented.  An example of this is if you try to print a field
of encoded characters, but overshoot the boundry and start printing packed decimal encoded bytes too... this will cause problems.


###Other Notes
I like to bind it to the F5 button on [Geany](http://www.geany.org/) for quick feedback.
Cross platform compatability has been tested between Windows and Linux and should have no problems on Mac.

Looking back, the module is suffering from a case of bad class cohesion.

Licensed under the GNU General Public License.

### Alternative implemenations

[MVSTool] (https://github.com/john-charles/MVSTool) Another student implementation in Java.

[MVS::JESFTP] (http://search.cpan.org/~mikeo/MVS-JESFTP-1.1/JESFTP.pm) Implementation in perl.

[IBM Java Example] (http://www.ibm.com/developerworks/systems/library/es-batch-zos.html)

