
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: *****N10338471*****
#    Student name: *****FERNANDO BARBOSA SILVA*****
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  What's On?: Online Entertainment Planning Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for planning an entertainment schedule.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.  You may import other widgets
# from the Tkinter module provided they are ones that come bundled
# with a standard Python 3 implementation and don't have to
# be downloaded and installed separately.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed one day).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it as a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
##def download(url = 'http://www.wikipedia.org/',
##             target_filename = 'download',
##             filename_extension = 'html'):
##
##    # Import an exception raised when a web server denies access
##    # to a document
##    from urllib.error import HTTPError
##
##    # Open the web document for reading
##    try:
##        web_page = urlopen(url)
##    except ValueError:
##        raise Exception("Download error - Cannot find document at URL '" + url + "'")
##    except HTTPError:
##        raise Exception("Download error - Access denied to document at URL '" + url + "'")
##    except:
##        raise Exception("Download error - Something went wrong when trying to download " + \
##                        "the document at URL '" + url + "'")
##
##    # Read its contents as a Unicode string
##    try:
##        web_page_contents = web_page.read().decode('UTF-8')
##    except UnicodeDecodeError:
##        raise Exception("Download error - Unable to decode document at URL '" + \
##                        url + "' as Unicode text")
##
##    # Write the contents to a local text file as Unicode
##    # characters (overwriting the file if it
##    # already exists!)
##    try:
##        text_file = open(target_filename + '.' + filename_extension,
##                         'w', encoding = 'UTF-8')
##        text_file.write(web_page_contents)
##        text_file.close()
##    except:
##        raise Exception("Download error - Unable to write to file '" + \
##                        target_file + "'")
##
##    # Return the downloaded document to the caller
##    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution--------------------------------------------------------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the planner file. To simplify marking, your program should
# generate its entertainment planner using this file name.
#planner_file = 'planner.html'

from time import asctime


# GLOBAL VARIABLES

item_selected_abc = 0
item_selected_museum = 0
item_selected_tvguide = 0

total_selected = 0

main_window = ''


# LIST TO CREATE OPTION LIST AND WEBPAGE

abc_dates =[]
abc_title =[]
abc_image =[]

museum_dates =[]
museum_title =[]
museum_image =[]

tvguide_dates =[]
tvguide_title =[]
tvguide_image =[]


# VARIABLES TO DEFINE THE PRINT LIST

list_selected_abc = [0,0,0,0,0,0]
list_selected_museum = [0,0,0,0,0,0]
list_selected_tvguide = [0,0,0,0,0,0]


#####################################################################################################################
#---------------------------------------DOWNLOAD THE WEBPAGE FILE TO A VARIABLE AS A STRING-------------------------#
#####################################################################################################################

#-----------------------------------------  ABC WEBPAGE ------------------------------------------------------------#
url_abc = 'https://www.abc.net.au/radionational/programs/theminefield/'

