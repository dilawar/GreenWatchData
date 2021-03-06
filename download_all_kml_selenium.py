#!/usr/bin/env python3
"""download_all_kml.py: 
Download all kml file.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import glob
from bs4 import BeautifulSoup
import shutil
import time


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

profile = FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False);
ftype = 'application/octet-stream'
profile.set_preference("browser.helperApps.neverAsk.openFile", ftype )
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ftype)
profile.set_preference("browser.download.folderList", 2); 
profile.set_preference("browser.download.dir", "./");
profile.set_preference("browser.helperApps.alwaysAsk.force", False);
profile.set_preference("browser.download.manager.useWindow", False);

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

print("[INFO] Firefox Headless Browser Invoked")

baseUrl_ = 'http://egreenwatch.nic.in/Public/Reports/View_Download_KML.aspx'
downloadBtnID = 'ctl00_ctl00_dpPH_dpPH_btnSearch'
tableId = 'ctl00_ctl00_dpPH_dpPH_gdCALs'
states_ = []
current_page_ = 1
all_files_ = [ ]

dir_  = os.path.join( os.environ['HOME'], 'Downloads' )
resDir_ = None

def find_select_by_id( id ):
    global driver
    ss = driver.find_element_by_id( id )
    return Select(ss)

def html2text( html ):
    soup = BeautifulSoup( html )
    return soup.get_text( ).strip().replace(' ', '_' )

def find_latest_kml_file( ):
    global dir_
    files = glob.glob( '%s/*.kml' % dir_ )
    if files:
        return max( files, key=os.path.getctime )
    else:
        return None

def download_from_table( table, download = True ):
    global current_page_
    global driver
    current_page_ += 1

    # Remove the tooltip
    ttips = table.find_elements_by_xpath( '//div[@id="tooltip"]' )
    for ttip in ttips:
        print( 'Disabling tooltip: %s' % ttip.get_attribute( 'innerHTML') )
        driver.execute_script("""var element = arguments[0];
            element.parentNode.removeChild(element);
            """, ttip)

    trs = table.find_elements_by_xpath( './/tr' )
    print( 'Found %d records' % len(trs))
    for i, tr in enumerate(trs):
        print( ' Row %d' % i, end =  ' ' )
        tds = tr.find_elements_by_xpath('.//td')
        if not tds:
            print( ' nothing found in this row' )
            continue

        text = ':'.join([ x.text for x in tds[1:] if x.text.strip() ])
        text = text.replace( r'/', '' )
        d = tr.find_elements_by_xpath( './/input')
        if not d:
            print( '  not clickable input found' )
            continue
        else:
            d = d[-1]
        filename = os.path.join( resDir_, '%s.kml' % text )
        filename = filename.replace( ' ', '_' )
        if os.path.exists( filename ):
            print( '[INFO] Already downloaded %s' % filename )
            continue
        try:
            d.click()
            print( ' .. downloadin by pressing button ID: %s' % d.get_attribute(
                'id' ), end = ' ' 
                )
            downloadedFiles = find_latest_kml_file( )
            if downloadedFiles is not None:
                assert filename not in all_files_
                all_files_.append(filename)
                shutil.move( downloadedFiles, filename )
                print( '[INFO] Saving to %s' % filename )
        except Exception as e:
            print( 'Could not click: \n\t%s' % e )
            pass


def download_kmp( state, siteType):
    global driver
    global states_
    driver.get( baseUrl_ )
    ss = find_select_by_id( "ctl00_ctl00_dpPH_dpPH_ddlState")
    states_ = [ o.text for o in ss.options ][1:]
    ss.select_by_visible_text( state )

    ss = find_select_by_id( 'ctl00_ctl00_dpPH_dpPH_ddlSiteType' )
    caTypes_ = [ o.text for o in ss.options ][1:]
    print( caTypes_ )
    ss.select_by_visible_text( siteType )

    submit = driver.find_element_by_id( 'ctl00_ctl00_dpPH_dpPH_btnSearch')
    submit.click()

    # now download verything on this page.
    #  pageLink = "javascript:__doPostBack('ctl00$ctl00$dpPH$dpPH$gdCALs','Page$%d')"
    for i in range(30):
        table = driver.find_element_by_xpath( '//table[@id="%s"]' % tableId )
        download_from_table( table, download = False )

        # refresh the table.
        pages = table.find_elements_by_xpath( './/td[@colspan="11"]//a' )
        if not pages:
            print( 'No more pages. Break')
            break

        found = False
        for p in pages:
            try:
                href = p.get_attribute( 'href')
            except Exception as e:
                print( 'Could not find href in td' )
                continue
            if 'Page$%d'% current_page_ in href:
                try:
                    p.click()
                    print( 'Great next page: %s' % current_page_ )
                    found = True
                    break
                except Exception as e:
                    print( 'Could not load page: %s' % e )
        if not found:
            break

def main( ):
    global driver
    global resDir_
    state = sys.argv[1]
    siteType = sys.argv[2]
    resDir_ = os.path.join( state, siteType )
    if not os.path.isdir( resDir_ ):
        os.makedirs( resDir_ )

    print( '[INFO]  State: %s, Site Type: %s' % (state, siteType))
    download_kmp( state, siteType)
    driver.quit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print( 'CTRL+C' )
        driver.quit()
