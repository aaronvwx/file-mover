import os
import shutil
import glob
import time
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from datetime import *
import threading






#Variabelen

#loglist werkt nog niet
extensielist = ["/", "mp3", "wav", "ogg", "midi", "aif", "cda", "mid", "mpa", "wma", "wpl", "m3u", "zip", "rar", "z", "7z", "arj", "deb", "pkg", "rpm", "tar.gz", "jpg", "jpeg", "png", "gif", "ico", "svg", "ps", "psd", "ai", "bmp", "tif", "tiff", "CR2", "exe", "com", "bat", "apk", "gadget", "jar", "wsf", "mp4", "avi", "mpg", "mpeg", "h264", "flv", "3g2", "3gp", "m4v", "mkv", "rm", "swf", "vob", "wmv", "mov", "pptx", "ppt", "pps", "odp", "key", "docx", "doc", "pdf", "txt", "odt","rtf","tex","wks","wps","wpd","py","c","class","dart","swift","sh","html","h","tmp","sys","lnk","msi","ico","icns","bak","cab","dmp","cfg","cpl","cur","dll","drv","ini","xlsx","xls","xlr","od","asp","aspx","cer","cfm","cgi","pl","css","htm","js","jsp","part","php","rss","xhtml","fnt","fon","otf","ttf","csv","dat","db","dbf","log","mdb","sav","sql","tar","xml","json","bin","dmg","iso","toast","vcd"]
aantalsorteer = 0
timerstatus = False



#Functions

#Sorteren, kijkt in map (src) en sorteert naar (dest)------------
def sort(dest, ext):
    global loglist
    global src2
    x = 0
    src = cfglisted[0]
    src2 = src.strip("\n") #strips \n want anders is dat geen 'map'
    dest2 = dest.strip("\n")
    src_file = glob.glob(f"{src2}/*.{ext}") #maakt lijst van alle files met die bepaalde extensies
    while len(src_file) != x: #zolang er files in de lijst zitten
        src_dir = f"{src2}"
        src_file2 = src_file[x].replace(f"{src2}", "") #src file2 wil alleen de naam zonder path
        if len(src_file2) > 0:
            src_file2 = src_file2[0 : 0 : ] + src_file2[0 + 1 : :] #haalt de '\' eruit
        if dest2 != "": #kijkt of de dest file niet leeg is ingegeven, anders doet hij niets
            rawfilename = os.path.splitext(src_file2)[0]
            if src2 == dest2:
                x+=1
                continue
            if not os.path.exists(f"{dest2}"):
                os.makedirs(f"{dest2}")
            if not os.path.isfile(f"{dest2}/{src_file2}"): #kijkt of filenaam al bestaat in die dest path
                dest_dir = f"{dest2}"
                shutil.move(src_file[x],dest_dir) #verplaatsing
                loglist.append(f"{dest2}/{rawfilename}.{ext}")
            else: #als filenaam al bestaat
                today = date.today()
                d = today.strftime("%d-%m-%Y")
                s = datetime.now().second
                m = datetime.now().minute
                u = datetime.now().hour
                newfilename = f"{rawfilename}({u}.{m}.{s}, {d})" #originele naam + huidige datum
                os.rename(src_file[x],f'{src2}/{newfilename}.{ext}')#rename
                dest_dir = f"{dest2}"
                shutil.move(f"{src2}/{newfilename}.{ext}",dest_dir)
                loglist.append(f"{dest2}/{newfilename}.{ext}")
            with open('log.txt', 'w') as f:
                for i in loglist:
                    f.write("%s\n" % i)
        x += 1
#---------------------------


#Opent verkenner voor src te selecteren
def verkenner(src2, e) :
    global cfglisted2
    global cfglisted
    global src
    #window.wm_state('iconic') #minimized main window want anders 'bugt' hij wat
    src = filedialog.askdirectory()
    cfglisted[src2] = src + "\n"
    e.delete(0,END) #Ingeven in balk
    e.insert(0,src)
    with open('cfg.txt', 'w') as f:
        cfglisted2 = []
        for s in cfglisted:
            cfglisted2.append(s.strip("\n")) #maakt 2de lijst aant om in cfg te schrijven omdat hij anders met 2 \n's zou schrijven
        for i in cfglisted2:
            f.write("%s\n" % i)
    with open('cfg.txt', 'r') as f:
        cfglisted = f.readlines()
        src = cfglisted[0]


#Timer -------------
def timer():
    global timerstatus
    timerstatus = not timerstatus
    if timerstatus == True:
        timerbutton['text'] = "Stop"
        timerbutton['bg'] = "red2"
        sorteer()
    else:
        timerbutton['text'] = "Start"
        timerbutton['bg'] = "green2"
        
    

        
#als je op de sorteerknop drukt, gebruikt hij sort funtie ---------------------
def sorteer() :
    global aantalsorteer
    global lbl1
    global lbl2
    global lbl3
    global timerstatus
    global loglist
    global src
    global src3
    tijd1 = []
    tijd2 = []
    tijd3 = []
    src3 = src.strip("\n")
    loglist = [f'Van [{src3}] naar:\n']
    i = 1
    while i < 132: #sorteert alle extensies met lists (zie extensielist bovenaan)
        sort(cfglisted[i], extensielist[i])
        i+=1


    #Datum weergeven van sorteerknop -------------------------     
    datesorteer = []
    uursorteer = datetime.now().hour
    if uursorteer < 10:
        uursorteer = str(uursorteer)
        uursorteer = f"0{uursorteer}"
    else:
        uursorteer = str(uursorteer)
    minuutsorteer = datetime.now().minute
    if minuutsorteer < 10:
        minuutsorteer = str(minuutsorteer)
        minuutsorteer = f"0{minuutsorteer}"
    else:
        minuutsorteer = str(minuutsorteer)
    secondesorteer = datetime.now().second
    if secondesorteer < 10:
        secondesorteer = str(secondesorteer)
        secondesorteer = f"0{secondesorteer}"
    else:
        secondesorteer = str(secondesorteer)
    datesorteer.append(uursorteer)
    datesorteer.append(minuutsorteer)
    datesorteer.append(secondesorteer)
    if aantalsorteer == 0:
        lbl1['text'] = "[" + ":".join(datesorteer) + "]  Succesvol gesorteerd."
        aantalsorteer += 1
    elif aantalsorteer == 1:
        lbl2['text'] = lbl1['text']
        lbl1['text'] = "[" + ":".join(datesorteer) + "]  Succesvol gesorteerd."
        aantalsorteer += 1
    elif aantalsorteer > 1:
        lbl3['text'] = lbl2['text']
        lbl2['text'] = lbl1['text']
        lbl1['text'] = "[" + ":".join(datesorteer) + "]  Succesvol gesorteerd."
        aantalsorteer += 1


    if timerstatus == True:
        threading.Timer(10.0, sorteer).start()
        
    #------------------------------------
def undo():
    with open('log.txt', 'r') as f:
        loglisted = f.readlines()
    i=0
    while len(loglisted) > i:
        loglisted[i] = loglisted[i].strip("\n")
        i+=1
    loglisted.remove('')
    loglisted[0] = loglisted[0].replace(f"Van [", "")
    loglisted[0] = loglisted[0].replace(f"] naar:", "")
    i = 1
    try:
        while len(loglisted) > i:
            shutil.move(loglisted[i],loglisted[0])
            i+=1
    except:
        pass

    
'''def writer():
    if len(cfglisted) < 2:
        i = 1
        while i < 12:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Music")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 12:            
                f.write("%s\n" % cfglisted[i])
                i += 1'''
#----------------------------




    

'''#to do list       
    #Log
    #Undo'''

"""with open('log.txt', 'w') as f:
    for i in loglist:
        f.write("%s\n" % i)"""



# Lees cfg file, eerste lijn en zet die in entry box voor default src
with open('cfg.txt', 'r') as f:
    cfglisted = f.readlines()

replaced = False
if cfglisted != []:
    for n, i in enumerate(cfglisted):
       if i == "\n":
          cfglisted[n] = ""
          replaced = True
if replaced == True:
    cfglisted = []


