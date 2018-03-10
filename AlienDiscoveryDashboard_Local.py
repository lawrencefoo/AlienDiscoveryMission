import os
import subprocess
from gtts import gTTS

import uuid
from flask import Flask
import time
import redis
from flask import Flask, render_template, redirect, request, url_for, make_response

import urllib2
import json
import boto


# Connection to Redis Database to get data from AlienDiscovery Bot
r = redis.Redis(host='redis-18803.c11.us-east-1-2.ec2.cloud.redislabs.com', port='18803', password='#############')


app = Flask(__name__)
my_uuid = str(uuid.uuid1())

#set colours
BLUE = "#777799"
GREEN = "#99CC99"
COLOR = BLUE

begin_html = """
<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Start To Detect Alien Discovery Adventure</title>

    <!-- Bootstrap core CSS -->
    <link href="static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="static/css/scrolling-nav.css" rel="stylesheet">

    <script type="text/JavaScript">
    <!--
    function TimedRefresh( t ) {
    setTimeout("location.reload(true);", t);
    }
    //   -->
    </script>

  </head>"""
    

end_html = """


    <section id="about">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <h2>About this page</h2>
            <p class="lead">This Alien Discovery Dashboard is to monitor any incoming signal from "Alien Discovery Bot". This Bot features:</p>
            <ul>
              <li>DellEMC Project on PCF with IQT (IOT with Intelligent)</li>
              <li>Alien Discovery Bot has various "advance" sensors to detect incoming Alien Object or Solar Flash</li>
              <li>Alien Discovery Bot will alert and try to communicate with the new encounter (LED and Buzzer)</li>
              <li>Bot will display the proximity of the distance on the incoming Alien Encounter</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section id="services" class="bg-light">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <h2>Services we offer</h2>
            <p class="lead">Advance Technology with End-to-End solutions which to meet your outcomes and missions</p>
          </div>
        </div>
      </div>
    </section>

    <section id="contact">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <h2>Contact us</h2>
            <p class="lead">DellEMC Singapore. Lawrence Foo (Email: Lawrence.Foo@dell.com) (+65 97598865)</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-5 bg-dark">
      <div class="container">
        <p class="m-0 text-center text-white">Copyright &copy; Your Website 2017</p>
      </div>
      <!-- /.container -->
    </footer>

    <!-- Bootstrap core JavaScript -->
    <script src="static/vendor/jquery/jquery.min.js"></script>
    <script src="static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Plugin JavaScript -->
    <script src="static/vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom JavaScript for this theme -->
    <script src="static/js/scrolling-nav.js"></script>

  </body>

</html>
"""



@app.route('/')
def mainmenu():

    fileLinksDescrip = open('static/linksdescriptions.txt')
    linkdescription_list = fileLinksDescrip.readlines()
    fileLinksDescrip.close()
    print linkdescription_list[0]
    print linkdescription_list[1]
    print linkdescription_list[2]

    mid1_html =  """
    <body id="page-top">
    <header class="bg-primary text-white">
      <div class="container text-center">
        <h1>Dell EMC</h1>
        <h2>Welcome to Alien Discovery Dashboard</h2>
        <p class="lead">This Dashboard is to monitor Alien Discovery Bot (in the outer space) via Ultrasonic Distance Sensor and Photoresistor</p>
      </div>
        """
    mid1_html += """<div class="col-lg-6 mx-auto">"""
    mid1_html += """<h3><font color="white">Distance Away from New Encounter (Alien): </font><font color="red">""" + r.get('AlienDistance') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Detecting Alien Solar Flare on Discovery Bot     : </font><font color="red">""" + r.get('AlienSolar') + """</font></h3>"""
    mid1_html += """<h3><font color="white">LED on Discovery Bot to communicate with Alien : </font><font color="red">""" + r.get('AlienLED') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Buzzer on Discovery Bot to communicate with Alien : </font><font color="red">""" + r.get('AlienBuzzer') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Latest Date/Time Sent From Discovery Bot     : </font><font color="red">""" + r.get('AlienDateTime') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Number of Consecutive Encounters with Alien  : </font><font color="red">""" + r.get('AlienCounter') + """</font></h3>"""
    mid1_html += """<br>"""    
    mid1_html += """<h3>Click The Below Links:</h3>"""
