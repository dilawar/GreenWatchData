"""rename.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import re
import shutil

def rename( f ):
    newname = re.sub(r'[^\x00-\x7F]', '', str(f))
    newname = newname.replace( ' ', '_' )
    if f == newname:
        return
    print( '- %s TO %s' % ( f, newname) )
    try:
        shutil.move( f, newname )
    except Exception as e:
        print( '[WARN] Failed to move %s' % f )

def main():
    files = []
    for d, sd, fs in os.walk( '.' ):
        for f in fs:
            if '.kml' not in f:
                continue
            if os.path.exists( os.path.join(d,f)):
                files.append( os.path.join(d,f))

    print( 'Total files to rename %d' % len(files))
    [ rename( f ) for f in files ]

if __name__ == '__main__':
    main()
