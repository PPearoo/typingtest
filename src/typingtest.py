import time
import random
import customtkinter as tk
import threading as th

with open("src/words.txt", "r", encoding="utf-8") as f:
    words = f.read().split("\n")

class TypingGUI():
    def __init__(self):
        # Csinálunk egy ablakot és beállítjuk a nevét, ikonját és méretét, majd konfiguráljuk a rácsrendszert
        self.root = tk.CTk()
        self.root.title("ÍRJ A LEGGYORSABBAN!")
        self.root.iconbitmap("src/icon.ico")
        self.root.geometry("800x600")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        
        # A szavakat a words.txt fájlból kiolvassuk, majd összekeverjük őket (5 szó van!)
        random.shuffle(words)
        self.words = words[:5]
        
        # Beállítjuk a főcímet és az alcímet, a főcím vastag betűvel lesz megjelenítve
        self.label_title = tk.CTkLabel(master=self.root, text="ÍRJ A LEGGYORSABBAN!", font=tk.CTkFont("Montserrat", 30, weight="bold"))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.label_subtitle = tk.CTkLabel(master=self.root, text="Írd be hiba nélkül a szavakat a mezőbe!", font=("Montserrat", 16))
        self.label_subtitle.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Beállítjuk a szavakat megjelenítő "címkét", a szavakat egy szóközzel elválasztva jelenítjük meg
        self.label_words = tk.CTkLabel(master=self.root, text=" ".join(self.words), font=("Montserrat", 20))
        self.label_words.grid(row=2, column=0, columnspan=2, padx=10, pady=0)
        
        # Beállítjuk a bemeneti mezőt, aminek a szélessége a szavak hosszától függ (a szavak hosszúsága + 3, szorozva tízzel, hogy ne legyen túl szűk)
        self._input = tk.CTkEntry(master=self.root, width=(len(" ".join(self.words))+3)*10, font=tk.CTkFont("Montserrat", 16, weight="bold"), height=38, border_color="#1a1a1a", corner_radius=16, border_width=2)
        self._input.grid(row=3, column=0, padx=5, pady=5)
        
        # A .focus()-al az alkalmazás indításakor egyből a bementi mezőben írunk
        self._input.focus()
        
        # Ha megnyomunk egy gombot, elindul a játék
        self._input.bind("<KeyPress>", self.start)
        # Ha az entert nyomjuk meg, újragenerálja a szavakat
        self._input.bind("<Return>", self.reset)
        
        # Beállítjuk a WPM számláló címkét, ez egyelőre üres, de ha elkezdünk írni, akkor megjelenik a szöveg
        # Consolas betűtípust használunk, mert annak fix a szélessége, így nem fog elmozdulni a szöveg annyira
        self.label_speed = tk.CTkLabel(master=self.root, text="", font=("Consolas", 20))
        self.label_speed.grid(row=4, column=0, columnspan=2, padx=5, pady=0)
    
        # Beállítjuk a reset gombot, ami újragenerálja a szavakat
        self.resetBtn = tk.CTkButton(master=self.root, text="Újra", command=self.reset, font=tk.CTkFont("Montserrat", 12, weight="bold"), corner_radius=25)
        self.resetBtn.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        
        # Beállítjuk a szükséges belső változókat: counter az idő számlálásához, started a játék állapotához (True = megy, False = megállt)
        self.counter = 0
        self.started = False
        
        # Elindítjuk az alkalmazást
        self.root.mainloop()
    
    def start(self, event):
        # Csak akkor szeretnénk, hogy elinduljon a játék, ha még nem indult el
        if not self.started:
            self.started = True
            # Threadet használunk, hogy ne blokkolja a GUI-t
            # Ez kb. olyan, mintha egy külön műveletként indítanánk el valamit
            # Jelen esetben arra kell, hogy az időzítő, amit a time.sleep()-el csinálunk, ne akadályozza az írást,
            # Ugyanis a time.sleep az asyncio.sleep-el szemben az egész programot megvárattatja (az asyncio sleep egy külön folyamatban fut alapból)
            # Azért nem használunk asyncio-t, mert ahhoz async függvényt kell használni
            t = th.Thread(target=self.timeThread)
            t.start()
    
    def timeThread(self):
        # Az időzítőt csak addig szeretnénk futtatni, amíg a játék is fut
        while self.started:
            time.sleep(0.1)
            self.counter += 0.1
            # Minden millisecundumban frissítjük a WPM számlálót
            wpm = (len(self._input.get().split(" ")) / self.counter) * 60
            self.label_speed.configure(text=f"WPM\t{wpm:.2f}")
            # A :.2f azt jelenti, hogy két tizedesjegy pontossággal írja ki a számot
            # Hasonlít a round(int, 2)-höz, de ez kiírja azt is, ha nincs tizedesjegy (pl 5.00)
            
            # Ha helytelen a szöveg, amit beírtunk, a bemeneti mező háttere piros lesz. Ha újra helyes, akkor visszaáll feketére
            if not self.label_words.cget("text").startswith(self._input.get()):
                self._input.configure(fg_color="red")
            else:
                self._input.configure(fg_color="black")
            
            # Ha a szöveg megegyezik a bemeneti mező tartalmával, akkor a bemeneti mező háttere zöldre vált, jelezve, hogy helyesen csináltunk mindent
            # és a játék is megáll
            # Azért kell a removesuffix, mert a Windows valami miatt automatikusan hozzárak egy \r-t a végére.
            # A .removesuffix() függvény csak Python 3.9-től elérhető, ha az alatt van a verzió, egy egyszerű .replace("\r", "")-el is megoldható
            if self._input.get() == self.label_words.cget("text").removesuffix("\r"):
                self.started = False
                self._input.configure(fg_color="green")
    
    def reset(self, event=None):
        # Újraindításnál visszaállítunk mindent az eredeti állapotára
        self.started = False
        self.counter = 0
        self._input.configure(fg_color="black")
        self.label_speed.configure(text="")
        
        # Újrageneráljuk a szavakat
        random.shuffle(words)
        self.words = words[:5]
        random.shuffle(self.words)
        self.label_words.configure(text=" ".join(self.words))
        
        # Töröljük a bemeneti mező tartalmát
        self._input.delete(0, tk.END)

if __name__ == "__main__":
    # Ha ezt a fájlt futtatjuk, akkor elindítja az alkalmazást
    # (ha külső fájl futtatja, nem fog elindulni)
    TypingGUI()