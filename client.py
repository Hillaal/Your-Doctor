import socket as sock
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import os
from os import path
import pickle
from _thread import *

vitals={'Heart Rate':"70 pbm",'Temp':"36.5",'Blood Pressure':"150/70"}

target_host="127.0.0.1"
target_port=5555
THIS_FOLDER= path.dirname(path.abspath(__file__))
DIAGNOSE_CLASS,_=loadUiType(path.join(THIS_FOLDER, "diagnose.ui"))
MAIN_CLASS,_=loadUiType(path.join(THIS_FOLDER, "main.ui"))
CHAT_CLASS,_=loadUiType(path.join(THIS_FOLDER, "chat.ui"))


class Main(QtWidgets.QMainWindow,MAIN_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.nameLabel.setText("Please Enter Your Name Then Press Enter")
        self.diagnose.hide()
        self.chat.hide()
        self.back.hide()
        self.setFixedSize(992, 688)
        self.back.clicked.connect(lambda:self.back_pushButton_clicked())
        self.name.returnPressed.connect(lambda: self.nameEntered())
        self.enterName.clicked.connect(lambda: self.nameEntered())
        self.diagnose.clicked.connect(lambda:self.diagnose_pushButton_clicked())
        self.chat.clicked.connect(lambda:self.chat_pushButton_clicked())

    def nameEntered(self):
        
        if not self.name.text():
            self.nameLabel.setText("No Name Entered, Please Enter Your Name Then Press Enter")
            self.nameLabel.adjustSize()
        else:
            global NAME
            NAME =self.name.text()
            self.nameLabel.setText("Hello {}, what do you want to do?".format(NAME))
            self.nameLabel.adjustSize()
            self.name.hide()
            self.enterName.hide()
            self.diagnose.show()
            self.chat.show()
            self.back.show()
    def diagnose_pushButton_clicked(self):
        Diagnose(self).show()
        self.close()

    def chat_pushButton_clicked(self):       
        Chat(self).show()
        self.close()

    def back_pushButton_clicked(self):
        self.name.show()
        self.nameLabel.setText("Please Enter Your Name Then Press Enter")
        self.enterName.show()
        self.diagnose.hide()
        self.nameLabel.show()
        self.chat.hide()
        self.back.hide()


class Diagnose(QtWidgets.QMainWindow,DIAGNOSE_CLASS):
    def __init__(self,parent=None):
        super(Diagnose,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        
        self.client=0
        self.payload=[]
        
        self.start()
        
    def handle_UI(self):
        self.setFixedSize(992, 752)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        self.fever.setEnabled(True)
        self.headache.setEnabled(True)
        self.diarrhea.setEnabled(True)
        # self.breathing_difficulty.setEnabled(True)
        self.vomiting.setEnabled(True)
        self.heartburn.setEnabled(True)
        self.sr.setEnabled(True)
        self.ab.setEnabled(True)
        #self.showDiagnose.setEnabled(False)

        #self.startbutton.clicked.connect(lambda :self.start())
        self.yes.clicked.connect(lambda :self.yesClicked())
        self.no.clicked.connect(lambda :self.noClicked())
        self.fever.clicked.connect(lambda :self.add("fever"))
        self.headache.clicked.connect(lambda :self.add("headache"))
        self.diarrhea.clicked.connect(lambda :self.add("diarrhea"))
        self.vomiting.clicked.connect(lambda :self.add("vomiting"))
        self.sneezing.clicked.connect(lambda :self.add("sneezing"))
        self.heartburn.clicked.connect(lambda :self.add("heartburn"))
        
        self.sr.clicked.connect(lambda :self.add("sneezing"))
        self.ab.clicked.connect(lambda :self.add("abdominal pain"))
        
        self.back.clicked.connect(lambda: self.backClicked())
        self.back.hide()
        #self.showDiagnose.clicked.connect(lambda :self.send())

    def start(self):
        try:
            client_socket=sock.socket(sock.AF_INET,sock.SOCK_STREAM)
        except sock.error as err:
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to create client</b></p>")
            self.browser.append("Reason:"+str(err))
            self.fever.setEnabled(False)
            self.headache.setEnabled(False)
            self.diarrhea.setEnabled(False)
            self.sneezing.setEnabled(False)
            self.vomiting.setEnabled(False)
            self.heartburn.setEnabled(False)
            self.sr.setEnabled(False)
            self.ab.setEnabled(False)
            self.yes.setEnabled(False)
            self.no.setEnabled(False)
        try:
            client_socket.connect((target_host,target_port))
            self.browser.append("<p style='color:#b03f3c'><b>Connected to server</b></p>")
            self.client=client_socket

        except sock.error as err:
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to connect to server</b></p>")
            self.browser.append("Reason:"+str(err))
            self.fever.setEnabled(False)
            self.headache.setEnabled(False)
            self.diarrhea.setEnabled(False)
            self.sneezing.setEnabled(False)
            self.vomiting.setEnabled(False)
            self.heartburn.setEnabled(False)
            self.sr.setEnabled(False)
            self.ab.setEnabled(False)
            self.yes.setEnabled(False)
            self.no.setEnabled(False)

        l=['d',NAME,list(vitals.values())]
        self.client=client_socket

        try:
            self.client.settimeout(5)
            client_socket.send(pickle.dumps(l))
            respond=client_socket.recv(2048)
            respond=respond.decode("utf-8")
            self.browser.append("<p style='color: #b03f3c'><i>DocBot:</i></p><b> {}</b>".format(str(respond)))
            self.client.settimeout(None)

        except sock.timeout:
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to send Vital signs data</b></p>")
            self.browser.append("Reason:"+str(err))
            self.fever.setEnabled(False)
            self.headache.setEnabled(False)
            self.diarrhea.setEnabled(False)
            self.sneezing.setEnabled(False)
            self.vomiting.setEnabled(False)
            self.heartburn.setEnabled(False)
            self.sr.setEnabled(False)
            self.ab.setEnabled(False)
            self.yes.setEnabled(False)
            self.no.setEnabled(False)


    def send(self,data):    
        data=data.encode("utf-8")
        
        try:    
            self.client.send(data)
        except sock.error as err:
            self.closeConnection()
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to send data</b></p>")

        self.recieve()

    def recieve(self):
        
        try:
            self.client.settimeout(5)
            respond=self.client.recv(2048)
            respond=respond.decode("utf-8")
            self.browser.append("<p style='color: #b03f3c'><i>DocBot:</i></p><b> {}</b>".format(respond))
            self.client.settimeout(None)

        except sock.timeout:
            self.closeConnection()
            self.browser.append("<p style='color:#b03f3c'><b>connection was closed because you were idle for so long</b></p>")
    
    def closeConnection(self):
        self.browser.append("<p style='color:#b03f3c'><b>Connection was terminated</b></p>")
        self.fever.setEnabled(False)
        self.headache.setEnabled(False)
        self.diarrhea.setEnabled(False)
        self.sneezing.setEnabled(False)
        self.vomiting.setEnabled(False)
        self.heartburn.setEnabled(False)
        self.sr.setEnabled(False)
        self.ab.setEnabled(False)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        self.client.close()
        self.back.show()



    def add(self,disease):

        if (disease in self.payload):
            self.browser.append("<p style='color: #b03f3c'><i>DocBot:</i></p> <b>You already have chosen this</b>" )
        else:    
            self.payload.append(disease)
            self.browser.append("<p style='color: #b03f3c'><i>Me:</i></p><b> {}</b>".format(disease))
            self.send(disease)

        self.fever.setEnabled(False)
        self.headache.setEnabled(False)
        self.diarrhea.setEnabled(False)
        self.sneezing.setEnabled(False)
        self.vomiting.setEnabled(False)
        self.heartburn.setEnabled(False)
        self.sr.setEnabled(False)
        self.ab.setEnabled(False)

        self.yes.setEnabled(True)
        self.no.setEnabled(True)
    
    def yesClicked(self):
        self.browser.append("<p style='color: #b03f3c'><i>Me:</i></p><b> Yes</b>")
        self.fever.setEnabled(True)
        self.headache.setEnabled(True)
        
        self.diarrhea.setEnabled(True)
        self.sneezing.setEnabled(True)
        self.vomiting.setEnabled(True)
        self.heartburn.setEnabled(True)
        self.sr.setEnabled(True)
        self.ab.setEnabled(True)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)

    def noClicked(self):
        self.browser.append("<p style='color: #b03f3c'><i>Me:</i></p><b> No</b>")
        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        #self.payload.append('0')
        self.send("n")
        self.closeConnection()

    def backClicked(self):
        Main(self).show()
        self.close()


class Chat(QtWidgets.QMainWindow,CHAT_CLASS):
    def __init__(self,parent=None):
        super(Chat,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.start()
        self.setFixedSize(800, 600)

        self.exit.clicked.connect(lambda :self.exitClicked())
        self.chatbox.returnPressed.connect(lambda: self.sendreply())
        self.refresh.clicked.connect(lambda: self.recieveReply())
        self.back.clicked.connect(lambda: self.backClicked())
        self.back.hide()

    def start(self):
        try:
            client_socket=sock.socket(sock.AF_INET,sock.SOCK_STREAM)
        except sock.error as err:
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to create client</b></p>")
            self.browser.append("Reason:"+str(err))
            sys.exit()

        try:
            client_socket.connect((target_host,target_port))
            self.browser.append("<p style='color:#b03f3c'><b>Connected to server</b></p>")
            self.client=client_socket

        except sock.error as err:
            self.browser.append("<p style='color:#b03f3c'><b>FAILED to connect to server</b></p>")
            self.browser.append("Reason:"+str(err))
            sys.exit()
        
        l=['c',NAME,list(vitals.values())]    
        self.client.send(pickle.dumps(l))

        respond=self.client.recv(2048)
        respond=respond.decode("utf-8")
        self.browser.append("{}".format(respond))

        

    def exitClicked(self):
        self.client.send("f".encode("utf-8")) 
        self.browser.append("<p style='color:#b03f3c'><b>Connection was terminated</b></p>")
        self.client.close()
        self.exit.hide()
        self.chatbox.hide()
        self.refresh.hide()
        self.back.show()

    def backClicked(self):
        Main(self).show()
        self.close()


    def sendreply(self):
        reply = self.chatbox.text()
        self.chatbox.setText('')
        self.client.send(reply.encode("utf-8")) 
        self.browser.append("<p style='color: #b03f3c'><i>Me:</i></p><b> {}</b>".format(str(reply)))

    def recieveReply(self):
        respond=self.client.recv(2048)
        respond=respond.decode("utf-8")
        self.browser.append("<p style='color: #b03f3c'><i>Doctor:</i></p><b> {}</b>".format(str(respond)))
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    window= Main()
    window.show()  
    app.exec_() 


if __name__ == '__main__':
    main()

# client =sock.socket(sock.AF_INET,sock.SOCK_STREAM)

# client.connect(('127.0.0.1', 5555))

# while True:

#     request= str(input())

#     request=request.encode('ascii')

#     client.send(request)

#     response=client.recv(512)

#     response=response.decode('ascii')

#     print(response)

   


# #     client.close()
#  more=input("anything else?")

#                 if more.lower() == 'y':
#                     payload=str(input("what do you feel"))
#                 elif more.lower() == 'n':
#                     payload="n"
#                     client.send(payload.encode("utf-8"))
#                     respond=client.recv(2048)
#                     print(str(respond))
#                     break