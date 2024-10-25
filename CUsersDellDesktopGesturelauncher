import boto3
import tkinter as tk
import os
import sys
from tempfile import gettempdir
from contextlib import closing

root=tk.Tk()
root.geometry("400x240")
root.title("T2S-CONVERTER AMZON POLLY")
textExample=tk.Text(root,height=10)
textExample.pack()

def gettext():
    aws_mag_con=boto3.session.Session(profile_name='Simran')
    client=aws_mag_con.client(service_name='polly',region_name='ap-south-1')
    result=textExample.get("1.0","end")
    print(result)
    response=client.synthesize_speech(VoiceId='Joanna',OutputFormat='mp3',Text=result,Engine='neural')
    print(response)
    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output=os.path.join(gettempdir(),"speech.mp3")
            try:
                with open(output,"wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Cloud could not find the stream!")
        sys.exit(-1)

    if sys.platform=='win32':
        os.startfile(output)                   

btnRead=tk.Button(root,height=1,width=10,text="Read",command=gettext)

btnRead.pack()
root.mainloop()