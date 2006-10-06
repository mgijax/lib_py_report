
'''
#
# Purpose:
#
# Support routines for printing Editing Interface and other reports.
# These routines are used by all Python reports installed in
# titan:/export/mgd and other ad hoc Python reports.
#
# History:
#
#	lec	10/06/2006
#	- TR 7943; change report headings; remove trailer
#
#       lec     04/24/2002
#	- added fileExt to init()
#
#       lec     04/03/2000
#	- convert to mgi_utils, db from mgdlib
#	- remove accessionlib
#
#       lec     02/07/2000
#	- TR 1350; changes to copyright notice (trailer())
#
#       lec     12/06/1999
#	- TR 830; add parameters to init(), trailer() to format html output
#
#       cjd     12/07/1998
#       - added trailer() function
#
#	lec	11/16/98
#	- changed mgdreport to mgireport
#
#	lec	01/08/98
#	- converted to new mgdlib API
#	- added comments
#	- removed 'def sql()'; obsolete function 
#
'''

import sys
import string
import posix
import os
import mgi_utils
import db

TAB = '\t'
CRT = '\n'
SEP = ', '
DOT = '.   '
SPACE = ' '
PAGE = ''
ULINE = '_'

column_width = 76	# Maximum column width
 
def init(outputfile, 
	 title = None, 
	 outputdir = None, 
	 printHeading = 'JAX', 
	 isHTML = 0, 
	 fileExt = None, 
	 sqlOneConnection = 1,
	 sqlLogging = 1):
	'''
	# requires: outputfile, the name of the output file (string)
	#           title, the title of the report (string)
	#	    outputdir, the directory in which to place the output file (string);
	#	      the default is the current working directory
	#	    printHeading, set to Header Type if the header is to be printed (default is JAX)
	#	    isHTML, set to 1 if the output file is HTML format, 0 otherwise
	#		(default is 0)
	#           fileExt, the file extension of the output file (e.g. ".rpt", ".tab")
	#
	# effects:
	# 1. Opens the output file under $HOME/mgireport directory for writing
	# 2. Initializes the output file with the title of the report, if given
	#
	# returns:
	# The file descriptor which was initialized
	#
	'''

	suffix = ''

	if fileExt != None:
		suffix = fileExt
		if isHTML:
			suffix = suffix + '.html'
	elif isHTML:
		suffix = suffix + '.html'
	else:
		suffix = '.rpt'

	outputfile = os.path.splitext(outputfile)

	if outputdir is None:
		outputdir = os.getcwd()

	filename = outputdir + '/' + outputfile[0] + suffix

	fp = open(filename, 'w')

	if isHTML:
		fp.write("<HTML>")
		fp.write("<BODY>")
		fp.write("<PRE>")
		# see finish_nonps for closing of these markups

	if printHeading is not None:
		header(fp, printHeading)

		if title is not None:
			fp.write(string.center(title, column_width) + 2 * CRT)

	if sqlOneConnection:
		db.useOneConnection(1)

	if sqlLogging:
		db.set_sqlLogFunction(db.sqlLogAll)

	return fp

def header(fp, headerType = "JAX"):
	'''
	# requires: fp, output file descriptor pointing to an open file
	#	headerType, string that denotes which header to use
	# effects: writes the specified header to the file
	'''

	TEXTDIR = os.environ['MGI_DBUTILS'] + '/text/'

	jaxheaderfile = TEXTDIR + 'jax_header'

	if headerType == 'MGI':
	    mgiheaderfile = TEXTDIR + 'mgi_header'
	elif headerType == 'MGD':
	    mgiheaderfile = TEXTDIR + 'mgd_header'
	elif headerType == 'GXD':
	    mgiheaderfile = TEXTDIR + 'gxd_header'
	else:
	    mgiheaderfile = ''

	#
	# always write the JAX header
	#

	jaxheaderfp = open(jaxheaderfile, 'r')
	for l in jaxheaderfp.readlines():
	    fp.write(l)
        fp.write('Date Generated: %s\n\n' % (mgi_utils.date()))

	#
	# specific header only if specified
	#

	if len(mgiheaderfile) > 0:
	    mgiheaderfp = open(mgiheaderfile, 'r')
	    for l in mgiheaderfp.readlines():
	        fp.write(l)