if cfglisted == []:
    cfglisted.append(f"C:/Users/{os.getlogin()}/Downloads")

global cfglisted2    
cfglisted2 = []
with open('cfg.txt', 'w') as f:
        for s in cfglisted:
            cfglisted2.append(s.strip("\n"))
        for i in cfglisted2:
            f.write("%s\n" % i)

src = cfglisted[0]
src2 = src.strip('\n')





#Open GUI Sorteer-------------------------------------------------------------------------------------------------------------------------
global lbl1
global lbl2
global lbl3
window = Tk()
 
window.title("Sorteerder")
 
window.geometry('520x250')

Label(window, text="").grid(column=0, row=0, sticky=W)
 
Label(window, text="Welke map wil je sorteren?").grid(column=0, row=1, sticky=W)

e1 = Entry(window, width = 50)
e1.grid(column=1, row=1, sticky=W)
e1.insert(0,cfglisted[0])

#Zoekknop
Label(window, text="").grid(column=2, row=2, sticky=W)
Button(window, text="Zoek", command= lambda: verkenner(0, e1)).grid(column=3, row=1, sticky=W)


#Timer
timerbutton = Button(window, text="Start", command=timer, bg = "green2")
timerbutton.grid(column=3, row=7, sticky=W)
Label(window, text="Timer (10s)").grid(column=3, row=6, sticky=W)

#Sorteerknop
Label(window, text="").grid(column=0, row=3, sticky=W)
Label(window, text="").grid(column=0, row=4, sticky=W)
Label(window, text="").grid(column=0, row=5, sticky=W)
Button(window, text="Sorteer", command=sorteer).grid(column=0, row=6, sticky=W)
lbl1 = Label(window, text="")
lbl1.grid(column=0, row=7, columnspan=2, sticky=W)
lbl2 = Label(window, text="")
lbl2.grid(column=0, row=8, columnspan=2, sticky=W)
lbl3 = Label(window, text="")
lbl3.grid(column=0, row=9, columnspan=2, sticky=W)
Label(window, text="").grid(column=3, row=8, sticky=W)
Button(window, text="Undo", command=undo, bg = "orange2").grid(column=3, row=9, sticky=W)


 


#Gui Destinations
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#Zet default voor als de entry's leeg zijn
if len(cfglisted) < 2:
        i = 1
        while i < 12:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Music")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 12:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 13:
        i = 12
        while i < 21:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Compressed")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 21:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 23:
        i = 21
        while i < 34:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Images")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 34:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 35:
        i = 34
        while i < 41:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Executables")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 41:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 42:
        i = 41
        while i < 56:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Videos")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 56:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 57:
        i = 56
        while i < 61:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Presentaties")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 61:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 62:
        i = 61
        while i < 63:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Word")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 63:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 64:
        i = 63
        while i < 64:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Pdf")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 64:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 65:
        i = 64
        while i < 71:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Text")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 71:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 72:
        i = 71
        while i < 79:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Programmeren")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 79:            
                f.write("%s\n" % cfglisted[i])
                i += 1

if len(cfglisted) < 80:
        i = 79
        while i < 94:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/System")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 94:            
                f.write("%s\n" % cfglisted[i])
                i += 1


if len(cfglisted) < 95:
        i = 94
        while i < 98:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Spreadsheets")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 98:            
                f.write("%s\n" % cfglisted[i])
                i += 1
if len(cfglisted) < 99:
        i = 98
        while i < 112:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Internet")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 112:            
                f.write("%s\n" % cfglisted[i])
                i += 1
if len(cfglisted) < 113:
        i = 112
        while i < 116:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Fonts")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 116:            
                f.write("%s\n" % cfglisted[i])
                i += 1
if len(cfglisted) < 117:
        i = 116
        while i < 127:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Data")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 127:            
                f.write("%s\n" % cfglisted[i])
                i += 1
if len(cfglisted) < 128:
        i = 127
        while i < 132:
            cfglisted.append(f"C:/Users/{os.getlogin()}/Documents/Disc")
            i += 1
        open('cfg.txt', 'w').close()
        i = 0
        with open('cfg.txt', 'w') as f:
            while i < 132:            
                f.write("%s\n" % cfglisted[i])
                i += 1





