#!/usr/bin/python
"""
submit_job.py

This script does three things:
   1. Transmits your .jcl file to the Mainframe's JES via FTP
      (and waits for the mainframe to process the job)
   2. Retrieves the job and saves it as a .job file in the same dir
   3. Clears the job from your queue so that you don't have clear it 
      with ISPF later.

Looks for a config file which contains your credentials in your home
directory or script's directory;  will generate if not found.


Written for: CSCI 360 - Computer Programming in Assembler Language
             Northern Illinois University

Vincent Schramer
vschramer@niu.edu

"""

from ftplib import FTP, Error
import re, os, sys, time, argparse, ConfigParser, getpass

# Function generateConfig
# Quick way to generate a config file.
def generateConfig(path):
   
   # Create new config object
   config = ConfigParser.RawConfigParser()
   
   # Obtain needed config values from stdin
   server = raw_input("Host [zos.kctr.marist.edu]: ")
   if server == "":
      server = 'zos.kctr.marist.edu'

   username = raw_input("User ID: ")
   password = getpass.getpass("Password (written plaintext): ")
   
   # Add to config object
   config.add_section(conf_sect)
   config.set(conf_sect, 'server', server)
   config.set(conf_sect, 'username', username)
   config.set(conf_sect, 'password', password)
   
   # Write config to file
   with open(try_path, 'wb') as configfile:
      config.write(configfile)

   print "Config file written to " + try_path
 
 




# -----------------------------
# Configuration File Parsing
# -----------------------------

conf_filename  = '.submit_job.cfg'
conf_sect      = 'submit_job'
conf_path      = None
conf_paths     = (os.getenv("HOME"), sys.path[0])

# Search for config file.
for p in conf_paths:
   try_path = p + '/' + conf_filename
   
   if os.path.exists(try_path): 
      conf_path = try_path
      break

 
if conf_path == None:
   print "Cannot find config file, lets create one."
   generateConfig(try_path)
   conf_path = try_path
   
   
# Attempt to read config file.
config = ConfigParser.RawConfigParser()
if len(config.read(conf_path)) != 1:
   print "Could not open " + conf_path
   exit()

# Retrieve needed configuration options.
username = config.get(conf_sect, 'username')
password = config.get(conf_sect, 'password')
server   = config.get(conf_sect, 'server')


# -----------------------------
# Parse command line arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("JCLFile", help="The JCL file to send")
args = parser.parse_args()


# I/O files
jclPath     = os.path.abspath(args.JCLFile)
jclBaseName = os.path.basename(jclPath)
outputPath  = os.path.dirname(jclPath) + "/" + jclBaseName + ".job"


# Attempt to open the files
try:
   
   try_file = jclPath
   jclFile = open(try_file, 'r')
   
   try_file = outputPath
   outputFile = open(try_file, 'wb')
   
except IOError as e:
   print 'Could not open file ' + try_file
   print e.args[1]
   exit()



# Begin connection to FTP server
try:

   print "Connecting to " + server + "... ",
   ftp = FTP()
   ftp.connect(server)   
   ftp.login(username, password)
   print "connected!"

   ftp.sendcmd("SITE FILETYPE=jes")

   # Attempt to upload the file
   print "Sending " + jclBaseName + " to the job entry spooler... "
   storResult = ftp.storlines("STOR "+jclBaseName, jclFile)
   
   
   
   
   # Extract the JOB id from the response code
   re = re.search("JOB[0-9]+", storResult)
   
   if re == None:
      raise Error("JOBID was not returned by the server for some reason... " + storResult)

   JOBID = storResult[re.start():re.end()]
   
   print ""
   print "Assigned JOBID: " + JOBID
   
   
   
   
   # Attempt to retrieve the resulting file
   time.sleep(1)   # Give the mainframe a moment to ready the file.
   while (True):
      
      try:
         # This lambda is a hack to make sure a newline character is written at the end of each line.
         ftp.retrlines("RETR "+JOBID+".x", lambda line: outputFile.write('%s\n' % line))
         print "Retrieved job"
         print ""
         
         break
         
      except error_perm as e:
         # If the server doesn't know about the job, wait awhile to try again.
         print e
         print JOBID
         ftp.retrlines("LIST " + JOBID)
         time.sleep(5)
      
   
   # Delete the job off the mainframe   
   print "Deleting " + JOBID
   ftp.delete(JOBID);
   
   
except Error as e:
   print "Error: ",
   print e
      
finally:
   print "Closing connection"
   
   ftp.close()
   
   jclFile.close()
   outputFile.close()


