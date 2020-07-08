This is the readme file for the scraper as requested. I also want to say that as a developer i was taught to google things or find answers to your problems if neccessary, i used google to search for some of the problems that i had during the making of scraper, because i just cant remember all the functions that a package or module offers like BEAUTIFULSOUP. so i had to google according to my problems.

REQUIREMENTS:

Selenium Chrome Driver According to the version of chrome installed i had v83 , i included the driver file in repo as well. otherwise v84 is available if its latest now.

Please Use CLI Accordingly Please Enter Driving License Number (--dlno) , Date Of Birth (--dob) example : $python scraper.py --dlno DL-0420110149646 --dob 09-02-1976

Official Site Also has too many bugs as most of the government websites do , for the tast url "https://parivahan.gov.in/rcdlstatus/?pur_cd=101" sometimes clicks doesnt register on server side , hence the page fails to process and gets stuck at same place, its the bug of the website and workaround is to close the browser and launch script again. i tried everything to minimize the errors but the official webpage errors i cant handle because its their server side problem.