#opent destination gui
#Note: waarschijnlijk wat opkuisbaarder, regelen we wel als alles klaar is en werkt
def destinationgui():
    global destinations
    
        
    destinations = Tk()
    destinations.title("Destinations")
    destinations.geometry("800x600")
                  


    
    #Labels 1st column
    Label(destinations, text="1/4").grid(column=0, row=0, sticky=W)
    Label(destinations, text="").grid(column=0, row=1, sticky=W)
    Label(destinations, text="").grid(column=1, row=1, sticky=W)

    
    Label(destinations, text="Audio", underline =True).grid(column=2, columnspan = 2, row=0, sticky=W)
    Label(destinations, text=".mp3").grid(column=3, row=1, sticky=W)
    Label(destinations, text=".wav").grid(column=3, row=2, sticky=W)
    Label(destinations, text=".ogg").grid(column=3, row=3, sticky=W)
    Label(destinations, text=".midi").grid(column=3, row=4, sticky=W)
    Label(destinations, text=".aif").grid(column=3, row=5, sticky=W)
    Label(destinations, text=".cda").grid(column=3, row=6, sticky=W)
    Label(destinations, text=".mid").grid(column=3, row=7, sticky=W)
    Label(destinations, text=".mpa").grid(column=3, row=8, sticky=W)
    Label(destinations, text=".wma").grid(column=3, row=9, sticky=W)
    Label(destinations, text=".wpl").grid(column=3, row=10, sticky=W)
    Label(destinations, text=".m3u").grid(column=3, row=11, sticky=W)

    Label(destinations, text="<", width=2, font=("Courier", 35), fg='SystemButtonFace').grid(rowspan=2,column=0, row=10, sticky=N)

    Label(destinations, text="Compressed", underline =True).grid(column=2, columnspan = 2, row=12, sticky=S)
    Label(destinations, text=".zip").grid(column=3, row=13, sticky=W)
    Label(destinations, text=".rar").grid(column=3, row=14, sticky=W)
    Label(destinations, text=".z").grid(column=3, row=15, sticky=W)
    Label(destinations, text=".7z").grid(column=3, row=16, sticky=W)
    Label(destinations, text=".arj").grid(column=3, row=17, sticky=W)
    Label(destinations, text=".deb").grid(column=3, row=18, sticky=W)
    Label(destinations, text=".pkg").grid(column=3, row=19, sticky=W)
    Label(destinations, text=".rpm").grid(column=3, row=20, sticky=W)
    Label(destinations, text=".tar.gz").grid(column=3, row=21, sticky=W)
    Label(destinations, text="").grid(column=2, row=23, sticky=W)

    #Entrys 1st column
    d1 = Entry(destinations, width = 30)
    d1.grid(column=4, row=1, sticky=W)
    d2 = Entry(destinations, width = 30)
    d2.grid(column=4, row=2, sticky=W)
    d3 = Entry(destinations, width = 30)
    d3.grid(column=4, row=3, sticky=W)
    d4 = Entry(destinations, width = 30)
    d4.grid(column=4, row=4, sticky=W)
    d5 = Entry(destinations, width = 30)
    d5.grid(column=4, row=5, sticky=W)
    d6 = Entry(destinations, width = 30)
    d6.grid(column=4, row=6, sticky=W)
    d7 = Entry(destinations, width = 30)
    d7.grid(column=4, row=7, sticky=W)
    d8 = Entry(destinations, width = 30)
    d8.grid(column=4, row=8, sticky=W)
    d9 = Entry(destinations, width = 30)
    d9.grid(column=4, row=9, sticky=W) 
    d10 = Entry(destinations, width = 30)
    d10.grid(column=4, row=10, sticky=W)    
    d11 = Entry(destinations, width = 30)
    d11.grid(column=4, row=11, sticky=W)   
    d12 = Entry(destinations, width = 30)
    d12.grid(column=4, row=13, sticky=W)
    d13 = Entry(destinations, width = 30)
    d13.grid(column=4, row=14, sticky=W)
    d14 = Entry(destinations, width = 30)
    d14.grid(column=4, row=15, sticky=W)
    d15 = Entry(destinations, width = 30)
    d15.grid(column=4, row=16, sticky=W) 
    d16 = Entry(destinations, width = 30)
    d16.grid(column=4, row=17, sticky=W)
    d17 = Entry(destinations, width = 30)
    d17.grid(column=4, row=18, sticky=W) 
    d18 = Entry(destinations, width = 30)
    d18.grid(column=4, row=19, sticky=W)  
    d19 = Entry(destinations, width = 30)
    d19.grid(column=4, row=20, sticky=W)    
    d20 = Entry(destinations, width = 30)
    d20.grid(column=4, row=21, sticky=W)    
        
    #Values 1st column
    d1.insert(0,cfglisted[1])
    d2.insert(0,cfglisted[2])
    d3.insert(0,cfglisted[3])
    d4.insert(0,cfglisted[4])
    d5.insert(0,cfglisted[5])
    d6.insert(0,cfglisted[6])
    d7.insert(0,cfglisted[7])
    d8.insert(0,cfglisted[8])
    d9.insert(0,cfglisted[9])
    d10.insert(0,cfglisted[10])
    d11.insert(0,cfglisted[11])
    d12.insert(0,cfglisted[12])
    d13.insert(0,cfglisted[13])
    d14.insert(0,cfglisted[14])
    d15.insert(0,cfglisted[15])
    d16.insert(0,cfglisted[16])
    d17.insert(0,cfglisted[17])
    d18.insert(0,cfglisted[18])
    d19.insert(0,cfglisted[19])
    d20.insert(0,cfglisted[20])

    #Buttons 1st column
    Label(destinations, text="").grid(column=5, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(1, d1)).grid(column=6, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(2, d2)).grid(column=6, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(3, d3)).grid(column=6, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(4, d4)).grid(column=6, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(5, d5)).grid(column=6, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(6, d6)).grid(column=6, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(7, d7)).grid(column=6, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(8, d8)).grid(column=6, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(9, d9)).grid(column=6, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(10, d10)).grid(column=6, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(11, d11)).grid(column=6, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(12, d12)).grid(column=6, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(13, d13)).grid(column=6, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(14, d14)).grid(column=6, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(15, d15)).grid(column=6, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(16, d16)).grid(column=6, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(17, d17)).grid(column=6, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(18, d18)).grid(column=6, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(19, d19)).grid(column=6, row=20, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(20, d20)).grid(column=6, row=21, sticky=W)




    #Labels 2nd column
    Label(destinations, text="--------", fg='SystemButtonFace').grid(column=7, row=1, sticky=W)
    Label(destinations, text="Images", underline =True).grid(column=8, row=0, sticky=W)
    Label(destinations, text=".jpg").grid(column=9, row=1, sticky=W)
    Label(destinations, text=".jpeg").grid(column=9, row=2, sticky=W)
    Label(destinations, text=".png").grid(column=9, row=3, sticky=W)
    Label(destinations, text=".gif").grid(column=9, row=4, sticky=W)
    Label(destinations, text=".ico").grid(column=9, row=5, sticky=W)
    Label(destinations, text=".svg").grid(column=9, row=6, sticky=W)
    Label(destinations, text=".ps").grid(column=9, row=7, sticky=W)
    Label(destinations, text=".psd").grid(column=9, row=8, sticky=W)
    Label(destinations, text=".ai").grid(column=9, row=9, sticky=W)
    Label(destinations, text=".bmp").grid(column=9, row=10, sticky=W)
    Label(destinations, text=".tif").grid(column=9, row=11, sticky=W)
    Label(destinations, text=".tiff").grid(column=9, row=12, sticky=W)
    Label(destinations, text=".CR2").grid(column=9, row=13, sticky=W)

    Button(destinations, text=">", font=("Courier", 35), command=desttab2).grid(rowspan=5,column=13, row=9, sticky=E)

    Label(destinations, text="Executables", underline =True).grid(column=8, columnspan = 2, row=14, sticky=S)
    Label(destinations, text=".exe").grid(column=9, row=15, sticky=W)
    Label(destinations, text=".com").grid(column=9, row=16, sticky=W)
    Label(destinations, text=".bat").grid(column=9, row=17, sticky=W)
    Label(destinations, text=".apk").grid(column=9, row=18, sticky=W)
    Label(destinations, text=".gadget").grid(column=9, row=19, sticky=W)
    Label(destinations, text=".jar").grid(column=9, row=20, sticky=W)
    Label(destinations, text=".wsf").grid(column=9, row=21, sticky=W)


    #Entrys 2nd column
    d21 = Entry(destinations, width = 30)
    d21.grid(column=10, row=1, sticky=W)
    d22 = Entry(destinations, width = 30)
    d22.grid(column=10, row=2, sticky=W)
    d23 = Entry(destinations, width = 30)
    d23.grid(column=10, row=3, sticky=W)
    d24 = Entry(destinations, width = 30)
    d24.grid(column=10, row=4, sticky=W)
    d25 = Entry(destinations, width = 30)
    d25.grid(column=10, row=5, sticky=W)
    d26 = Entry(destinations, width = 30)
    d26.grid(column=10, row=6, sticky=W)
    d27 = Entry(destinations, width = 30)
    d27.grid(column=10, row=7, sticky=W)
    d28 = Entry(destinations, width = 30)
    d28.grid(column=10, row=8, sticky=W)
    d29 = Entry(destinations, width = 30)
    d29.grid(column=10, row=9, sticky=W) 
    d30 = Entry(destinations, width = 30)
    d30.grid(column=10, row=10, sticky=W)    
    d31 = Entry(destinations, width = 30)
    d31.grid(column=10, row=11, sticky=W)   
    d32 = Entry(destinations, width = 30)
    d32.grid(column=10, row=12, sticky=W)
    d33 = Entry(destinations, width = 30)
    d33.grid(column=10, row=13, sticky=W)
    d34 = Entry(destinations, width = 30)
    d34.grid(column=10, row=15, sticky=W)
    d35 = Entry(destinations, width = 30)
    d35.grid(column=10, row=16, sticky=W) 
    d36 = Entry(destinations, width = 30)
    d36.grid(column=10, row=17, sticky=W)
    d37 = Entry(destinations, width = 30)
    d37.grid(column=10, row=18, sticky=W) 
    d38 = Entry(destinations, width = 30)
    d38.grid(column=10, row=19, sticky=W)  
    d39 = Entry(destinations, width = 30)
    d39.grid(column=10, row=20, sticky=W)    
    d40 = Entry(destinations, width = 30)
    d40.grid(column=10, row=21, sticky=W)



    #Values 2nd column
    d21.insert(0,cfglisted[21])
    d22.insert(0,cfglisted[22])
    d23.insert(0,cfglisted[23])
    d24.insert(0,cfglisted[24])
    d25.insert(0,cfglisted[25])
    d26.insert(0,cfglisted[26])
    d27.insert(0,cfglisted[27])
    d28.insert(0,cfglisted[28])
    d29.insert(0,cfglisted[29])
    d30.insert(0,cfglisted[30])
    d31.insert(0,cfglisted[31])
    d32.insert(0,cfglisted[32])
    d33.insert(0,cfglisted[33])
    d34.insert(0,cfglisted[34])
    d35.insert(0,cfglisted[35])
    d36.insert(0,cfglisted[36])
    d37.insert(0,cfglisted[37])
    d38.insert(0,cfglisted[38])
    d39.insert(0,cfglisted[39])
    d40.insert(0,cfglisted[40])


    #Buttons 2nd column
    Label(destinations, text="").grid(column=11, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(21, d21)).grid(column=12, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(22, d22)).grid(column=12, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(23, d23)).grid(column=12, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(24, d24)).grid(column=12, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(25, d25)).grid(column=12, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(26, d26)).grid(column=12, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(27, d27)).grid(column=12, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(28, d28)).grid(column=12, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(29, d29)).grid(column=12, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(30, d30)).grid(column=12, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(31, d31)).grid(column=12, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(32, d32)).grid(column=12, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(33, d33)).grid(column=12, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(34, d34)).grid(column=12, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(35, d35)).grid(column=12, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(36, d36)).grid(column=12, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(37, d37)).grid(column=12, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(38, d38)).grid(column=12, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(39, d39)).grid(column=12, row=20, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(40, d40)).grid(column=12, row=21, sticky=W)

    
