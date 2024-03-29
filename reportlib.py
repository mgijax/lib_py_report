'''
#
# Purpose:
#
# Support routines for printing qcreports_db, reports_db
#
# History:
#
#       lec     12/2023
#       wts2-1155/GOC taking over GOA mouse, GOA human, etc.
#       remove: sqlOneConnection, sqlLogging
#
#       lec     05/31/2012
#       - TR11093/create_accession_anchor/use new flavor of accession link
#
#       lec     04/11/2012
#       - postgres options added
#
#       lec     03/28/2012
#       - TR11027
#       - create_imsrstrain_anchor
#       - create_accession_anchor
#       - use env variable 'WI_URL' when possible
#
'''

import sys
import os
import db
import mgi_utils

TAB = '\t'
CRT = '\n'
SPACE = ' '
PAGE = ''

column_width = 76       # Maximum column width
 
def init(outputfile, 
         title = None, 
         outputdir = None, 
         printHeading = 'JAX', 
         isHTML = 0, 
         fileExt = None):
        '''
        # requires: outputfile, the name of the output file (string)
        #           title, the title of the report (string)
        #           outputdir, the directory in which to place the output file (string);
        #             the default is the current working directory
        #           printHeading, set to Header Type if the header is to be printed (default is JAX)
        #           isHTML, set to 1 if the output file is HTML format, 0 otherwise (default is 0)
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
                header(fp)
                if title is not None:
                        fp.write(str.center(title, column_width) + 2 * CRT)

        db.set_sqlLogFunction(db.sqlLogAll)

        return fp

def header(fp):
        '''
        # requires: fp, output file descriptor pointing to an open file
        # effects: writes the specified header to the file
        '''
        fp.write('#\n# Date Generated: %s\n' % (mgi_utils.date()))
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

