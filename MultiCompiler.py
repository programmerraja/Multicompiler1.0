import tkinter as t
from tkinter import scrolledtext,filedialog,messagebox
from os import getcwd
""" A online multi compiler program """
import requests as r
from sys import argv
class MultiCompiler():
    def __init__(self):
            """ header for the request """
            self.__header={ "path":"/main.php",
                        "scheme":"https",
                        "accept":"application/json,text/javascript, */*; q=0.01",
                        "accept-encoding":"gzip, deflate, br",
                        "accept-language":"en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7",
                        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
                        "origin":"https://ide.geeksforgeeks.org",
                        "refere":"https://ide.geeksforgeeks.org/",
                        "sec-fetch-dest":"empty",
                        "sec-fetch-mode":"cors",
                        "sec-fetch-site":"same-origin",
                        "user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
                        "x-requested-with":"XMLHttpRequest"}
            self.input=""
            self.fname=""
            self.compilerwindow=t.Tk()
            self.dir=getcwd()
            self.color="#7d3cff"
            self.compilerwindow.configure(bg=self.color)
            self.compilerwindow.title("MultiCompiler")
            self.compilerwindow.geometry("700x700+0+0")
            self.label=t.Label(self.compilerwindow,text="MultiCompiler",fg="#ff5a09",bg="#7d3cff",font=("times new roman",35,"italic")).place(x=150,y=10)

            
            self.lang=t.StringVar()
            self.lang.set("python")
            #drop down option for language
            temp=["C","Cpp","Java","Python3","Csharp", "Scala" ,"Perl","python"]
            self.dropdown=t.OptionMenu(self.compilerwindow,self.lang,*temp)
            self.dropdown.place(x=465,y=120)
            #menu 
            self.menu=t.Menu(self.compilerwindow)
            self.compilerwindow.config(menu=self.menu)
            #submenu 1
            self.File=t.Menu(self.menu,tearoff=0)
            self.File.add_command(label='Open',command=self.open_file)
            self.File.add_command(label='Save',command=self.save)
            self.File.add_command(label='Save As..',command=self.save_as)
            #adding sub menu to menu
            self.menu.add_cascade(label="File",menu=self.File)
            #sub menu 2
            self.Help=t.Menu(self.menu,tearoff=0)
            self.Help.add_command(label='About Me',command=self.about_us)
            #adding sub menu 2
            self.menu.add_cascade(label="Help",menu=self.Help)
            
            #sub menu 3
            self.run=t.Menu(self.menu,tearoff=0)
            self.run.add_command(label='Run  f5',command=self.runit)
            #adding sub menu 3
            self.menu.add_cascade(label="Run",menu=self.run)
            #code
            self.code_label=t.Label(self.compilerwindow,text="Code:",bg=self.color,font=("times new roman",15,"bold"),fg="#f2d53c")
            self.code_label.place(x=10,y=128)
            
            self.text_code=scrolledtext.ScrolledText(self.compilerwindow,width=65,height=20,wrap="word",relief="groove")
            self.text_code.place(x=10,y=150)
            self.compilerwindow.bind("<F5>",lambda e :self.runit())

            #input
            self.input_label=t.Label(self.compilerwindow,text="Input:",bg=self.color,font=("times new roman",15,"bold"),fg="#f2d53c")
            self.input_label.place(x=555,y=120)
            
            self.text_input=scrolledtext.ScrolledText(self.compilerwindow,width=15,height=20,wrap="word",relief="groove")
            self.text_input.place(x=555,y=150)

            #output
            self.output_label=t.Label(self.compilerwindow,text="Output:",bg=self.color,font=("times new roman",15,"bold"),fg="#f2d53c")
            self.output_label.place(x=10,y=480)
            
            self.text_output=scrolledtext.ScrolledText(self.compilerwindow,width=65,height=11,wrap="word",relief="groove")
            self.text_output.place(x=10,y=505)
            self.text_output["state"]="disabled"
            self.compilerwindow.mainloop()

           
    def runit(self):
        """ geting and evaluating the cmd line input """
        self.code=self.text_code.get("1.0","end")
        self.input=self.text_input.get("1.0","end")
        self.text_output["state"]="normal"
        self.compileit()
        self.text_output["state"]="disabled"
            
    def open_file(self):
        """ open the src code file and read it """
        #befroe open clear the text
        self.text_code.delete('1.0',"end")
        file=filedialog.askopenfilename(initialdir=self.dir)
        if(file):
            open_file=open(file,"r")
            li=open_file.name.split("/")
            self.fname=li[len(li)-1]
            self.text_code.insert('1.0', open_file.read())
        else:
              messagebox.showinfo("ERROR","No File Found")
    def save(self):
        if(self.fname):
                open(self.fname,"w").write(self.text_code.get("1.0","end"))
        else:
            self.save_as()
            
    def save_as(self):
          self.fname=filedialog.asksaveasfilename(initialdir=self.dir)
          if(self.fname):
              open(self.fname,"w").write(self.text_code.get("1.0","end"))
            
    def compileit(self):
        self.text_output.delete('1.0',"end")
        
        """ compile the progam using geeksforgeeks api """
        se=r.Session()
        data={"lang":self.lang.get() ,"code":self.code ,"input":self.input, "save":"false"}
        
        try:
           
            outputid=se.post("https://ide.geeksforgeeks.org/main.php",data=data,headers=self.__header)
            
            """ looping until the status until it sucess"""
        
            if(outputid.json()["status"]=="SUCCESS"):
                    data2={"sid":outputid.json()["sid"],"requestType":"fetchResults"}
                    output_json=se.post("https://ide.geeksforgeeks.org/submissionResult.php",data=data2)
                    while(output_json.json()['status']== 'IN-QUEUE'):
                         output_json=se.post("https://ide.geeksforgeeks.org/submissionResult.php",data=data2)
            elif (outputid.json()["status"]=='ERROR'):
                    self.text_output.insert("1.0",outputid.json()['message'])
                    return
        except :
            self.text_output.insert("1.0","No Internet Connection!")
            return 

        """ output in json fromat"""
        if(output_json):
            self.text_output.delete('1.0',"end")
            output=output_json.json()
            if(output.get("output",0)):
                 self.text_output.insert("1.0",output["output"])
                 if(output.get("warning",0)):
                              self.text_output.insert("2.0","\nWARNNING:\n"+output["warning"])
                 if(output.get("cmpError",0)):
                        self.text_output.insert(1.0,"CompilerError:\n"+output["cmpError"])
                 if(output.get("rntError",0)):
                      self.text_output.insert("1.0",output["rntError"])
            elif(output.get("cmpError",0)):
                        self.text_output.insert(1.0,"CompilerError:\n"+output["cmpError"])
            elif(output.get("rntError",0)):
                self.text_output.insert("1.0",output["rntError"])
            else:
                self.text_output.insert("1.0","No Output!")
                        
    def about_us(self):
        top=t.Toplevel(self.compilerwindow)
        top.title("About Me")
        top.configure(bg="yellow")
        top.geometry("250x250+10+10")
        top.resizable(0,0)
        label=t.Label(top, bg="yellow",fg="red",text="\n\nI  Am  Programmer\n \n Who Love To Do Something New \n\n My Special Thanks To Geeksforgeeks",font=("times new roman",10,"bold"))
        label.place(x=3,y=3)

MultiCompiler()