#    mid1_html += """<h3><a href="autorefresh.html" style="color:rgb(0,255,0)">Auto Refresh Dashboard Page</a></h3>"""
#    mid1_html += """<h3><a href="wunderground.html" style="color:rgb(0,255,0)">Astronomy On Moon Data From Weather Underground</a></h3>"""
#    mid1_html += """<h3><a href="ecsphotos.html" style="color:rgb(0,255,0)">View Astronomy Photos In ECS</a></h3>"""
    mid1_html += """<h3><a href="autorefresh.html" style="color:rgb(0,255,0)">""" + linkdescription_list[0] + """</a></h3>"""
    mid1_html += """<h3><a href="wunderground.html" style="color:rgb(0,255,0)">""" + linkdescription_list[1] + """</a></h3>"""
    mid1_html += """<h3><a href="ecsphotos.html" style="color:rgb(0,255,0)">""" + linkdescription_list[2] + """</a></h3>"""
        
    mid1_html +=  """
      </div>
    </header>
    """

    mid2_html =  """
            <!-- Navigation -->
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
              <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top">Alien Discovery Dashboard</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#services">Services</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#contact">Contact</a>
                    </li>
                  </ul>
                </di
              </div>
            </nav>"""
    
    response = begin_html + mid1_html + mid2_html + end_html

    return response

@app.route('/autorefresh.html')
def autorefresh():