def clear():
    global destinations
    list = destinations.grid_slaves()
    for l in list:
        l.destroy()



def desttab2():
    global destinations
    clear()


    #Labels 3rd column
    Label(destinations, text="2/4").grid(column=0, row=0, sticky=W)
    Label(destinations, text="Video", underline =True).grid(column=2, columnspan = 2, row=0, sticky=W)
    Label(destinations, text=".mp4").grid(column=3, row=1, sticky=W)
    Label(destinations, text=".avi").grid(column=3, row=2, sticky=W)
    Label(destinations, text=".mpg").grid(column=3, row=3, sticky=W)
    Label(destinations, text=".mpeg").grid(column=3, row=4, sticky=W)
    Label(destinations, text=".h264").grid(column=3, row=5, sticky=W)
    Label(destinations, text=".flv").grid(column=3, row=6, sticky=W)
    Label(destinations, text=".3g2").grid(column=3, row=7, sticky=W)
    Label(destinations, text=".3gp").grid(column=3, row=8, sticky=W)
    Label(destinations, text=".m4v").grid(column=3, row=9, sticky=W)
    Label(destinations, text=".mkv").grid(column=3, row=10, sticky=W)
    Label(destinations, text=".rm").grid(column=3, row=11, sticky=W)
    Label(destinations, text=".swf").grid(column=3, row=12, sticky=W)
    Label(destinations, text=".vob").grid(column=3, row=13, sticky=W)
    Label(destinations, text=".wmv").grid(column=3, row=14, sticky=W)
    Label(destinations, text=".mov").grid(column=3, row=15, sticky=W)

    Button(destinations, text="<", font=("Courier", 35), command=desttab1).grid(rowspan=5,column=0, row=10, sticky=N)
    

    Label(destinations, text="Presentations", underline =True).grid(column=2, columnspan = 2, row=16, sticky=S)
    Label(destinations, text=".pptx").grid(column=3, row=17, sticky=W)
    Label(destinations, text=".ppt").grid(column=3, row=18, sticky=W)
    Label(destinations, text=".pps").grid(column=3, row=19, sticky=W)
    Label(destinations, text=".odp").grid(column=3, row=20, sticky=W)
    Label(destinations, text=".key").grid(column=3, row=21, sticky=W)
    Label(destinations, text="").grid(column=2, row=23, sticky=W)


    #Entrys 3rd column
    d41 = Entry(destinations, width = 30)
    d41.grid(column=4, row=1, sticky=W)
    d42 = Entry(destinations, width = 30)
    d42.grid(column=4, row=2, sticky=W)
    d43 = Entry(destinations, width = 30)
    d43.grid(column=4, row=3, sticky=W)
    d44 = Entry(destinations, width = 30)
    d44.grid(column=4, row=4, sticky=W)
    d45 = Entry(destinations, width = 30)
    d45.grid(column=4, row=5, sticky=W)
    d46 = Entry(destinations, width = 30)
    d46.grid(column=4, row=6, sticky=W)
    d47 = Entry(destinations, width = 30)
    d47.grid(column=4, row=7, sticky=W)
    d48 = Entry(destinations, width = 30)
    d48.grid(column=4, row=8, sticky=W)
    d49 = Entry(destinations, width = 30)
    d49.grid(column=4, row=9, sticky=W) 
    d50 = Entry(destinations, width = 30)
    d50.grid(column=4, row=10, sticky=W)    
    d51 = Entry(destinations, width = 30)
    d51.grid(column=4, row=11, sticky=W)   
    d52 = Entry(destinations, width = 30)
    d52.grid(column=4, row=12, sticky=W)
    d53 = Entry(destinations, width = 30)
    d53.grid(column=4, row=13, sticky=W)
    d54 = Entry(destinations, width = 30)
    d54.grid(column=4, row=14, sticky=W)
    d55 = Entry(destinations, width = 30)
    d55.grid(column=4, row=15, sticky=W) 
    d56 = Entry(destinations, width = 30)
    d56.grid(column=4, row=17, sticky=W)
    d57 = Entry(destinations, width = 30)
    d57.grid(column=4, row=18, sticky=W) 
    d58 = Entry(destinations, width = 30)
    d58.grid(column=4, row=19, sticky=W)  
    d59 = Entry(destinations, width = 30)
    d59.grid(column=4, row=20, sticky=W)    
    d60 = Entry(destinations, width = 30)
    d60.grid(column=4, row=21, sticky=W)


    #Values 3rd column
    d41.insert(0,cfglisted[41])
    d42.insert(0,cfglisted[42])
    d43.insert(0,cfglisted[43])
    d44.insert(0,cfglisted[44])
    d45.insert(0,cfglisted[45])
    d46.insert(0,cfglisted[46])
    d47.insert(0,cfglisted[47])
    d48.insert(0,cfglisted[48])
    d49.insert(0,cfglisted[49])
    d50.insert(0,cfglisted[50])
    d51.insert(0,cfglisted[51])
    d52.insert(0,cfglisted[52])
    d53.insert(0,cfglisted[53])
    d54.insert(0,cfglisted[54])
    d55.insert(0,cfglisted[55])
    d56.insert(0,cfglisted[56])
    d57.insert(0,cfglisted[57])
    d58.insert(0,cfglisted[58])
    d59.insert(0,cfglisted[59])
    d60.insert(0,cfglisted[60])

    #Buttons 3rd column
    Label(destinations, text="").grid(column=5, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(41, d41)).grid(column=6, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(42, d42)).grid(column=6, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(43, d43)).grid(column=6, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(44, d44)).grid(column=6, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(45, d45)).grid(column=6, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(46, d46)).grid(column=6, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(47, d47)).grid(column=6, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(48, d48)).grid(column=6, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(49, d49)).grid(column=6, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(50, d50)).grid(column=6, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(51, d51)).grid(column=6, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(52, d52)).grid(column=6, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(53, d53)).grid(column=6, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(54, d54)).grid(column=6, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(55, d55)).grid(column=6, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(56, d56)).grid(column=6, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(57, d57)).grid(column=6, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(58, d58)).grid(column=6, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(59, d59)).grid(column=6, row=20, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(60, d60)).grid(column=6, row=21, sticky=W)
    

    #Labels 4th column
    Label(destinations, text="--------", fg='SystemButtonFace').grid(column=7, row=1, sticky=W)
    Label(destinations, text="Text", underline =True).grid(column=8, columnspan = 2, row=0, sticky=W)
    Label(destinations, text=".docx").grid(column=9, row=1, sticky=W)
    Label(destinations, text=".doc").grid(column=9, row=2, sticky=W)
    Label(destinations, text=".pdf").grid(column=9, row=3, sticky=W)
    Label(destinations, text=".txt").grid(column=9, row=4, sticky=W)
    Label(destinations, text=".odt").grid(column=9, row=5, sticky=W)
    Label(destinations, text=".rtf").grid(column=9, row=6, sticky=W)
    Label(destinations, text=".tex").grid(column=9, row=7, sticky=W)
    Label(destinations, text=".wks").grid(column=9, row=8, sticky=W)
    Label(destinations, text=".wps").grid(column=9, row=9, sticky=W)
    Label(destinations, text=".wpd").grid(column=9, row=10, sticky=W)

    Button(destinations, text=">", font=("Courier", 35), command=desttab3).grid(rowspan=5,column=13, row=9, sticky=E)

    Label(destinations, text="Programming", underline =True).grid(column=8, columnspan = 2, row=11, sticky=S)
    Label(destinations, text=".py").grid(column=9, row=12, sticky=W)
    Label(destinations, text=".c").grid(column=9, row=13, sticky=W)
    Label(destinations, text=".class").grid(column=9, row=14, sticky=W)
    Label(destinations, text=".dart").grid(column=9, row=15, sticky=W)
    Label(destinations, text=".swift").grid(column=9, row=16, sticky=W)
    Label(destinations, text=".sh").grid(column=9, row=17, sticky=W)
    Label(destinations, text=".html").grid(column=9, row=18, sticky=W)
    Label(destinations, text=".h").grid(column=9, row=19, sticky=W)


    #Entrys 4th column
    d61 = Entry(destinations, width = 30)
    d61.grid(column=10, row=1, sticky=W)
    d62 = Entry(destinations, width = 30)
    d62.grid(column=10, row=2, sticky=W)
    d63 = Entry(destinations, width = 30)
    d63.grid(column=10, row=3, sticky=W)
    d64 = Entry(destinations, width = 30)
    d64.grid(column=10, row=4, sticky=W)
    d65 = Entry(destinations, width = 30)
    d65.grid(column=10, row=5, sticky=W)
    d66 = Entry(destinations, width = 30)
    d66.grid(column=10, row=6, sticky=W)
    d67 = Entry(destinations, width = 30)
    d67.grid(column=10, row=7, sticky=W)
    d68 = Entry(destinations, width = 30)
    d68.grid(column=10, row=8, sticky=W)
    d69 = Entry(destinations, width = 30)
    d69.grid(column=10, row=9, sticky=W) 
    d70 = Entry(destinations, width = 30)
    d70.grid(column=10, row=10, sticky=W)    
    d71 = Entry(destinations, width = 30)
    d71.grid(column=10, row=12, sticky=W)   
    d72 = Entry(destinations, width = 30)
    d72.grid(column=10, row=13, sticky=W)
    d73 = Entry(destinations, width = 30)
    d73.grid(column=10, row=14, sticky=W)
    d74 = Entry(destinations, width = 30)
    d74.grid(column=10, row=15, sticky=W)
    d75 = Entry(destinations, width = 30)
    d75.grid(column=10, row=16, sticky=W) 
    d76 = Entry(destinations, width = 30)
    d76.grid(column=10, row=17, sticky=W)
    d77 = Entry(destinations, width = 30)
    d77.grid(column=10, row=18, sticky=W) 
    d78 = Entry(destinations, width = 30)
    d78.grid(column=10, row=19, sticky=W)      



    #Values 4th column
    d61.insert(0,cfglisted[61])
    d62.insert(0,cfglisted[62])
    d63.insert(0,cfglisted[63])
    d64.insert(0,cfglisted[64])
    d65.insert(0,cfglisted[65])
    d66.insert(0,cfglisted[66])
    d67.insert(0,cfglisted[67])
    d68.insert(0,cfglisted[68])
    d69.insert(0,cfglisted[69])
    d70.insert(0,cfglisted[70])
    d71.insert(0,cfglisted[71])
    d72.insert(0,cfglisted[72])
    d73.insert(0,cfglisted[73])
    d74.insert(0,cfglisted[74])
    d75.insert(0,cfglisted[75])
    d76.insert(0,cfglisted[76])
    d77.insert(0,cfglisted[77])
    d78.insert(0,cfglisted[78])


    #Buttons 4th column
    Label(destinations, text="").grid(column=11, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(61, d61)).grid(column=12, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(62, d62)).grid(column=12, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(63, d63)).grid(column=12, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(64, d64)).grid(column=12, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(65, d65)).grid(column=12, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(66, d66)).grid(column=12, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(67, d67)).grid(column=12, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(68, d68)).grid(column=12, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(69, d69)).grid(column=12, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(70, d70)).grid(column=12, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(71, d71)).grid(column=12, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(72, d72)).grid(column=12, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(73, d73)).grid(column=12, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(74, d74)).grid(column=12, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(75, d75)).grid(column=12, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(76, d76)).grid(column=12, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(77, d77)).grid(column=12, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(78, d78)).grid(column=12, row=19, sticky=W)

