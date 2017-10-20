### If learning wrong, re-run the program. Thanks! 
import tkinter as tk
from Emailaddress import Email
from neuralNetwork import NeuralNetwork
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import style
style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
import numpy
import smtplib
import time
email = Email()
neural_network = NeuralNetwork()
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Welcome, MainPage,MainPage2):

            frame = F(container, self)
            self.frames[F] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Welcome)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Welcome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, font= (None,30),text="Welcome to Cyclone Detection System", fg='blue')
        label1.pack(pady=10,padx=10)
        label2 = tk.Label(self,font=(None,25), text="Please Input Your Email Address: ", fg="brown")
        label2.place(x = 140, y = 200)

        self.emailEntry = tk.Entry(self,font=(None, 25))
        self.emailEntry.place(x= 140, y =250)
        button1 = tk.Button(self, font=(None, 25),text="Start!", command=lambda: controller.show_frame(MainPage))
        button2 = tk.Button(self, font=(None, 25),text="Exit", command=self.quit)
        button3 = tk.Button(self, font=(None, 25), text="Register", command=self.register)
        button3.place(x=140, y = 300 )
        button1.place(x= 620, y= 200)
        button2.place(x= 620, y= 300)

    def register(self):
        email.setEmailAddress(self.emailEntry.get())

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        label3 = tk.Label(self, text="Run Time: ")
        label3.pack(pady=4,padx=10)
        button4 = tk.Button(self, text="Next",  command=lambda: controller.show_frame(MainPage2))

        self.run_time = tk.Entry(self)
        self.run_time.pack(side="top")

        runButton = tk.Button(self, text="RUN", command=self.drawGraph)
        runButton.pack(side = "top")
        button4.pack()
        label1 = tk.Label(self, font=(None, 25),fg="red", text="Error rate:")
        label1.place(x=20, y=100)
        self.widget = None

        self.backbutton = tk.Button(self, text="Back", font=(None, 20), command=lambda: controller.show_frame(Welcome))
        self.backbutton.pack(side="top")
        self.TimeLabel = tk.Label(self, font=(None, 20), )
        self.TimeLabel.place(x=600, y=50)
    def drawGraph(self):

        train = []
        error = []
        times = int(self.run_time.get())
        with open('data.csv','rt') as f:

            reader = csv.reader(f, delimiter=',')
            count = 0
            for row in reader:
                if count > 0:
                    tmp = []
                    tmp.append(float(row[1]) / 10)
                    tmp.append(float(row[2]) / 10)
                    tmp.append(float(row[3]))
                    train.append(tmp)
                count += 1

        startTime = time.time()
        for i in range(times):
            ri = numpy.random.randint(len(train))
            point = train[ri]
            neural_network.setWindSpeed(float(point[0]))
            neural_network.setTemperature(float(point[1]))
            neural_network.setOccur(point[2])
            neural_network.learning_weight1()
            neural_network.learning_weight2()
            neural_network.learning_constant()
            error.append(neural_network.Calculateerror())


        endtime = time.time()
        self.TimeLabel.config(text="Time:" + str(endtime - startTime) + " seconds")

        if self.widget:
            self.widget.destroy()

        f = Figure(figsize=(5, 5), dpi=100)
        f.clf()
        a = f.add_subplot(111)
        a.hist(error)
        canvas = FigureCanvasTkAgg(f, self)
        f.canvas.draw()
        self.widget = canvas.get_tk_widget()
        self.widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class MainPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.resultNameLabel = tk.Label(self, font=(None, 20),fg="blue",text="Result: ")
        self.resultNameLabel.place(x=20, y=250)
        windLabel= tk.Label(self,font=(None,20),fg="brown",text ="Wind Speed: ")
        windLabel.place(x=20,y= 20)
        self.windEntry = tk.Entry(self,font=(None,20))
        self.windEntry.place(x=20, y=70)
        tempertureLabel = tk.Label(self,font=(None,20),fg="darkgreen",text="Temperture: ")
        tempertureLabel.place(x =20, y=140)
        self.temperatureEntry = tk.Entry(self,font=(None,20))
        self.temperatureEntry.place(x=20,y=190)
        InputButton = tk.Button(self, text="Input", font=(None,20),command=self.getProbability)
        InputButton.place(x=400,y= 100)
        EmailButton = tk.Button(self,text="SendEmail",font=(None,20),command=self.SendEmail)
        EmailButton.place(x=500,y= 100)
        ExitButton = tk.Button(self, text="Exit", font=(None,20),command=self.quit)
        ExitButton.place(x=650,y= 100)

        self.resultLabel = tk.Label(self,font=(None,20),)
        self.resultLabel.place(x=20,y= 300)

        self.backbutton = tk.Button(self, text="Back", font=(None, 20), command=lambda: controller.show_frame(MainPage))
        self.backbutton.place(x=750, y=100)
    def getProbability(self):
        windSpeed = float(self.windEntry.get())/10
        temperature = float(self.temperatureEntry.get())/10
        neural_network.setWindSpeed(windSpeed)
        neural_network.setTemperature(temperature)
        result = neural_network.sigmoid()


        if result < 0.001:
            result=0
            self.resultLabel.config(text="The probability of cyclone occurrence: " + str(result) + '%'+'\n'+"Happy! No typhoon!")

            return result
        elif result*100 <= 50 and result*100>0.1:
            result *= 100
            self.resultLabel.config(text="The probability of cyclone occurrence: " + str(result) + '%' + '\n'
                                         + "Don't worry about typhoon! Happy!")

            return result
        elif result*100 > 50 and result*100 <= 80 :
            result*=100
            self.resultLabel.config(text="The probability of cyclone occurrence: " + str(result) + '%'+'\n'
                                         +"Prepare some clothes!")

            return result
        elif result*100 > 80:
            result *= 100
            self.resultLabel.config(text="The probability of cyclone occurrence: " + str(result) + '%' + '\n'
                                         + "Stay at home if you don't have to go out")

            return result

    def SendEmail(self):
        result1= self.getProbability()
        message =""
        if result1 < 0.1:
            message = "Hello! The probability of cyclone is " + str(result1)+ "%" +'\n'+"Happy! No typhoon!"
        elif result1 <= 50 and result1>=0.1:
            message = "Hello! The probability of cyclone is " + str(result1) + "%" + '\n'+ "Don't worry about typhoon! Happy!"

        elif result1 > 50 and result1 <= 80 :
            message = "Hello! The probability of cyclone is " + str(result1) + "%" + '\n' + "Prepare some clothes!"

        elif result1 > 80:
            message = "Hello! The probability of cyclone is " + str(result1) + "%" + '\n' +"Stay at home if you don't have to go out"

        fromEmailAddress = "workjhua182@gmail.com"
        toEmailAddress = str(email.getEmailAddress())
        password = 'jhua182JHUA'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(fromEmailAddress, password)
        server.sendmail(fromEmailAddress, toEmailAddress, message)
        server.quit()

if __name__ == "__main__":
    app = App()
    app.geometry("1000x500")
    while True:
        try:
            app.mainloop()
            break
        except UnicodeDecodeError:
            pass