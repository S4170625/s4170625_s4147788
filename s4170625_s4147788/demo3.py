import pyhtml
import student_a_level_1
import student_a_level_2
import student_a_level_3

import student_b_level_1
import student_b_level_2
import student_b_level_3

pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"]      =student_a_level_1; #Page to show when someone accesses "http://localhost/"
pyhtml.MyRequestHandler.pages["/page2a"]=student_a_level_2; #Page to show when someone accesses "http://localhost/page2a"
pyhtml.MyRequestHandler.pages["/page3a"]=student_a_level_3; #Page to show when someone accesses "http://localhost/page3a"
pyhtml.MyRequestHandler.pages["/page1b"]=student_b_level_1; #Page to show when someone accesses "http://localhost/page1b"
pyhtml.MyRequestHandler.pages["/page2b"]=student_b_level_2; #Page to show when someone accesses "http://localhost/page2b"
pyhtml.MyRequestHandler.pages["/page3b"]=student_b_level_3; #Page to show when someone accesses "http://localhost/page3b"

#Host the site!
pyhtml.host_site()