def desttab1():
    global destinations
    clear()


    #Labels 1st column
    Label(destinations, text="1/4").grid(column=0, row=0, sticky=W)
    Label(destinations, text="").grid(column=0, row=1, sticky=W)
    Label(destinations, text="").grid(column=1, row=1, sticky=W)

    
    Label(destinations, text="Audio", underline =True).grid(column=2, columnspan = 2, row=0, sticky=W)
    Label(destinations, text=".mp3").grid(column=3, row=1, sticky=W)
    Label(destinations, text=".wav").grid(column=3, row=2, sticky=W)
    Label(destinations, text=".ogg").grid(column=3, row=3, sticky=W)
    Label(destinations, text=".midi").grid(column=3, row=4, sticky=W)
    Label(destinations, text=".aif").grid(column=3, row=5, sticky=W)
    Label(destinations, text=".cda").grid(column=3, row=6, sticky=W)
    Label(destinations, text=".mid").grid(column=3, row=7, sticky=W)
    Label(destinations, text=".mpa").grid(column=3, row=8, sticky=W)
    Label(destinations, text=".wma").grid(column=3, row=9, sticky=W)
    Label(destinations, text=".wpl").grid(column=3, row=10, sticky=W)
    Label(destinations, text=".m3u").grid(column=3, row=11, sticky=W)

    Label(destinations, text="<", width=2, font=("Courier", 35), fg='SystemButtonFace').grid(rowspan=2,column=0, row=10, sticky=N)

    Label(destinations, text="Compressed", underline =True).grid(column=2, columnspan = 2, row=12, sticky=S)
    Label(destinations, text=".zip").grid(column=3, row=13, sticky=W)
    Label(destinations, text=".rar").grid(column=3, row=14, sticky=W)
    Label(destinations, text=".z").grid(column=3, row=15, sticky=W)
    Label(destinations, text=".7z").grid(column=3, row=16, sticky=W)
    Label(destinations, text=".arj").grid(column=3, row=17, sticky=W)
    Label(destinations, text=".deb").grid(column=3, row=18, sticky=W)
    Label(destinations, text=".pkg").grid(column=3, row=19, sticky=W)
    Label(destinations, text=".rpm").grid(column=3, row=20, sticky=W)
    Label(destinations, text=".tar.gz").grid(column=3, row=21, sticky=W)
    Label(destinations, text="").grid(column=2, row=23, sticky=W)

    #Entrys 1st column
    d1 = Entry(destinations, width = 30)
    d1.grid(column=4, row=1, sticky=W)
    d2 = Entry(destinations, width = 30)
    d2.grid(column=4, row=2, sticky=W)
    d3 = Entry(destinations, width = 30)
    d3.grid(column=4, row=3, sticky=W)
    d4 = Entry(destinations, width = 30)
    d4.grid(column=4, row=4, sticky=W)
    d5 = Entry(destinations, width = 30)
    d5.grid(column=4, row=5, sticky=W)
    d6 = Entry(destinations, width = 30)
    d6.grid(column=4, row=6, sticky=W)
    d7 = Entry(destinations, width = 30)
    d7.grid(column=4, row=7, sticky=W)
    d8 = Entry(destinations, width = 30)
    d8.grid(column=4, row=8, sticky=W)
    d9 = Entry(destinations, width = 30)
    d9.grid(column=4, row=9, sticky=W) 
    d10 = Entry(destinations, width = 30)
    d10.grid(column=4, row=10, sticky=W)    
    d11 = Entry(destinations, width = 30)
    d11.grid(column=4, row=11, sticky=W)   
    d12 = Entry(destinations, width = 30)
    d12.grid(column=4, row=13, sticky=W)
    d13 = Entry(destinations, width = 30)
    d13.grid(column=4, row=14, sticky=W)
    d14 = Entry(destinations, width = 30)
    d14.grid(column=4, row=15, sticky=W)
    d15 = Entry(destinations, width = 30)
    d15.grid(column=4, row=16, sticky=W) 
    d16 = Entry(destinations, width = 30)
    d16.grid(column=4, row=17, sticky=W)
    d17 = Entry(destinations, width = 30)
    d17.grid(column=4, row=18, sticky=W) 
    d18 = Entry(destinations, width = 30)
    d18.grid(column=4, row=19, sticky=W)  
    d19 = Entry(destinations, width = 30)
    d19.grid(column=4, row=20, sticky=W)    
    d20 = Entry(destinations, width = 30)
    d20.grid(column=4, row=21, sticky=W)    
        
    #Values 1st column
    d1.insert(0,cfglisted[1])
    d2.insert(0,cfglisted[2])
    d3.insert(0,cfglisted[3])
    d4.insert(0,cfglisted[4])
    d5.insert(0,cfglisted[5])
    d6.insert(0,cfglisted[6])
    d7.insert(0,cfglisted[7])
    d8.insert(0,cfglisted[8])
    d9.insert(0,cfglisted[9])
    d10.insert(0,cfglisted[10])
    d11.insert(0,cfglisted[11])
    d12.insert(0,cfglisted[12])
    d13.insert(0,cfglisted[13])
    d14.insert(0,cfglisted[14])
    d15.insert(0,cfglisted[15])
    d16.insert(0,cfglisted[16])
    d17.insert(0,cfglisted[17])
    d18.insert(0,cfglisted[18])
    d19.insert(0,cfglisted[19])
    d20.insert(0,cfglisted[20])

    #Buttons 1st column
    Label(destinations, text="").grid(column=5, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(1, d1)).grid(column=6, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(2, d2)).grid(column=6, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(3, d3)).grid(column=6, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(4, d4)).grid(column=6, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(5, d5)).grid(column=6, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(6, d6)).grid(column=6, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(7, d7)).grid(column=6, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(8, d8)).grid(column=6, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(9, d9)).grid(column=6, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(10, d10)).grid(column=6, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(11, d11)).grid(column=6, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(12, d12)).grid(column=6, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(13, d13)).grid(column=6, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(14, d14)).grid(column=6, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(15, d15)).grid(column=6, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(16, d16)).grid(column=6, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(17, d17)).grid(column=6, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(18, d18)).grid(column=6, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(19, d19)).grid(column=6, row=20, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(20, d20)).grid(column=6, row=21, sticky=W)




    #Labels 2nd column
    Label(destinations, text="--------", fg='SystemButtonFace').grid(column=7, row=1, sticky=W)
    Label(destinations, text="Images", underline =True).grid(column=8, row=0, sticky=W)
    Label(destinations, text=".jpg").grid(column=9, row=1, sticky=W)
    Label(destinations, text=".jpeg").grid(column=9, row=2, sticky=W)
    Label(destinations, text=".png").grid(column=9, row=3, sticky=W)
    Label(destinations, text=".gif").grid(column=9, row=4, sticky=W)
    Label(destinations, text=".ico").grid(column=9, row=5, sticky=W)
    Label(destinations, text=".svg").grid(column=9, row=6, sticky=W)
    Label(destinations, text=".ps").grid(column=9, row=7, sticky=W)
    Label(destinations, text=".psd").grid(column=9, row=8, sticky=W)
    Label(destinations, text=".ai").grid(column=9, row=9, sticky=W)
    Label(destinations, text=".bmp").grid(column=9, row=10, sticky=W)
    Label(destinations, text=".tif").grid(column=9, row=11, sticky=W)
    Label(destinations, text=".tiff").grid(column=9, row=12, sticky=W)
    Label(destinations, text=".CR2").grid(column=9, row=13, sticky=W)

    Button(destinations, text=">", font=("Courier", 35), command=desttab2).grid(rowspan=5,column=13, row=9, sticky=E)

    Label(destinations, text="Executables", underline =True).grid(column=8, columnspan = 2, row=14, sticky=S)
    Label(destinations, text=".exe").grid(column=9, row=15, sticky=W)
    Label(destinations, text=".com").grid(column=9, row=16, sticky=W)
    Label(destinations, text=".bat").grid(column=9, row=17, sticky=W)
    Label(destinations, text=".apk").grid(column=9, row=18, sticky=W)
    Label(destinations, text=".gadget").grid(column=9, row=19, sticky=W)
    Label(destinations, text=".jar").grid(column=9, row=20, sticky=W)
    Label(destinations, text=".wsf").grid(column=9, row=21, sticky=W)


    #Entrys 2nd column
    d21 = Entry(destinations, width = 30)
    d21.grid(column=10, row=1, sticky=W)
    d22 = Entry(destinations, width = 30)
    d22.grid(column=10, row=2, sticky=W)
    d23 = Entry(destinations, width = 30)
    d23.grid(column=10, row=3, sticky=W)
    d24 = Entry(destinations, width = 30)
    d24.grid(column=10, row=4, sticky=W)
    d25 = Entry(destinations, width = 30)
    d25.grid(column=10, row=5, sticky=W)
    d26 = Entry(destinations, width = 30)
    d26.grid(column=10, row=6, sticky=W)
    d27 = Entry(destinations, width = 30)
    d27.grid(column=10, row=7, sticky=W)
    d28 = Entry(destinations, width = 30)
    d28.grid(column=10, row=8, sticky=W)
    d29 = Entry(destinations, width = 30)
    d29.grid(column=10, row=9, sticky=W) 
    d30 = Entry(destinations, width = 30)
    d30.grid(column=10, row=10, sticky=W)    
    d31 = Entry(destinations, width = 30)
    d31.grid(column=10, row=11, sticky=W)   
    d32 = Entry(destinations, width = 30)
    d32.grid(column=10, row=12, sticky=W)
    d33 = Entry(destinations, width = 30)
    d33.grid(column=10, row=13, sticky=W)
    d34 = Entry(destinations, width = 30)
    d34.grid(column=10, row=15, sticky=W)
    d35 = Entry(destinations, width = 30)
    d35.grid(column=10, row=16, sticky=W) 
    d36 = Entry(destinations, width = 30)
    d36.grid(column=10, row=17, sticky=W)
    d37 = Entry(destinations, width = 30)
    d37.grid(column=10, row=18, sticky=W) 
    d38 = Entry(destinations, width = 30)
    d38.grid(column=10, row=19, sticky=W)  
    d39 = Entry(destinations, width = 30)
    d39.grid(column=10, row=20, sticky=W)    
    d40 = Entry(destinations, width = 30)
    d40.grid(column=10, row=21, sticky=W)



    #Values 2nd column
    d21.insert(0,cfglisted[21])
    d22.insert(0,cfglisted[22])
    d23.insert(0,cfglisted[23])
    d24.insert(0,cfglisted[24])
    d25.insert(0,cfglisted[25])
    d26.insert(0,cfglisted[26])
    d27.insert(0,cfglisted[27])
    d28.insert(0,cfglisted[28])
    d29.insert(0,cfglisted[29])
    d30.insert(0,cfglisted[30])
    d31.insert(0,cfglisted[31])
    d32.insert(0,cfglisted[32])
    d33.insert(0,cfglisted[33])
    d34.insert(0,cfglisted[34])
    d35.insert(0,cfglisted[35])
    d36.insert(0,cfglisted[36])
    d37.insert(0,cfglisted[37])
    d38.insert(0,cfglisted[38])
    d39.insert(0,cfglisted[39])
    d40.insert(0,cfglisted[40])


    #Buttons 2nd column
    Label(destinations, text="").grid(column=11, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(21, d21)).grid(column=12, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(22, d22)).grid(column=12, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(23, d23)).grid(column=12, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(24, d24)).grid(column=12, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(25, d25)).grid(column=12, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(26, d26)).grid(column=12, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(27, d27)).grid(column=12, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(28, d28)).grid(column=12, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(29, d29)).grid(column=12, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(30, d30)).grid(column=12, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(31, d31)).grid(column=12, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(32, d32)).grid(column=12, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(33, d33)).grid(column=12, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(34, d34)).grid(column=12, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(35, d35)).grid(column=12, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(36, d36)).grid(column=12, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(37, d37)).grid(column=12, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(38, d38)).grid(column=12, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(39, d39)).grid(column=12, row=20, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(40, d40)).grid(column=12, row=21, sticky=W)

