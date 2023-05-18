"""Real time plotting of Microphone level using kivy
"""

'''[hex(x) for x in frames[0]]. If you want to get the actual 2-byte numbers use the format string '<H' with the struct module.
https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio
'''


from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
#from kivy.garden.graph import MeshLinePlot
from kivy_garden.graph import MeshLinePlot
#from kivy_garden.graph import Graph, LinePlot
from kivy.clock import Clock
from threading import Thread
#import audioop
#import pyaudio
from audiostream import get_output, AudioSample, get_input_sources, get_input
from android.permissions import request_permissions,Permission,check_permission



def get_microphone_level(self):
    """
    source: http://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino
    audioop.max alternative to audioop.rms
    
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    s = p.open(format=FORMAT,
               channels=CHANNELS,
               rate=RATE,
               input=True,
               frames_per_buffer=chunk)
    global levels
    while True:
        data = s.read(chunk)
        mx = audioop.rms(data, 2)
        if len(levels) >= 100:
            levels = []
        levels.append(mx)
    """
    self.levels = []  # store levels of microphone
 
    self.samples_per_second = 60 # variables which stores the number of audio samples recorded per second
    #self.audioData = [] # creates a list to store the audio bytes recorded
    self.mic = get_input(callback=self.micCallback, rate=8000, source='default', buffersize=2048) # initialises the method get_input 
    print("self.mic = get_input")
    self.mic.start() # starts the method 'self.mic' recording audio data
    Clock.schedule_interval(self.readChunk, 1 / self.samples_per_second) # calls the method 'self.readChunk' to read and store each audio buffer (2048 samples)  
        
        
      
    def micCallback(self, buffer):
        print("def micCallback")
        # method which is called by the method 'get_input' to store recorded audio data (each buffer of audio samples)        
        #self.audioData.append(buffer) # appends each buffer (chunk of audio data) to variable 'self.audioData'
        #print('size of frames: ' + str(len(self.audioData)))
        self.levels.append(buffer) 
        
        print('size of frames: ' + str(len(buffer)))
        #print ('got : ' + str(len(buf)))

    #def start(self):
        # method which begins the process of recording the audio data
        #self.mic.start() # starts the method 'self.mic' recording audio data
        #Clock.schedule_interval(self.readChunk, 1 / self.samples_per_second) # calls the method 'self.readChunk' to read and store each audio buffer (2048 samples) 60 


    def readChunk(self, sampleRate):
        print("def readChunk")
        # method which coordinates the reading and storing of the bytes from each buffer of audio data (which is a chunk of 2048 samples)
        self.mic.poll()  # calls 'get_input(callback=self.mic_....)' to read content. This byte content is then dispatched to the callback method 'self.micCallback'        
        
    
  
    
    

class Logic(BoxLayout):
    def __init__(self,):
        super(Logic, self).__init__()
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])

    def start(self):
        self.ids.graph.add_plot(self.plot)
        Clock.schedule_interval(self.get_value, 0.001)

    def stop(self):
        Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plot.points = [(i, j/5) for i, j in enumerate(levels)]


class RealTimeMicrophone(App):
    def build(self):
        request_permissions([Permission.INTERNET, Permission.RECORD_AUDIO])
        return Builder.load_file("look.kv")




    
    
get_level_thread = Thread(target = get_microphone_level)
get_level_thread.daemon = True
get_level_thread.start()
RealTimeMicrophone().run()
    