def trailer(fp):
	'''
	# requires: fp, output file descriptor pointing to an open file
	# effects: writes the standard MGI warantee trailer to the output file
	# notes: call this function just before closing. The trailers
	#  should be placed last in the file.
	#
	# obsolete as of TR7943; 
	# remove this entirely once all references to it are removed
	#
	'''

	return

def finish_nonps(fp, isHTML = 0):
	'''
	# requires: fp, the output file descriptor
	#
	# effects:
	# 1. Closes the output file
	#
	# returns:
	#
	'''

	if isHTML:
		fp.write("</PRE>")
		fp.write("</BODY>")
		fp.write("</HTML>")

	fp.close()
	db.useOneConnection(0)
 
def finish_ps(fp, banner = None, options = None):
	'''
	# requires: fp, the output file descriptor
	#           banner, a banner to print (string)
	#           options, a list of  postscript options (string)
	#
	# effects:
	# 1. Closes the open output file
	# 2. Creates and prints a postscript file of the output file
	#    by opening a pipe to a postscript conversion program 'enscript'
	#
	# returns:
	#
	'''

	filename = fp.name
	file = fp.name + '.ps'
	fp.close()
 
        cmd = 'rsh uncompaghre "set path = ($path /usr/local/bin);enscript -b"'
	
	if banner != None:
              cmd = cmd + banner 

	if options != None:
              cmd = cmd + options

	cmd = cmd + '" -fTimes-Roman8 -p' + file + ' ' + filename + '"'
        p = posix.popen(cmd, 'r')
        s = p.read()
        p.close()
	db.useOneConnection(0)

def format_line(str):
	'''
	# requires: str, the line to format (string)
	#
	# effects:
	# Inserts carriage returns and tabs into a string
	# if it is greater than the global column_width.
	# If the length of the string is less than or equal 
	# to the global column_width then
	# no changes to the string are necessary.
	#
	# returns:
	# The converted or unchanged string.
	#
	'''

        newstr = ''
        counter = len(str) / column_width
 
        start = 0
        end = column_width - 1
 
        while (counter):
                newstr = newstr + str[start : end + 1] + CRT + TAB
                start = start + column_width
                end = start + column_width - 1
                counter = counter - 1
 
        newstr = newstr + str[start : ]
        return newstr
 
def create_accession_anchor(id):
	'''
	# requires:  id, the accession id for the anchor
	#
	# effects:
	# constructs an HTML anchor string to the public WI accession CGI using
	# the given id
	#
	# returns:
	# a formatted HTML anchor
	#
	# note:
	# close the anchor using close_accession_anchor()
	#
	'''

	anchor = '<A HREF="http://www.informatics.jax.org/searches/accession_report.cgi?id=%s">' % (id)
	return anchor

def close_accession_anchor():
	'''
	# requires:  nothing
	#
	# effects:
	# constructs an closing HTML anchor string
	#
	# returns:
	# a closing HTML anchor
	#
	# note:
	# create the anchor using create_accession_anchor(), create_imsrstrain_anchor
	#
	'''

	return '</A>'

def create_imsrstrain_anchor(strain):
	'''
	# requires:  strain, the imsr strain for the anchor
	#
	# effects:
	# constructs an HTML anchor string to the public IMSR WI Strain Query using
	# the given string
	#
	# returns:
	# a formatted HTML anchor
	#
	# note:
	# close the anchor using close_imsrstrain_anchor()
	#
	'''

	anchor = '<A HREF="http://www.informatics.jax.org//imsr/fetch?page=imsrSummary&selectedQuery=Strains&query=%s">' % (strain)
	return anchor