def desttab3():
    global destinations
    clear()

    #Labels 5th column
    Label(destinations, text="3/4").grid(column=0, row=0, sticky=W)
    Label(destinations, text="System", underline =True).grid(column=2, columnspan = 2, row=0, sticky=W)
    Label(destinations, text=".tmp").grid(column=3, row=1, sticky=W)
    Label(destinations, text=".sys").grid(column=3, row=2, sticky=W)
    Label(destinations, text=".lnk").grid(column=3, row=3, sticky=W)
    Label(destinations, text=".msi").grid(column=3, row=4, sticky=W)
    Label(destinations, text=".ico").grid(column=3, row=5, sticky=W)
    Label(destinations, text=".icns").grid(column=3, row=6, sticky=W)
    Label(destinations, text=".bak").grid(column=3, row=7, sticky=W)
    Label(destinations, text=".cab").grid(column=3, row=8, sticky=W)
    Label(destinations, text=".dmp").grid(column=3, row=9, sticky=W)
    Label(destinations, text=".cfg").grid(column=3, row=10, sticky=W)
    Label(destinations, text=".cpl").grid(column=3, row=11, sticky=W)
    Label(destinations, text=".cur").grid(column=3, row=12, sticky=W)
    Label(destinations, text=".dll").grid(column=3, row=13, sticky=W)
    Label(destinations, text=".drv").grid(column=3, row=14, sticky=W)
    Label(destinations, text=".ini").grid(column=3, row=15, sticky=W)

    Button(destinations, text="<", font=("Courier", 35), command=desttab2).grid(rowspan=5,column=0, row=10, sticky=N)
    

    Label(destinations, text="Spreadsheets", underline =True).grid(column=2, columnspan = 2, row=16, sticky=S)
    Label(destinations, text=".xlsx").grid(column=3, row=17, sticky=W)
    Label(destinations, text=".xls").grid(column=3, row=18, sticky=W)
    Label(destinations, text=".xlr").grid(column=3, row=19, sticky=W)
    Label(destinations, text=".od").grid(column=3, row=20, sticky=W)
    Label(destinations, text="").grid(column=2, row=23, sticky=W)


    #Entrys 5th column
    d79 = Entry(destinations, width = 30)
    d79.grid(column=4, row=1, sticky=W)
    d80 = Entry(destinations, width = 30)
    d80.grid(column=4, row=2, sticky=W)
    d81 = Entry(destinations, width = 30)
    d81.grid(column=4, row=3, sticky=W)
    d82 = Entry(destinations, width = 30)
    d82.grid(column=4, row=4, sticky=W)
    d83 = Entry(destinations, width = 30)
    d83.grid(column=4, row=5, sticky=W)
    d84 = Entry(destinations, width = 30)
    d84.grid(column=4, row=6, sticky=W)
    d85 = Entry(destinations, width = 30)
    d85.grid(column=4, row=7, sticky=W)
    d86 = Entry(destinations, width = 30)
    d86.grid(column=4, row=8, sticky=W)
    d87 = Entry(destinations, width = 30)
    d87.grid(column=4, row=9, sticky=W) 
    d88 = Entry(destinations, width = 30)
    d88.grid(column=4, row=10, sticky=W)    
    d89 = Entry(destinations, width = 30)
    d89.grid(column=4, row=11, sticky=W)   
    d90 = Entry(destinations, width = 30)
    d90.grid(column=4, row=12, sticky=W)
    d91 = Entry(destinations, width = 30)
    d91.grid(column=4, row=13, sticky=W)
    d92 = Entry(destinations, width = 30)
    d92.grid(column=4, row=14, sticky=W)
    d93 = Entry(destinations, width = 30)
    d93.grid(column=4, row=15, sticky=W) 
    d94 = Entry(destinations, width = 30)
    d94.grid(column=4, row=17, sticky=W)
    d95 = Entry(destinations, width = 30)
    d95.grid(column=4, row=18, sticky=W) 
    d96 = Entry(destinations, width = 30)
    d96.grid(column=4, row=19, sticky=W)  
    d97 = Entry(destinations, width = 30)
    d97.grid(column=4, row=20, sticky=W)    


    #Values 5th column
    d79.insert(0,cfglisted[79])
    d80.insert(0,cfglisted[80])
    d81.insert(0,cfglisted[81])
    d82.insert(0,cfglisted[82])
    d83.insert(0,cfglisted[83])
    d84.insert(0,cfglisted[84])
    d85.insert(0,cfglisted[85])
    d86.insert(0,cfglisted[86])
    d87.insert(0,cfglisted[87])
    d88.insert(0,cfglisted[88])
    d89.insert(0,cfglisted[89])
    d90.insert(0,cfglisted[90])
    d91.insert(0,cfglisted[91])
    d92.insert(0,cfglisted[92])
    d93.insert(0,cfglisted[93])
    d94.insert(0,cfglisted[94])
    d95.insert(0,cfglisted[95])
    d96.insert(0,cfglisted[96])
    d97.insert(0,cfglisted[97])

    #Buttons 5th column
    Label(destinations, text="").grid(column=5, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(79, d79)).grid(column=6, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(80, d80)).grid(column=6, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(81, d81)).grid(column=6, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(82, d82)).grid(column=6, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(83, d83)).grid(column=6, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(84, d84)).grid(column=6, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(85, d85)).grid(column=6, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(86, d86)).grid(column=6, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(87, d87)).grid(column=6, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(88, d88)).grid(column=6, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(89, d89)).grid(column=6, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(90, d90)).grid(column=6, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(91, d91)).grid(column=6, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(92, d92)).grid(column=6, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(93, d93)).grid(column=6, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(94, d94)).grid(column=6, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(95, d95)).grid(column=6, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(96, d96)).grid(column=6, row=19, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(97, d97)).grid(column=6, row=20, sticky=W)



    #Labels 6th column
    Label(destinations, text="--------", fg='SystemButtonFace').grid(column=7, row=1, sticky=W)
    Label(destinations, text="Internet", underline =True).grid(column=8, columnspan = 1, row=0, sticky=W)
    Label(destinations, text=".asp").grid(column=9, row=1, sticky=W)
    Label(destinations, text=".aspx").grid(column=9, row=2, sticky=W)
    Label(destinations, text=".cer").grid(column=9, row=3, sticky=W)
    Label(destinations, text=".cfm").grid(column=9, row=4, sticky=W)
    Label(destinations, text=".cgi").grid(column=9, row=5, sticky=W)
    Label(destinations, text=".pl").grid(column=9, row=6, sticky=W)
    Label(destinations, text=".css").grid(column=9, row=7, sticky=W)
    Label(destinations, text=".htm").grid(column=9, row=8, sticky=W)
    Label(destinations, text=".js").grid(column=9, row=9, sticky=W)
    Label(destinations, text=".jsp").grid(column=9, row=10, sticky=W)
    Label(destinations, text=".part").grid(column=9, row=11, sticky=W)
    Label(destinations, text=".php").grid(column=9, row=12, sticky=W)
    Label(destinations, text=".rss").grid(column=9, row=13, sticky=W)
    Label(destinations, text=".xhtml").grid(column=9, row=14, sticky=W)

    Button(destinations, text=">", font=("Courier", 35), command=desttab4).grid(rowspan=5,column=13, row=9, sticky=E)

    Label(destinations, text="Fonts", underline =True).grid(column=8, columnspan = 2, row=15, sticky=S)
    Label(destinations, text=".fnt").grid(column=9, row=16, sticky=W)
    Label(destinations, text=".fon").grid(column=9, row=17, sticky=W)
    Label(destinations, text=".otf").grid(column=9, row=18, sticky=W)
    Label(destinations, text=".ttf").grid(column=9, row=19, sticky=W)


    #Entrys 6th column
    d98 = Entry(destinations, width = 30)
    d98.grid(column=10, row=1, sticky=W)
    d99 = Entry(destinations, width = 30)
    d99.grid(column=10, row=2, sticky=W)
    d100 = Entry(destinations, width = 30)
    d100.grid(column=10, row=3, sticky=W)
    d101 = Entry(destinations, width = 30)
    d101.grid(column=10, row=4, sticky=W)
    d102 = Entry(destinations, width = 30)
    d102.grid(column=10, row=5, sticky=W)
    d103 = Entry(destinations, width = 30)
    d103.grid(column=10, row=6, sticky=W)
    d104 = Entry(destinations, width = 30)
    d104.grid(column=10, row=7, sticky=W)
    d105 = Entry(destinations, width = 30)
    d105.grid(column=10, row=8, sticky=W)
    d106 = Entry(destinations, width = 30)
    d106.grid(column=10, row=9, sticky=W) 
    d107 = Entry(destinations, width = 30)
    d107.grid(column=10, row=10, sticky=W)    
    d108 = Entry(destinations, width = 30)
    d108.grid(column=10, row=11, sticky=W)   
    d109 = Entry(destinations, width = 30)
    d109.grid(column=10, row=12, sticky=W)
    d110 = Entry(destinations, width = 30)
    d110.grid(column=10, row=13, sticky=W)
    d111 = Entry(destinations, width = 30)
    d111.grid(column=10, row=14, sticky=W)
    d112 = Entry(destinations, width = 30)
    d112.grid(column=10, row=16, sticky=W) 
    d113 = Entry(destinations, width = 30)
    d113.grid(column=10, row=17, sticky=W)
    d114 = Entry(destinations, width = 30)
    d114.grid(column=10, row=18, sticky=W) 
    d115 = Entry(destinations, width = 30)
    d115.grid(column=10, row=19, sticky=W)   



    #Values 6th column
    d98.insert(0,cfglisted[98])
    d99.insert(0,cfglisted[99])
    d100.insert(0,cfglisted[100])
    d101.insert(0,cfglisted[101])
    d102.insert(0,cfglisted[102])
    d103.insert(0,cfglisted[103])
    d104.insert(0,cfglisted[104])
    d105.insert(0,cfglisted[105])
    d106.insert(0,cfglisted[106])
    d107.insert(0,cfglisted[107])
    d108.insert(0,cfglisted[108])
    d109.insert(0,cfglisted[109])
    d110.insert(0,cfglisted[110])
    d111.insert(0,cfglisted[111])
    d112.insert(0,cfglisted[112])
    d113.insert(0,cfglisted[113])
    d114.insert(0,cfglisted[114])
    d115.insert(0,cfglisted[115])


    #Buttons 6th column
    Label(destinations, text="").grid(column=11, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(98, d98)).grid(column=12, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(99, d99)).grid(column=12, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(100, d100)).grid(column=12, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(101, d101)).grid(column=12, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(102, d102)).grid(column=12, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(103, d103)).grid(column=12, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(104, d104)).grid(column=12, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(105, d105)).grid(column=12, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(106, d106)).grid(column=12, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(107, d107)).grid(column=12, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(108, d108)).grid(column=12, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(109, d109)).grid(column=12, row=12, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(110, d110)).grid(column=12, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(111, d111)).grid(column=12, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(112, d112)).grid(column=12, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(113, d113)).grid(column=12, row=17, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(114, d114)).grid(column=12, row=18, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(115, d115)).grid(column=12, row=19, sticky=W)
    