#    tts = gTTS(text='Alien Encounter', lang='en')
#    tts.save("alienencounter.mp3")
    intAlienCounter = r.get('AlienCounter')
    print "Alien Counter : " + intAlienCounter
    if int(intAlienCounter) >= 3:
        print "Sound Alarm"
        for i in range(1,4):
            subprocess.call(["C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe","--play-and-exit","C:\\Users\\fool\\Documents\\Work\\Technical\\EMC\\Trainings\\Piped_Piper\\Project\\alienencounter.mp3"])
            time.sleep(0.5)

    mid1_html =  """
    <body id="page-top" onload="JavaScript:TimedRefresh(1000);">
    <header class="bg-primary text-white">
      <div class="container text-center">
        <h1>Dell EMC</h1>
        <h2>Welcome to Alien Discovery Dashboard</h2>
        <p class="lead">This Dashboard is to monitor Alien Discovery Bot (in the outer space) via Ultrasonic Distance Sensor and Photoresistor</p>
      </div>
        """
    mid1_html += """<div class="col-lg-6 mx-auto">"""
    mid1_html += """<h3><font color="white">Distance Away from New Encounter (Alien): </font><font color="red">""" + r.get('AlienDistance') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Detecting Alien Solar Flare on Discovery Bot     : </font><font color="red">""" + r.get('AlienSolar') + """</font></h3>"""
    mid1_html += """<h3><font color="white">LED on Discovery Bot to communicate with Alien : </font><font color="red">""" + r.get('AlienLED') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Buzzer on Discovery Bot to communicate with Alien : </font><font color="red">""" + r.get('AlienBuzzer') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Latest Date/Time Sent From Discovery Bot     : </font><font color="red">""" + r.get('AlienDateTime') + """</font></h3>"""
    mid1_html += """<h3><font color="white">Number of Consecutive Encounters with Alien  : </font><font color="red">""" + r.get('AlienCounter') + """</font></h3>"""
    mid1_html += """<br>"""    
    mid1_html += """<h3>Click The Below Links:</h3>"""
    mid1_html += """<h3><a href=/ style="color:rgb(0,255,0)">Back To Main Page Menu</a></h3>"""
    mid1_html += """
      </div>
    </header>
    """

    mid2_html =  """
            <!-- Navigation -->
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
              <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top">Alien Discovery Dashboard</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#services">Services</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#contact">Contact</a>
                    </li>
                  </ul>
                </di
              </div>
            </nav>"""
    
    response = begin_html + mid1_html + mid2_html + end_html

    return response

@app.route('/wunderground.html')
def wunderground():

    f = urllib2.urlopen('http://api.wunderground.com/api/###################/astronomy/q/Singapore/Singapore.json')

    json_string = f.read()
    parsed_json = json.loads(json_string)
    strMoonPhase = parsed_json['moon_phase']['phaseofMoon']
    strPercentIluminated = parsed_json['moon_phase']['percentIlluminated']
    strCurrentTimeHour = parsed_json['moon_phase']['current_time']['hour']
    strCurrentTimeMin = parsed_json['moon_phase']['current_time']['minute']
    strSunRiseTimeHour = parsed_json['moon_phase']['sunrise']['hour']
    strSunRiseTimeMin = parsed_json['moon_phase']['sunrise']['minute']
    #temp_f = parsed_json['current_observation']['temp_f']
    print "Current Moon Phase in %s is: %s" % (strMoonPhase, strPercentIluminated)

    mid1_html =  """
    <body id="page-top">
    <header class="bg-primary text-white">
      <div class="container text-center">
        <h1>Dell EMC</h1>
        <h2>Welcome to Alien Discovery Dashboard</h2>
        <p class="lead">This Dashboard is to monitor Alien Discovery Bot (in the outer space) via Ultrasonic Distance Sensor and Photoresistor</p>
      </div>
        """
    mid1_html += """<div class="col-lg-6 mx-auto">"""
    mid1_html += """<h3><font color="white">Moon Of The Phase In Singapore: </font><font color="red">""" + strMoonPhase + """</font></h3>"""
    mid1_html += """<h3><font color="white">Percentage Of The Moon Iluminated in SG : </font><font color="red">""" + strPercentIluminated + """</font></h3>"""
    mid1_html += """<h3><font color="white">Current Hour Of The Moon Iluminated in SG : </font><font color="red">""" + strCurrentTimeHour + """</font></h3>"""
    mid1_html += """<h3><font color="white">Current Minute Of The Moon Iluminated in SG : </font><font color="red">""" + strCurrentTimeMin + """</font></h3>"""
    mid1_html += """<h3><font color="white">Next Hour Of The Sunrise in SG : </font><font color="red">""" + strSunRiseTimeHour + """</font></h3>"""
    mid1_html += """<h3><font color="white">Next Minute Of The Sunrise in SG : </font><font color="red">""" + strSunRiseTimeMin + """</font></h3>"""
    mid1_html += """<br>"""    
    mid1_html += """<h3>Click The Below Links:</h3>"""
    mid1_html += """<h3><a href=/ style="color:rgb(0,255,0)">Back To Main Page Menu</a></h3>"""
    mid1_html += """
      </div>
    </header>
    """


    
    mid2_html =  """
            <!-- Navigation -->
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
              <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top">Alien Discovery Dashboard</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#services">Services</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#contact">Contact</a>
                    </li>
                  </ul>
                </di
              </div>
            </nav>"""
    
    response = begin_html + mid1_html + mid2_html + end_html
    f.close()

    return response

@app.route('/ecsphotos.html')
def ecsphotos():

    ### Retrieve Moon Photo from ECS
    ecs_access_key_id = '##############@ecstestdrive.emc.com'  
    ecs_secret_key = '##########################'

    #### This is the ECS syntax. It requires "host" parameter
    session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='object.ecstestdrive.com')  
    bname = 'aliendiscovery'

    #### Get bucket and display details
    b = session.get_bucket(bname)
    print "ECS connection is: " + str(session)
    print "Bucket is: " + str(b)

    photoshtml = ""
    for k in b.list():
        photoecs = "http://###############.public.ecstestdrive.com/" +bname +"/" + k.key
        print photoecs
        photoshtml = photoshtml + """<img src="http://##############.public.ecstestdrive.com/{}/{}"><br>""".format(bname, k.key)
        print photoshtml


    mid1_html =  """
    <body id="page-top">
    <header class="bg-primary text-white">
      <div class="container text-center">
        <h1>Dell EMC</h1>
        <h2>Welcome to Alien Discovery Dashboard</h2>
        <p class="lead">This Dashboard is to monitor Alien Discovery Bot (in the outer space) via Ultrasonic Distance Sensor and Photoresistor</p>
      </div>
        """
    mid1_html += """<div class="col-lg-6 mx-auto">"""
    mid1_html += """<br>"""    
    mid1_html += """<h3>Click The Below Links:</h3>"""
    mid1_html += """<h3><a href=/ style="color:rgb(0,255,0)">Back To Main Page Menu</a></h3>"""
    mid1_html += """<br>"""    
    mid1_html += """<h3>Astronomy Photos From ECS:</h3>"""
    mid1_html += """<h3>""" + photoshtml + """</h3>"""
    mid1_html += """
      </div>
    </header>
    """


    
    mid2_html =  """
            <!-- Navigation -->
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
              <div class="container">
                <a class="navbar-brand js-scroll-trigger" href="#page-top">Alien Discovery Dashboard</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#services">Services</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link js-scroll-trigger" href="#contact">Contact</a>
                    </li>
                  </ul>
                </di
              </div>
            </nav>"""
    
    response = begin_html + mid1_html + mid2_html + end_html

    return response


if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
