# GUI client for ModernMT machine translation API

![Screenshot.png](Screenshot.png)

Note: You will need a paid subscription from [https://www.modernmt.com](https://www.modernmt.com) for this tool to work.

ModernMT API documentation can be found here:
[https://www.modernmt.com/api/](https://www.modernmt.com/api/)

Why did I create this tool? 2 Reasons:
1. I am learning Python.
2. As a technical translator, this is a useful tool for me to have a quick manual lookup tool in all languages that are relevant for me.

The tool is pretty much self-explanatory.

## Features:
* Translations are always copied to the clipboard 
* Easy to handle with keyboard (Alt-Enter for translate, Alt-C for clear)
* Source language recognition or manual setting 
* Shows quality estimation

### Saving your settings
* Source and target language settings (top line) can be stored in __settings.json__
* The API Key is stored in __api.json__

### Features I want to implement in future:
* MT adaptation: upload TMX files to improve the MT output
* Choose how much each TMX file influences the MT output (use of context vectors)
* Guessing of best context vector by MMT 