def desttab4():
    global destinations
    clear()



    #Labels 7th column
    Label(destinations, text="4/4").grid(column=0, row=0, sticky=W)
    Label(destinations, text="Data", underline =True).grid(column=2, columnspan = 1, row=0, sticky=W)
    Label(destinations, text=".csv").grid(column=3, row=1, sticky=W)
    Label(destinations, text=".dat").grid(column=3, row=2, sticky=W)
    Label(destinations, text=".db").grid(column=3, row=3, sticky=W)
    Label(destinations, text=".dbf").grid(column=3, row=4, sticky=W)
    Label(destinations, text=".log").grid(column=3, row=5, sticky=W)
    Label(destinations, text=".mdb").grid(column=3, row=6, sticky=W)
    Label(destinations, text=".sav").grid(column=3, row=7, sticky=W)
    Label(destinations, text=".sql").grid(column=3, row=8, sticky=W)
    Label(destinations, text=".tar").grid(column=3, row=9, sticky=W)
    Label(destinations, text=".xml").grid(column=3, row=10, sticky=W)
    Label(destinations, text=".json").grid(column=3, row=11, sticky=W)

    Button(destinations, text="<", font=("Courier", 35), command=desttab3).grid(rowspan=5,column=0, row=10, sticky=N)
    

    Label(destinations, text="Disc", underline =True).grid(column=2, columnspan = 1, row=12, sticky=S)
    Label(destinations, text=".bin").grid(column=3, row=13, sticky=W)
    Label(destinations, text=".dmg").grid(column=3, row=14, sticky=W)
    Label(destinations, text=".iso").grid(column=3, row=15, sticky=W)
    Label(destinations, text=".toast").grid(column=3, row=16, sticky=W)
    Label(destinations, text=".vcd").grid(column=3, row=17, sticky=W)
    Label(destinations, text="").grid(column=2, row=23, sticky=W)


    #Entrys 7th column
    d116 = Entry(destinations, width = 30)
    d116.grid(column=4, row=1, sticky=W)
    d117 = Entry(destinations, width = 30)
    d117.grid(column=4, row=2, sticky=W)
    d118 = Entry(destinations, width = 30)
    d118.grid(column=4, row=3, sticky=W)
    d119 = Entry(destinations, width = 30)
    d119.grid(column=4, row=4, sticky=W)
    d120 = Entry(destinations, width = 30)
    d120.grid(column=4, row=5, sticky=W)
    d121 = Entry(destinations, width = 30)
    d121.grid(column=4, row=6, sticky=W)
    d122 = Entry(destinations, width = 30)
    d122.grid(column=4, row=7, sticky=W)
    d123 = Entry(destinations, width = 30)
    d123.grid(column=4, row=8, sticky=W)
    d124 = Entry(destinations, width = 30)
    d124.grid(column=4, row=9, sticky=W) 
    d125 = Entry(destinations, width = 30)
    d125.grid(column=4, row=10, sticky=W)    
    d126 = Entry(destinations, width = 30)
    d126.grid(column=4, row=11, sticky=W)   
    d127 = Entry(destinations, width = 30)
    d127.grid(column=4, row=13, sticky=W)
    d128 = Entry(destinations, width = 30)
    d128.grid(column=4, row=14, sticky=W)
    d129 = Entry(destinations, width = 30)
    d129.grid(column=4, row=15, sticky=W)
    d130 = Entry(destinations, width = 30)
    d130.grid(column=4, row=16, sticky=W) 
    d131 = Entry(destinations, width = 30)
    d131.grid(column=4, row=17, sticky=W)


    
    #Values 7th column
    d116.insert(0,cfglisted[116])
    d117.insert(0,cfglisted[117])
    d118.insert(0,cfglisted[118])
    d119.insert(0,cfglisted[119])
    d120.insert(0,cfglisted[120])
    d121.insert(0,cfglisted[121])
    d122.insert(0,cfglisted[122])
    d123.insert(0,cfglisted[123])
    d124.insert(0,cfglisted[124])
    d125.insert(0,cfglisted[125])
    d126.insert(0,cfglisted[126])
    d127.insert(0,cfglisted[127])
    d128.insert(0,cfglisted[128])
    d129.insert(0,cfglisted[129])
    d130.insert(0,cfglisted[130])
    d131.insert(0,cfglisted[131])


    #Buttons 7th column
    Label(destinations, text="").grid(column=5, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(116, d116)).grid(column=6, row=1, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(117, d117)).grid(column=6, row=2, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(118, d118)).grid(column=6, row=3, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(119, d119)).grid(column=6, row=4, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(120, d120)).grid(column=6, row=5, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(121, d121)).grid(column=6, row=6, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(122, d122)).grid(column=6, row=7, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(123, d123)).grid(column=6, row=8, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(124, d124)).grid(column=6, row=9, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(125, d125)).grid(column=6, row=10, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(126, d126)).grid(column=6, row=11, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(127, d127)).grid(column=6, row=13, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(128, d128)).grid(column=6, row=14, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(129, d129)).grid(column=6, row=15, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(130, d130)).grid(column=6, row=16, sticky=W)
    Button(destinations, text="Zoek", command= lambda: verkenner(131, d131)).grid(column=6, row=17, sticky=W)
    


    

#Destination GUI
Button(window, text="Bewerk destination folders", command=destinationgui).grid(column=1, row=6, sticky=W)

window.mainloop()
