## ✨ Dominik WPM tesztje <sup>(kawaii & uwu certified)</sup>

### Futtatás
```bash
python3 -m pip install -R requirements.txt
```
...de ez amúgy full fölösleges, mert csak egy modul kell hozzá, szóval az is elég, hogy `python3 -m pip install --upgrade customtkinter`

<sup>azért nem használunk sima tkinter-t, mert az bűnronda</sup>

Töltsük le a Montserrat.ttf betűtípust is, ha lehet, mert az alap betűtípussal csúnya a GUI.

*A futtatáshoz MINIMUM Python 3.9 szükséges a .removesuffix beépített függvény miatt, ha kisebb a verzió, írd át arra, hogy `.replace("\r", "")`*

### 💻 A játék lényege
Majdnem az összes magyar szó le van írva a words.txt fájlban, és a játék onnan választ **5 random szót.** <sup>vagy szavat idk nem tudok ragozni</sup>
Neked le kell írnod az 5 szót, és a program hihetetlenül jó matematikával kiszámítja neked, hogy **mennyi a WPM-ed,** azaz words per minute-öd, azaz szó per perced. Ez igazából csak egy lehetőség arra, hogy flexelj a haverjaidnak, mekkora jó Discord mod vagy, és milyen gyorsan írsz.

⏰ **Az átlag WPM ~40,** ha annál több vagy, certified moderátor badge-et kapsz (de csak tiszteletbelit, mert már nem akartam beleírni a kódba, hogy kiírja, hogy certified moderátor vagy)

### 🔣 Speciális karakterek
Mivel a tkinter egy nagyon jó könyvtár (nem) és a Python minden nyelvre és szövegbevitelre odafigyel (szintén nem), nincsenek olyan szavak a words.txt-ben, amiben van **ő** vagy **ű** karakterek. Ez azért van, mert a tkinter a bemeneti mezőkben valami miatt automatikusan kicseréli az ő betűt õ-re, és az ű betűt û-re. Ezért imádok magyar lenni, a másik kedvencem, amikor nem írják bele az ő-t meg az ű-t a betűtípusokba, és amúgy a nagymamák meg azzal készítik a szülinapi meghívókat, és olyan jókat tudok nevetni rajta.
