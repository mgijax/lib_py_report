
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
#	lec	05/31/2012
#	- TR11093/create_accession_anchor/use new flavor of accession link
#
#	lec	04/11/2012
#	- postgres options added
#
#	lec	03/28/2012
#	- TR11027
#	- create_imsrstrain_anchor
#	- create_accession_anchor
#	- use env variable 'WI_URL' when possible
#
#	lec	10/25/2007
#	- TR 8557; create_accession_anchor/isANCHOR
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

import pg_db
db = pg_db
db.setAutoTranslateBE()

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

	try:
        	if os.environ['DB_TYPE'] == 'sybase':
			if sqlLogging:
				db.set_sqlLogFunction(db.sqlLogAll)
	except:
		if sqlLogging:
			db.set_sqlLogFunction(db.sqlLogAll)

	return fp

def header(fp, headerType = "JAX"):
	'''
	# requires: fp, output file descriptor pointing to an open file
	#	headerType, string that denotes which header to use
	# effects: writes the specified header to the file
	'''

	jaxheaderfile = '# The Jackson Laboratory - Mouse Genome Informatics (MGI)\n# Copyright 1996, 1999, 2002, 2005, 2008 The Jackson Laboratory\n# All Rights Reserved\n'


	#
	# always write the JAX header
	#

        fp.write(jaxheaderfile)
        fp.write('# Date Generated: %s\n' % (mgi_utils.date()))

	#
	# special case
	#

	if headerType == 'JAX':
	    fp.write('#\n')
        else:
	    fp.write('# (server = %s, database = %s)\n#\n\n' % (db.get_sqlServer(), db.get_sqlDatabase()))

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
 
def create_accession_anchor(id, accType = None):
	'''
	# requires:  id, the accession id for the anchor
	#            accType, type of accession id ('marker', 'reference') for MGI 5.0
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

	serverName = os.environ['SERVER_NAME']
	url = os.environ['WI_URL']

	#
	# MGI 5.0/fewi
	#
	if accType in ('marker', 'reference'):
	    anchor = '<A HREF="%s%s/%s">' % (url, accType, id)

	#
	# non-fewi (python/java wi)
	#
	else:
	    anchor = '<A HREF="%saccession/%s">' % (url, id)

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
	# constructs an HTML anchor string to the public IMSR Strain Query
	# using the given string
	#
	# returns:
	# a formatted HTML anchor
	#
	# note:
	# close the anchor using close_imsrstrain_anchor()
	#
	'''

	anchor = '<A HREF="http://www.findmice.org/summary?query=%22' + strain + '%22">'

	return anchor