#FUNCTION TO DOWNLOAD THE WEBPAGE FROM THE URL ABOVE
def web_page_downloader_abc(url):
    global abc_dates
    global abc_title
    global abc_image
    
    url_to_download = url
    web_page = urlopen(url_to_download)
    web_page_bytes = web_page.read()
    web_page_ascii = web_page_bytes.decode('utf-8', 'backslashreplace')
    web_page_ascii = web_page_ascii.replace('\u2019',"’")
    web_page_ascii = web_page_ascii.replace('\\','' )
    web_page_ascii = web_page_ascii.replace('&#039;',"'" )

    # FIND THE DATES
    date_result = findall('<div class="article-index section ct-teaser-view cs-tabbed">[\s]*<h3>[a-zA-Z ]*([0-9 ]*[a-zA-Z ]*[0-9]*)</h3>',
                     web_page_ascii)
    abc_dates = date_result
    
    # FIND THE TITLE
    title_result = findall('''<h3 class="title"><[a-zA-Z0-9 -:/"?.=]*>([a-zA-Z0-9 ?;:'',’\-]*)</a>''',
                           web_page_ascii)
    abc_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''<img src="(https://www.abc.net.au/radionational/image/[0-9]*-4x3-[0-9x]*[A-Za-z\.\-]+)"''',
                     web_page_ascii)
    abc_image = image_result


###CREATE THE OFFLINE FILE
    #html_file = open( 'archive/abc.txt', 'w', encoding = 'utf-8')
    #html_file.write(str(web_page_ascii))
    #html_file.close()
#web_page_downloader_abc(url_abc)

#-----------------------------------------------

#ABC OFF_LINE FILE TO A VARIABLE AS A STRING
file_abc ='archive/abc.txt'

def file_abc_search(file):
    global abc_dates
    global abc_title
    global abc_image

    file =open(file_abc,'r')
    file = file.read()
    file1 = file

    # FIND THE DATES
    date_result = findall('<div class="article-index section ct-teaser-view cs-tabbed">[\s]*<h3>[a-zA-Z ]*([0-9 ]*[a-zA-Z ]*[0-9]*)</h3>',
                     str(file1))
    abc_dates = date_result
    
    # FIND THE TITLE
    title_result = findall('''<h3 class="title"><[a-zA-Z0-9 -:/"?.=]*>([a-zA-Z0-9 ?;:'',’\-]*)</a>''',
                           str(file1))
    abc_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''<img src="(https://www.abc.net.au/radionational/image/[0-9]*-4x3-[0-9x]*[A-Za-z\.\-]+)"''',
                           str(file1))
    abc_image = image_result

#--------------------------------------------------------------------------------------------------------------------#

#-----------------------------------------  MUSEUM WEBPAGE-----------------------------------------------------------#
url_museum = 'https://www.oldmuseum.org/'

#FUNCTION TO DOWNLOAD THE WEBPAGE FROM THE URL ABOVE
def web_page_downloader_museum(url):

    global museum_dates
    global museum_title
    global museum_image
    
    url_to_download = url
    web_page = urlopen(url_to_download)
    web_page_bytes = web_page.read()
    web_page_ascii = web_page_bytes.decode('utf-8', 'backslashreplace')
    web_page_ascii = web_page_ascii.replace('\u2019',"’")
    web_page_ascii = web_page_ascii.replace('\\','' )
    web_page_ascii = web_page_ascii.replace('&#039;',"'" )

    # FIND THE DATES
    date_result = findall('class="summary-thumbnail-event-date-month">([a-zA-Z]*)</span>[\s]*<span[\s]*class="summary-thumbnail-event-date-day">([0-9]*)',
                     web_page_ascii)

    # Merge Month and day in a List to be used together
    date_result_list = []
    for i in range (len(date_result)):
        date = str(date_result[i])
        date = date.replace('(','[')
        date = date.replace(')',']')
        date = date.replace(","," " )
        date = date.replace("'", "")
        date = date.replace("[","")
        date = date.replace("]","")
        date_result_list.append(date)

    museum_dates = date_result_list
    
    # FIND THE TITLE
    title_result = findall('''class="summary-title-link">([a-zA-Z\- \W]*)</a>''',
                           web_page_ascii)
    museum_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''data-image="(https://static1.squarespace.com/static/591d35bf1b10e3036133256f/5976a9751e5b6c546cf01744/[a-z-A-Z0-9\/\_\.+)]*)''',
                     web_page_ascii)
    museum_image = image_result

###CREATE THE OFFLINE FILE
#    html_file = open( 'archive/museum.txt', 'w', encoding = 'utf-8')
#    html_file.write(str(web_page_ascii))
#    html_file.close()  
#web_page_downloader_museum(url_museum)


#-----------------------------------------------

#museum OFF_LINE FILE TO A VARIABLE AS A STRING
file_museum ='archive/museum.txt'

def file_museum_search(file):
    global museum_dates
    global museum_title
    global museum_image

    file =open(file_museum,'r')
    file = file.read()
    file1 = file

    # FIND THE DATES
    date_result = findall('class="summary-thumbnail-event-date-month">([a-zA-Z]*)</span>[\s]*<span[\s]*class="summary-thumbnail-event-date-day">([0-9]*)',
                     str(file1))

    # Merge Month and day in a List to be used together
    date_result_list = []
    for i in range (len(date_result)):
        date = str(date_result[i])
        date = date.replace('(','[')
        date = date.replace(')',']')
        date = date.replace(","," " )
        date = date.replace("'", "")
        date = date.replace("[","")
        date = date.replace("]","")
        date_result_list.append(date)
    museum_dates = date_result_list

    
    # FIND THE TITLE
    title_result = findall('''class="summary-title-link">([a-zA-Z\- \W]*)</a>''',
                           str(file1))
    museum_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''data-image="(https://static1.squarespace.com/static/591d35bf1b10e3036133256f/5976a9751e5b6c546cf01744/[a-z-A-Z0-9\/\_\.+)]*)''',
                           str(file1))
    museum_image = image_result

file_museum_search(file_museum)
#--------------------------------------------------------------------------------------------------------------------#

#----------------------------------------- TVGUIDE WEBPAGE-----------------------------------------------------------#
url_tvguide = 'https://www.tvguide.com/tv-premiere-dates/'

