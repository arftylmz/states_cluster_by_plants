from tkinter.ttk import Combobox, Style
import re
import recommendations
import clusters
from tkinter import *
from tkinter import filedialog
class Editor(Frame):

    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.root=parent
        self.initUI()

    def initUI(self):



        self.grid()
        self.harf_listesi=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","x","y","z"]
        frame = Frame(self,bg="Beige" , width = "800", height="700",pady = "25",padx="10")
        frame.grid()
        self.Baslik = Label(frame,text="Eyalet Kümeleme Sistemi", fg="Blue", bg="Beige")
        self.Baslik.config(font=("Courier", 18, "bold italic"))
        self.Baslik.grid(row=0, column = 0,columnspan = 7)

        self.Dosya_Sec = Label(frame,text="Bitki Veri Seti Yükle",fg="Blue", bg="Beige")
        self.Dosya_Sec.config(font=("Courier", 14, "bold italic"))
        self.Dosya_Sec.grid(row = 2,column = 0)
        self.button=Button(frame,text="Dosya Seç",fg="Blue",bg ="Gold",command=self.Dosya)
        self.button.grid(row = 2,column=4)

        self.harf_label = Label(frame,text="İlk harf seç",fg="Blue", bg="Beige")
        self.harf_label.config(font=("Courier", 14, "bold italic"))
        self.harf_label.grid(row = 4,column = 0,columnspan = 1)
        self.method = Label(frame, text="kümeleme methodu", fg="Blue", bg="Beige")
        self.method.config(font=("Courier", 14, "bold italic"))
        self.method.grid(row=4, column=3,columnspan = 3,padx="58")


        #######Listbox ve Scrollbar ######
        self.scroll=Scrollbar(frame,orient=VERTICAL,width =35)
        self.listbox = Listbox(frame,width =30 ,selectmode=MULTIPLE, fg="Blue", bg="Beige",yscrollcommand=self.scroll)
        self.listbox.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox.grid(row = 5, column =0,sticky=E)
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=5, column=1,sticky=N + S + W)
        for i in self.harf_listesi:
            self.listbox.insert(END,i)
        ###Radio Button#####
        self.kumeleme = IntVar()
        self.radio1=Radiobutton(frame,text="Hiyerarşik",value=0,variable=self.kumeleme, fg="Blue", bg="Beige")
        self.radio2=Radiobutton(frame,text="K - Means",value=1,variable=self.kumeleme, fg="Blue", bg="Beige")
        self.radio1.grid(row=5, column=3,sticky=N+S+E+W,padx = "30")
        self.radio2.grid(row=5, column=3,sticky=S,padx = "30")

        ###Textbox olucaturmak###
        self.text = Text(frame, font="Times 13" ,height=15,width=40,bg="Beige")
        self.text.grid(row = 8,column = 0,columnspan=6,sticky = W + E )
        self.text_scroll = Scrollbar(frame, orient=VERTICAL, width=35)
        self.text_scroll.config(command=self.text.yview)
        self.text_scroll.grid(row=8, column=7, sticky=N + S + W)
        self.text_scroll2 = Scrollbar(frame, orient=HORIZONTAL, width=35)
        self.text_scroll2.config(command=self.text.xview)
        self.text_scroll2.grid(row=9, column=0,columnspan = 6, sticky=W+E+N)

        self.button=Button(frame,text="Kümeleri Göster",fg="Blue",bg ="Gold",command=self.Goster)
        self.button.grid(row = 7,column=1)
        self.boslabel = Label(frame,text = "")
        self.boslabel.grid(row = 6,column = 0,columnspan = 6)

        self.sayi = IntVar()
        self.K_sayısı = Label(frame, text="K : ", fg="Blue", bg="Beige")
        self.K_sayısı.config(font=("Courier", 12, "bold italic"))
        self.K_sayısı.grid(row = 5,column = 4,sticky =S,padx ="10")
        self.Sayı_Entry = Entry(frame,textvariable = self.sayi,width = "5", fg="Blue", bg="Beige")
        self.Sayı_Entry.grid(row = 5,column =5,sticky =S+W)

    def matches(self,key, dic):
        if key in dic:
            return dic[key]
    def Dosya(self):
        self.filename = filedialog.askopenfilename(initialdir="/Desktop", title="Dosya Seç",
                                                      filetypes=(("Text Files", "*.txt"), ("all files", "*.*")))




    def onSelect(self,val):
        try:
            self.liste = ""
            idx = self.listbox.curselection()
            for i in idx:
                self.value = self.listbox.get(i)
                self.liste += self.value
            self.text.delete("1.0",END)
            self.text.insert(INSERT,self.liste)


        except:
            print("")

    def Goster(self):
        try:
            # Matrisimizi oluşturuyoruz...
            # Öncelikle kısaltmaları normal eyalet yapacağımız ve ana sözlüğümüzü oluşturuyoruz.
            self.sozluk = {}
            self.eyalet = {}
            file2 = open("stateabbr.txt", "r+")
            for line in file2:

                kısaltma = line.split()
                eyaletAdı = re.split("^[a-z]+", line)
                eyaletAdı[-1] = eyaletAdı[-1].strip()
                if (len(eyaletAdı) == 1):
                    continue
                else:
                    self.eyalet.setdefault(kısaltma[0], "")
                    self.eyalet[kısaltma[0]] = eyaletAdı[1]

            # yukarıda kısaltma:eyaletadı sözlüğü oluşturuldu

            file = open(self.filename, "r+")
            for line in file:
                bitkiler = line.split(",")
                bitkiler[-1] = bitkiler[-1].strip()
                eyaletler = bitkiler[1:]
                cemal = bitkiler[0]
                split = cemal.split()

                for i in eyaletler:
                    #Bir kısalta ("gl") matrisimize "dengl" olarak düşüyordu,çözüm içni bu if bloğu kullanıldı
                    if i == 'dengl':
                        eslesenKısaltma = self.matches('gl',self.eyalet)
                    else:
                        eslesenKısaltma = self.matches(i, self.eyalet)
                    # kısaltmayı eyalet sözlüğüne yolluyoruz o da bize doğru eyaleti geri döndürüyor.
                    self.sozluk.setdefault(split[0], {})
                    try:
                        regex = self.liste
                        match = re.match(('^' + regex), split[0])
                        if match:
                            self.sozluk[split[0]][eslesenKısaltma] = 1
                    except AttributeError:
                        self.sozluk[split[0]][eslesenKısaltma] = 1
            self.sozluk = recommendations.transformPrefs(self.sozluk)
            # Bundan sonrası matris oluşturma işlemi
            out_file = open("matris.txt", "w", encoding="UTF-8")
            out_file.write("Bitkiler")
            columnslist = []

            # create list of columns
            # önce kolonların listesini yazdırıyoruz,ilk satır kolonlardan oluşuyor zira
            for value in self.sozluk.values():
                for key in value:
                    if key not in columnslist:
                        columnslist.append(key)

            # write clolumns in columnlist to file
            for column in columnslist:
                out_file.write('\t%s' % column)
            out_file.write('\n')

            # convert dictionary to tuple list. The tuple is like that = [(tag,{url:value}]
            # şimdi keylerden bitkilerimizin isimleriniz yazdırıyoruz
            # Filtreleme işini burda yapabiliriz!!! regex burda yazılıcak keyler üzerinde harfe göre filtreleme yapmalı..
            for key, value in self.sozluk.items():
                out_file.write(key)
                out_file.write('\t')

                for column in columnslist:
                    # if url not in values,it equalize it value to 0 and write to file
                    # Bitkilerimizhangi eyaletteyse ona değerini diğer eyaletlere de 0 değerini yazdırıyoruz
                    if column not in value:
                        out_file.write('0\t')
                    else:
                        out_file.write(str(value[column]))
                        out_file.write('\t')
                out_file.write('\n')
            out_file.close()

            #--------------------------------------------------------------------------------------------------------------------------------
            # bundan sonra seçeceğimiz kümelemeye ve seçtiğimiz harflere göre kümeleme yapma işlemimiz var.


            karar  = self.kumeleme.get()
            if(karar == 0):
             # Kümeleme yapılan yer. h-cluster ile işlemlerimizi yapıyoruz.
                self.text.delete(1.0,END)
                blognames, words, data = clusters.readfile('matris.txt')
                clust = clusters.hcluster(data,distance = clusters.tanamoto)
                self.printclust(clust, labels=blognames)


            elif(karar == 1):

                #Kümeleme yapılan yer. k-means ile kümeleme yapıyoruz
                self.text.delete(1.0, END)
                blognames, words, data = clusters.readfile('matris.txt')
                kclust = clusters.kcluster(data,distance = clusters.tanamoto,k = int(self.sayi.get()))
                for r in kclust:
                    self.text.insert(INSERT,"\n ---centroid---\n")
                    for i in r:
                        self.text.insert(INSERT,"\n" + blognames[i] + "\n")
        except:
            self.text.delete(1.0,END)








        #Hiyerarşik kümelemede texte bastırma fonksiyonu
    def printclust(self,clust, labels=None, n=0):
        # indent to make a hierarchy layout
        for i in range(n): print(' ', end='')
        if clust.id < 0:
            # negative id means that this is branch
            self.text.insert(INSERT,'-\n')
        else:
            # positive id means that this is an endpoint
            if labels == None:
                self.text.insert(INSERT,"\t" + clust.id + "\n")
            else:
                self.text.insert(INSERT,"\t" + labels[clust.id] + "\n")

        # now print the right and left branches
        if clust.left != None: self.printclust(clust.left, labels=labels, n=n + 1)
        if clust.right != None: self.printclust(clust.right, labels=labels, n=n + 1)


















def main():
    root= Tk()
    root.title("Excel-Reader")
    root.geometry("650x650+300+100")
    #konumu ayarlıyoruz ve ekran boyut ayarlamasını kapatıyoruz.
    root.resizable(FALSE,FALSE)
    App = Editor(root)
    root.mainloop()



if __name__ == '__main__':
    main()