#FUNCTION TO DOWNLOAD THE WEBPAGE FROM THE URL ABOVE
def web_page_downloader_tvguide(url):
    global tvguide_dates
    global tvguide_title
    global tvguide_image
    
    url_to_download = url
    web_page = urlopen(url_to_download)
    web_page_bytes = web_page.read()
    web_page_ascii = web_page_bytes.decode('utf-8', 'backslashreplace')
    web_page_ascii = web_page_ascii.replace('\u2019',"’")
    web_page_ascii = web_page_ascii.replace('\\','' )
    web_page_ascii = web_page_ascii.replace('&#039;',"'" )

    # FIND THE DATES
    date_result = findall('data-date="([0-9\-]*)"',
                     web_page_ascii)
    tvguide_dates = date_result
    
    # FIND THE TITLE
    title_result = findall('''href="https://www.tvguide.com/tvshows/[a-zA-Z0-9\-\/"]*>([a-zA-Z0-9 ',\-\:]*)''',
                           web_page_ascii)
    tvguide_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''data-amp-src="(https://static.tvgcdn.net/feed/1/[a-z0-9\/\.\_]*)" />''',
                     web_page_ascii)
    tvguide_image = image_result

###CREATE THE OFFLINE FILE
#    html_file = open( 'archive/tvguide.txt', 'w', encoding = 'utf-8')
#    html_file.write(str(web_page_ascii))
#    html_file.close()  
#web_page_downloader_tvguide(url_tvguide)

#-----------------------------------------------

#tvguide OFF_LINE FILE TO A VARIABLE AS A STRING
file_tvguide ='archive/tvguide.txt'

def file_tvguide_search(file):
    global tvguide_dates
    global tvguide_title
    global tvguide_image

    file =open(file_tvguide,'r')
    file = file.read()
    file1 = file

    # FIND THE DATES
    date_result = findall('data-date="([0-9\-]*)"',
                     str(file1))
    tvguide_dates = date_result
    
    # FIND THE TITLE
    title_result = findall('''href="https://www.tvguide.com/tvshows/[a-zA-Z0-9\-\/"]*>([a-zA-Z0-9 ',\-\:]*)''',
                           str(file1))
    tvguide_title = title_result

    # FIND THE IMAGE URL
    image_result = findall('''data-amp-src="(https://static.tvgcdn.net/feed/1/[a-z0-9\/\.\_]*)" />''',
                           str(file1))
    tvguide_image = image_result


#--------------------------------------------------------------------------------------------------------------------#


#####################################################################################################################
#---------------------------------------------- START THE MAIN PROGRAM----------------------------------------------#
#####################################################################################################################    

# START THE MAIN INTERFACE WHINDOW
def root_window():

    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#
    #                                             TOPLEVEL WINDOWS                                             #
    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#

    # CHECKBUTTONS FONT DEFINITION FOR THE TOP LEVEL WINDOWS
    font_checkbox = 'Arial'
    font_size_checkbox = 16

    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤  WHIDOW WITH ABC OPTIONS  ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#
    
    #DEFINE WEB OR OFFLINE INFORMATION TO BE USED BY THE PROGRAM
    def window_abc():
        if offline_checkbox_var.get()==1:
            file_abc_search(file_abc)
            #print(offline_checkbox_var.get())
        else:
            try:
                web_page_downloader_abc(url_abc)
            except:
                print("Not internet connection - Program in offline mode.")
                internet_connection()
                file_abc_search(file_abc)

        check_box_abc()

    
    #CREATE THE ABC WINDOW OPTIONS LIST    
    def check_box_abc():
        # DISABLE BUTTON ABC
        abc_button.config(state=(['disable']))

        ## CRETATE THE ABC WINDOW
        #global abc_window
        abc_window = Toplevel(main_window)
        abc_window.title ('ABC Radio')
        abc_window.geometry('1200x700') 
        abc_window.resizable(width=False, height=False)
        abc_color = 'light green'

        ## CHECBUTTONS STATUS    
        abc_checkbox_1_var = IntVar()
        abc_checkbox_2_var = IntVar() 
        abc_checkbox_3_var = IntVar() 
        abc_checkbox_4_var = IntVar() 
        abc_checkbox_5_var = IntVar() 
        abc_checkbox_6_var = IntVar() 

        ## COUNT THE NUMBER OF ITEMS SELECTED    
        def update_select_abc():
            global item_selected_abc
            global list_selected_abc
 
            # COUNT THE ITEMS SELECTED 
            count_abc = int((abc_checkbox_1_var.get() + abc_checkbox_2_var.get() + abc_checkbox_3_var.get()+
                               abc_checkbox_4_var.get() + abc_checkbox_5_var.get() + abc_checkbox_6_var.get()))
            item_selected_abc = count_abc
            
            # CREATE A LIST OF THE ITEMS SELECTED 
            list_selected_abc = [abc_checkbox_1_var.get() , abc_checkbox_2_var.get() , abc_checkbox_3_var.get(),
                               abc_checkbox_4_var.get() , abc_checkbox_5_var.get() , abc_checkbox_6_var.get()]

            # UPDATE EVENTS SELECTED IN THE MAIN WINDOW
            status_screen()
            
        ## CREATE THE WIDGEDS

        # LABEL
        # 1
        label_abc = Label(abc_window, text = 'ABC RADIO SCHEDULE LIST',
                          font = ('arial',36),
                          bg = abc_color,
                          width = "41")
        
        # CHECKBUTTONS  
        #  1
        abc_checkbox_1 = Checkbutton(abc_window, text = '1: ' + abc_dates[0]+' : '+abc_title[0],
                                     variable = abc_checkbox_1_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc)    
        #  2
        abc_checkbox_2 = Checkbutton(abc_window, text='2: ' + abc_dates[1]+' : '+abc_title[1],
                                     variable = abc_checkbox_2_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc)   
        #  3
        abc_checkbox_3 = Checkbutton(abc_window, text='3: ' + abc_dates[2]+' : '+abc_title[2],
                                     variable = abc_checkbox_3_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc)   
        #  4
        abc_checkbox_4 = Checkbutton(abc_window, text='4: ' + abc_dates[3]+' : '+abc_title[3],
                                     variable = abc_checkbox_4_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc) 
        #  5
        abc_checkbox_5 = Checkbutton(abc_window, text='5: ' + abc_dates[4]+' : '+abc_title[4],
                                     variable = abc_checkbox_5_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc)
        #  6
        abc_checkbox_6 = Checkbutton(abc_window, text='6: ' + abc_dates[5]+' : '+abc_title[5],
                                     variable = abc_checkbox_6_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_abc)
        #  7
        label_abc_url = Label(abc_window, text = url_abc, font = ('arial',16) )
        
        
        ## WIDGETS LAYOUT

        label_abc.grid(row = 0, column = 1, padx=20, pady=20)
        abc_checkbox_1.grid(row = 1, column = 1, sticky = W, padx=20, pady=20)
        abc_checkbox_2.grid(row = 2, column = 1, sticky = W, padx=20, pady=20)
        abc_checkbox_3.grid(row = 3, column = 1, sticky = W, padx=20, pady=20)
        abc_checkbox_4.grid(row = 4, column = 1, sticky = W, padx=20, pady=20)
        abc_checkbox_5.grid(row = 5, column = 1, sticky = W, padx=20, pady=20)
        abc_checkbox_6.grid(row = 6, column = 1, sticky = W, padx=20, pady=20)
        label_abc_url.grid(row = 7, column = 1, sticky = W, padx=20, pady=20)

        abc_window.mainloop()


    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤  WHIDOW WITH MUSEUM OPTIONS  ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#

    #DEFINE WEB OR OFFLINE INFORMATION TO BE USED BY THE PROGRAM
    def window_museum():
        if offline_checkbox_var.get()==1:
            file_museum_search(file_museum)
        else:
            try:
                web_page_downloader_museum(url_museum) 
            except:
                print("Not internet connection - Program in offline mode.")
                internet_connection()
                file_museum_search(file_museum)
        check_box_museum()
     
    #CREATE THE MUSEUM WINDOW OPTIONS LIST    
    def check_box_museum():
        # DISABLE BUTTON museum
        museum_button.config(state=(['disable']))

        ## CRETATE THE MUSEUM WINDOW PROPERTIES
        global museum_window
        museum_window = Toplevel(main_window)
        museum_window.title ('Old Museum')
        museum_window.geometry('1200x700') 
        museum_window.resizable(width=False, height=False)
        widged_color = 'light blue'
        

        ## CHECBUTTONS STATUS    
        museum_checkbox_1_var = IntVar() 
        museum_checkbox_2_var = IntVar() 
        museum_checkbox_3_var = IntVar() 
        museum_checkbox_4_var = IntVar()
        museum_checkbox_5_var = IntVar()
        museum_checkbox_6_var = IntVar()

        ## COUNT THE NUMBER OF ITEMS SELECTED    
        def update_select_museum():
            global item_selected_museum
            global list_selected_museum

            # COUNT THE ITEMS SELECTED 
            count_museum = int((museum_checkbox_1_var.get() + museum_checkbox_2_var.get() + museum_checkbox_3_var.get()+
                               museum_checkbox_4_var.get() + museum_checkbox_5_var.get() + museum_checkbox_6_var.get()))
            item_selected_museum = count_museum
            
            # CREATE A LiST OF THE ITEMS SELECTED 
            list_selected_museum = [museum_checkbox_1_var.get() , museum_checkbox_2_var.get() , museum_checkbox_3_var.get(),
                               museum_checkbox_4_var.get() , museum_checkbox_5_var.get() , museum_checkbox_6_var.get()]

            # UPDATE EVENTS SELECTED IN THE MAIN WINDOW
            status_screen()
            
        ## CREATE THE WIDGEDS

        # LABEL
        # 1
        label_museum = Label(museum_window, text = 'OLD MUSEUM SCHEDULE LIST',
                             font = ('arial',36),
                             bg = widged_color,
                             width = "41")
        
        # CHECKBUTTONS  
        #  1
        museum_checkbox_1 = Checkbutton(museum_window, text = '1: ' + museum_dates[0]+' : '+museum_title[0],
                                     variable = museum_checkbox_1_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum)    
        #  2
        museum_checkbox_2 = Checkbutton(museum_window, text='2: ' + museum_dates[1]+' : '+museum_title[1],
                                     variable = museum_checkbox_2_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum)   
        #  3
        museum_checkbox_3 = Checkbutton(museum_window, text='3: ' + museum_dates[2]+' : '+museum_title[2],
                                     variable = museum_checkbox_3_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum)   
        #  4
        museum_checkbox_4 = Checkbutton(museum_window, text='4: ' + museum_dates[3]+' : '+museum_title[3],
                                     variable = museum_checkbox_4_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum) 
        #  5
        museum_checkbox_5 = Checkbutton(museum_window, text='5: ' + museum_dates[4]+' : '+museum_title[4],
                                     variable = museum_checkbox_5_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum)
        #  6
        museum_checkbox_6 = Checkbutton(museum_window, text='6: ' + museum_dates[5]+' : '+museum_title[5],
                                     variable = museum_checkbox_6_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_museum)
        #  7
        label_museum_url = Label(museum_window, text = url_museum, font = ('arial',16) )
        
        
        ## WIDGETS LAYOUT

        label_museum.grid(row = 0, column = 1, padx=20, pady=20)
        museum_checkbox_1.grid(row = 1, column = 1, sticky = W, padx=20, pady=20)
        museum_checkbox_2.grid(row = 2, column = 1, sticky = W, padx=20, pady=20)
        museum_checkbox_3.grid(row = 3, column = 1, sticky = W, padx=20, pady=20)
        museum_checkbox_4.grid(row = 4, column = 1, sticky = W, padx=20, pady=20)
        museum_checkbox_5.grid(row = 5, column = 1, sticky = W, padx=20, pady=20)
        museum_checkbox_6.grid(row = 6, column = 1, sticky = W, padx=20, pady=20)
        label_museum_url.grid(row = 7, column = 1, sticky = W, padx=20, pady=20)

        museum_window.mainloop()

    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤  WHIDOW WITH TVGUIDE OPTIONS  ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#
    
    #DEFINE WEB OR OFFLINE INFORMATION TO BE USED BY THE PROGRAM
    def window_tvguide():
        if offline_checkbox_var.get()==1:
            file_tvguide_search(file_tvguide)
        else:
            try:
                web_page_downloader_tvguide(url_tvguide) 
            except:
                print("Not internet connection - Program in offline mode.")
                internet_connection()
                file_tvguide_search(file_tvguide)
        check_box_tvguide()
  
    #CREATE THE tvguide WINDOW OPTIONS LIST    
    def check_box_tvguide():
        # DISABLE BUTTON tvguide
        tvguide_button.config(state=(['disable']))

        ## CRETATE THE tvguide WINDOW
        global tvguide_window  
        tvguide_window = Toplevel(main_window)
        tvguide_window.title ('TV Guide')
        tvguide_window.geometry('1200x700') 
        tvguide_window.resizable(width=False, height=False)
        widged_color = 'light yellow'

        ## CHECBUTTONS STATUS    
        tvguide_checkbox_1_var = IntVar()
        tvguide_checkbox_2_var = IntVar() 
        tvguide_checkbox_3_var = IntVar() 
        tvguide_checkbox_4_var = IntVar() 
        tvguide_checkbox_5_var = IntVar() 
        tvguide_checkbox_6_var = IntVar() 

        ## COUNT THE NUMBER OF ITEMS SELECTED    
        def update_select_tvguide():
            global item_selected_tvguide
            global list_selected_tvguide         
            
            # COUNT THE ITEMS SELECTED 
            count_tvguide = int((tvguide_checkbox_1_var.get() + tvguide_checkbox_2_var.get() +
                                 tvguide_checkbox_3_var.get()+ tvguide_checkbox_4_var.get() +
                                 tvguide_checkbox_5_var.get() + tvguide_checkbox_6_var.get()))
            item_selected_tvguide = count_tvguide
            
            # CREATE A LiST OF THE ITEMS SELECTED 
            list_selected_tvguide = [tvguide_checkbox_1_var.get() , tvguide_checkbox_2_var.get() ,
                                     tvguide_checkbox_3_var.get(),tvguide_checkbox_4_var.get() ,
                                     tvguide_checkbox_5_var.get() , tvguide_checkbox_6_var.get()]
            
            # UPDATE EVENTS SELECTED IN THE MAIN WINDOW
            status_screen()

        ## CREATE THE WIDGEDS

        # LABEL
        # 1
        label_tvguide = Label(tvguide_window, text = 'TV GUIDE SCHEDULE LIST',
                              font = ('arial',36),
                              bg = widged_color,
                              width = "41")
        
        # CHECKBUTTONS  
        #  1
        tvguide_checkbox_1 = Checkbutton(tvguide_window, text = '1: ' + tvguide_dates[0]+' : '+tvguide_title[0],
                                     variable = tvguide_checkbox_1_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide)    
        #  2
        tvguide_checkbox_2 = Checkbutton(tvguide_window, text='2: ' + tvguide_dates[1]+' : '+tvguide_title[1],
                                     variable = tvguide_checkbox_2_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide)   
        #  3
        tvguide_checkbox_3 = Checkbutton(tvguide_window, text='3: ' + tvguide_dates[2]+' : '+tvguide_title[2],
                                     variable = tvguide_checkbox_3_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide)   
        #  4
        tvguide_checkbox_4 = Checkbutton(tvguide_window, text='4: ' + tvguide_dates[3]+' : '+tvguide_title[3],
                                     variable = tvguide_checkbox_4_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide) 
        #  5
        tvguide_checkbox_5 = Checkbutton(tvguide_window, text='5: ' + tvguide_dates[4]+' : '+tvguide_title[4],
                                     variable = tvguide_checkbox_5_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide)
        #  6
        tvguide_checkbox_6 = Checkbutton(tvguide_window, text='6: ' + tvguide_dates[5]+' : '+tvguide_title[5],
                                     variable = tvguide_checkbox_6_var,
                                     font = (font_checkbox,font_size_checkbox),
                                     command = update_select_tvguide)
        #  7
        label_tvguide_url = Label(tvguide_window, text = url_tvguide, font = ('arial',16))
        
        ## WIDGETS LAYOUT

        label_tvguide.grid(row = 0, column = 1, padx=20, pady=20)
        tvguide_checkbox_1.grid(row = 1, column = 1, sticky = W, padx=20, pady=20)
        tvguide_checkbox_2.grid(row = 2, column = 1, sticky = W, padx=20, pady=20)
        tvguide_checkbox_3.grid(row = 3, column = 1, sticky = W, padx=20, pady=20)
        tvguide_checkbox_4.grid(row = 4, column = 1, sticky = W, padx=20, pady=20)
        tvguide_checkbox_5.grid(row = 5, column = 1, sticky = W, padx=20, pady=20)
        tvguide_checkbox_6.grid(row = 6, column = 1, sticky = W, padx=20, pady=20)
        label_tvguide_url.grid(row = 7, column = 1, sticky = W, padx=20, pady=20)

        tvguide_window.mainloop()
    #¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤#

    #-------------------------------------------------------------------------------------------------------#
    #                                           FUNCTIONS                                                   #
    #-------------------------------------------------------------------------------------------------------#
    
    #------------------------------------ RESET THE PROGRAM ------------------------------------------------#
    """" RESET ALL THE GLOBAL VARIABLES AND CALL THE MAIN WINDOW PROGRAM AGAIN """
    def reset():
        # RESET GLOBAL VARIABLES
        global item_selected_abc
        global item_selected_museum
        global item_selected_tvguide
        global list_selected_abc
        global list_selected_museum
        global list_selected_tvguide
        global total_selected

        item_selected_abc = 0
        item_selected_museum = 0
        item_selected_tvguide = 0
        total_selected = 0

        list_selected_abc = [0,0,0,0,0,0]
        list_selected_museum = [0,0,0,0,0,0]
        list_selected_tvguide = [0,0,0,0,0,0]
        
        """  SET THE BUTTONS ABC, MUSEUM AND TVGUIDE AS NORMAL IN THE MAIN WINDOW """
        abc_button.config(state=(['normal']))
        museum_button.config(state=(['normal']))
        tvguide_button.config(state=(['normal']))
        """ -----------------------------------------------------------------------"""

        # RESET TOP LEVEL WINDOWS AND THE STATUS LABEL IN THE MAIN SCREEN
        status_screen()
        main_window.destroy()
        root_window()

    
    # --------------------------------- DEFINE THE NUMBER OF ITEMS SELECTED ------------------------------#

    # SHOW IN THE MAIN WINDOW THE LIST EVENT SAVED      
    def save_list():    
        global total_selected
        if total_selected>1:
            label_print_status['text']= "( "+str(total_selected)+" ) Events Saved!"
        else:
            label_print_status['text']= "( "+str(total_selected)+" ) Event Saved!"

    # SHOW IN THE MAIN WINDOW THE LIST EVENT SAVED
    def status_screen():    
        global total_selected
        total_selected = item_selected_abc + item_selected_museum + item_selected_tvguide
        if total_selected>1:
            label_print_status['text']= "( "+str(total_selected)+" ) Events Selected!"
        else:
            label_print_status['text']= "( "+str(total_selected)+" ) Event Selected!"

    def internet_connection():
        label_print_status['text']= "No internet - Offline Mode!"
   
            
    #######################################  CREATE THE HTML FILE   ###################################
    def print_list():
        
        # SHOW IN THE MAIN WINDOW THE LIST EVENT PRINTED
        global total_selected
        if total_selected>1:
            label_print_status['text']= "( "+str(total_selected)+" ) Events Printed!"
        else:
            label_print_status['text']= "( "+str(total_selected)+" ) Event Printed!"

            
        ### TEMPLATE TO CREATE THE HTML FILE

        time = asctime()

        html_template_part_1 = '''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 10px;
          text-align: left;    
        }
        </style>
        </head>
        <body>


         <tr>
            <th ><img src="http://www.blogingmantra.com/wp-content/uploads/2018/07/ent.blog_.cochairs.jpg"
            alt="No image found" style="width:750px;height:250px
        "></th>

        <h2>ENTERTAINMENT LIST</h2>
        <p></p>
        <p> List generated on: ***TIME***</p>

        '''

        html_template_part_2 ='''
        <table>
          <tr>
            <th rowspan="2" width="250"><img src="***URL***" alt="No image found" style="width:250px;height:150px
        "></th>
            <td width="460">***DATE***</td>
          </tr>
          <tr>
            <td width="460">***TITLE***</td>
          </tr>
        </table>
        <p></p>
        '''


        html_template_part_3 ='''
        <p><a href="https://www.abc.net.au/radionational/programs/theminefield/">www.abc.net.au</a></p>
        <p><a href="https://www.oldmuseum.org/">www.oldmuseum.org</a></p>
        <p><a href="https://www.tvguide.com/tv-premiere-dates/">www.tvguide.com</a></p>
        </body>
        </html>

        '''
        # ---------------------------------- DEFINE ITEMS SELECTED TO BE PRINTED -----------------------------#
        
        # VARIABLES  (SHOW THE AMOUNT O ITEMS SELECTED)
        total_selected = item_selected_abc + item_selected_museum + item_selected_tvguide
        
        # CREATE A LIST WITH ALL ITEMS SELECTED BY THE USER      
        # LIST OF EVENT'S IMAGES URL
        final_list_image=[]
        for index in range(6):
            if list_selected_abc[index]==1:
                final_list_image.append(abc_image[index])
            if list_selected_museum[index]==1:
                final_list_image.append(museum_image[index])
            if list_selected_tvguide[index]==1:
                final_list_image.append(tvguide_image[index])        
        # LIST OF EVENT'S DATES
        final_list_date=[]
        for index in range(6):
            if list_selected_abc[index]==1:
                final_list_date.append(abc_dates[index])
            if list_selected_museum[index]==1:
                final_list_date.append(museum_dates[index])
            if list_selected_tvguide[index]==1:
                final_list_date.append(tvguide_dates[index])
        # LIST OF EVENT'S TITLEs
        final_list_title=[]
        for index in range(6):
            if list_selected_abc[index]==1:
                final_list_title.append(abc_title[index])
            if list_selected_museum[index]==1:
                final_list_title.append(museum_title[index])
            if list_selected_tvguide[index]==1:
                final_list_title.append(tvguide_title[index])

        ### COMPLETE LIST TO BE PRINTED IN HTML FILE (planner.html)            
        date  = final_list_date
        title = final_list_title
        image = final_list_image

        
        final_html='''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 10px;
          text-align: left;    
        }
        </style>
        </head>
        <body>
         <tr>
            <th ><img src="http://www.blogingmantra.com/wp-content/uploads/2018/07/ent.blog_.cochairs.jpg"
            alt="No image found" style="width:750px;height:250px
        "></th>

        <h2>NO EVENT SELECTED </h2>
        <p></p>
        <p> List generated on: ***TIME***</p>

        </body>
        </html>

        '''
        final_html = final_html.replace('***TIME***', time)

        for index in range(len(date)):
            
            final_html = html_template_part_1
            final_html = final_html.replace('***TIME***', time)
            for item in range (len(date)):
                #print("teste"+str(item))
                final_html = final_html + html_template_part_2
                final_html = final_html.replace('***URL***',image[item])
                final_html = final_html.replace('***DATE***',date[item])
                final_html = final_html.replace('***TITLE***',title[item])

            final_html = final_html + html_template_part_3

        ### Write the HTML code to a Unicode text file
        html_file = open( 'planner.html', 'w', encoding = 'UTF-8')
        html_file.write(final_html)
        html_file.close()

    #################################################################################################################        
    ##                                               DATABASE                                                      ##
    ################################################################################################################# 

    # FUNCTION TO SAVE ITEMS SELECTED IN A DATABASE
    def sql_save_function():
        connection = connect('entertainment_planner.db')
        view = connection.cursor()
    
        save_list()
            
        # CREATE A LIST WITH ALL ITEMS SELECTED BY THE USER           
        # LIST OF EVENT'S DATES
        
        final_list_date=[]
        for index in range(6):
            if list_selected_abc[index]==1:
                final_list_date.append(abc_dates[index])
            if list_selected_museum[index]==1:
                final_list_date.append(museum_dates[index])
            if list_selected_tvguide[index]==1:
                final_list_date.append(tvguide_dates[index])
        # LIST OF EVENT'S TITLEs
        final_list_title=[]
        for index in range(6):
            if list_selected_abc[index]==1:
                final_list_title.append(abc_title[index])
            if list_selected_museum[index]==1:
                final_list_title.append(museum_title[index])
            if list_selected_tvguide[index]==1:
                final_list_title.append(tvguide_title[index])

        ### COMPLETE LIST TO BE PRINTED IN HTML FILE (planner.html)            
        list_date  = final_list_date
        list_name = final_list_title  

        # FUNCTION TO DELETE, INSERT, AND PRINT INFORMATION FROM THE DATABASE
        def delete():
            view.execute("DELETE FROM events")
            connection.commit()
            print('Number of rows deleted: ', view.rowcount)

        def insert():
            count = 0
            for index in range(len(list_date)):
                name = list_name[index]
                date = list_date[index]
                view.execute("INSERT INTO events(event_name, event_date) VALUES (?,?)",
                             (name, date))
                connection.commit()
                count = count + 1
            print('Number of rows inserted: ' + str(count)) # , view.rowcount)
        def select():
            data = list(view.execute("SELECT * FROM events ")) 
            for index in data:
                print(index)
            
        delete()
        insert()    
        select()

        view.close()
        connection.close()

    #-----------------------------------------------------------------------------------------------------------#


    #############################################################################################################
    #                                         MAIN WINDOW INTERFACE                                             #
    #############################################################################################################
    # -------------------- VARIABLES USED BY THE MAIN WINDOW 
    global main_window
    global abc_button
    global museum_button
    global tvguide_button
    
    main_window = Tk()
    main_window.title('MEDIA AND ENTERTAINMENT') 
    #main_window.geometry('500x700') 
    main_window.resizable(width=False, height=False)
    main_window_color = 'light blue'
    main_window['bg']= main_window_color


    # -------------------- VARIABLES USED BY MAIN WINDOW COMPONENTS 

    ###------------------- MAIN WINDOW FONT DEFINITION
    font_buttons = 'Arial'
    font_size_buttons = 20
    activeforeground_color = 'white'
    button_bg_color = 'light grey'
    button_fg_color = 'dark blue'
    buttons_width = 26

    ###------------------- FRAME_MW PARAMETERS
    frame_width = 450
    frame_height = 300
    frame_font_size = 20
    frame_font = 'Arial'

    ###------------------- FRAME PARAMETERS

    frame_mw = LabelFrame(main_window, text = 'CATEGORIES',relief = RIDGE,
                          bg = main_window_color,
                          fg = 'white',
                          width = frame_width , height = frame_height,
                          font = (frame_font,frame_font_size),
                          borderwidth=4) 

    ###------------------- LABELS PARAMETERS
    photo = PhotoImage(file = 'entertaiment.png') # Image used in the main window

    # LABEL 1
    label_photo = Label(main_window, image = photo, borderwidth=0)

    ###------------------- BUTTONS PARAMETERS
    # 1 - BUTTON MUSEUM
    museum_button = Button(frame_mw, text= 'OLD MUSEUM',
                          font = (font_buttons,font_size_buttons),
                          bg = button_bg_color ,
                          fg = button_fg_color,
                          activeforeground = activeforeground_color,
                          width = buttons_width,
                          command = window_museum) 
    # 2 - BUTTON ABC
    abc_button = Button(frame_mw, text= 'ABC RADIO',
                        font = (font_buttons,font_size_buttons),
                        bg = button_bg_color,
                        fg = button_fg_color,
                        activeforeground = activeforeground_color,
                        width = buttons_width,
                        command = window_abc) 
    # 3 - BUTTON TVGUIDE
    tvguide_button = Button(frame_mw, text= 'TV GUIDE',
                          font = (font_buttons,font_size_buttons),
                          bg = button_bg_color,
                          fg = button_fg_color,
                          activeforeground = activeforeground_color,
                          width = buttons_width,
                          command = window_tvguide)
    
    # 4 - LABEL STATUS SCREEN
    label_print_status = Label(main_window, text = '( 0 ) Event Selected)',
                               bg = main_window_color,
                               fg = "white",
                               width ="26", 
                               font = (font_buttons,font_size_buttons),
                               borderwidth=0)
    # 5 - FRAME 2
    frame_mw_2 = LabelFrame(main_window, text = '',relief = RIDGE,
                          bg = main_window_color,
                          fg = 'white',
                          width = frame_width , height = "3",
                          font = (frame_font,frame_font_size),
                          borderwidth=0) 
    
    # 6 - BUTTON PRINT
    print_button = Button(frame_mw_2, text= 'PRINT',
                          font = (font_buttons,font_size_buttons),
                          bg = button_bg_color,
                          fg = button_fg_color,
                          activeforeground = activeforeground_color,
                          width = int((buttons_width//2)-1),
                          command = print_list )
    # 7 - BUTTON SAVE IN SQL
    save_button = Button(frame_mw_2, text= 'SAVE',
                          font = (font_buttons,font_size_buttons),
                          bg = button_bg_color,
                          fg = button_fg_color,
                          activeforeground = activeforeground_color,
                          width = int((buttons_width//2)-1),
                          command = sql_save_function)
    # 8 - BUTTON RESET
    reset_button = Button(main_window, text= 'RESET PROGRAM',
                          font = (font_buttons,font_size_buttons),
                          bg = button_bg_color,
                          fg = button_fg_color,
                          activeforeground = activeforeground_color,
                          width = buttons_width,
                          command=reset)
    # 9 - CHECKBUTTON WORK OFFLINE
    offline_checkbox_var = IntVar() # Variables
    
    offline_checkbox = Checkbutton(main_window, text='Option: Work Offfline         ',
                          fg = 'grey',
                          bg = main_window_color,
                          activebackground = main_window_color,
                          variable = offline_checkbox_var,
                          font = (font_checkbox,font_size_checkbox)) 
    
    ###------------------- WIDGETS LAYOUT 
    label_photo.pack(padx=0, pady=0)

    frame_mw.pack(padx=0, pady=10)
    museum_button.pack(padx=10, pady=10) 
    abc_button.pack(padx=10, pady=10)
    tvguide_button.pack(padx=10, pady=10)
    label_print_status.pack(padx=10, pady=2)

    frame_mw_2.pack(padx=0, pady=10)
    print_button.grid(row = 0, column = 0, padx=8, pady=10)
    save_button.grid(row = 0 , column = 1 ,padx=8, pady=10)

    reset_button.pack(padx=0, pady=10)
    offline_checkbox.pack(padx=10, pady=10, anchor='s')
    
    main_window.mainloop()  

##  START THE APLICATION
root_window()


