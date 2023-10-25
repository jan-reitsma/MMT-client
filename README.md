# GUI client for ModernMT machine translation API

![Screenshot.png](Screenshot.png)

Note: You will need a paid subscription from [https://www.modernmt.com](https://www.modernmt.com) for this tool to work.

ModernMT API documentation can be found here:
[https://www.modernmt.com/api/](https://www.modernmt.com/api/)

Why did I create this tool? 2 Reasons:
1. I am improving my Python skills and decided to create a desktop GUI using the MVP (model - view - presenter) design principle.
2. As a technical translator, this could be even useful for easy lookup of machine translations on the desktop.

## Features:
* Translations are always copied to the clipboard 
* Easy to handle with keyboard (Alt-Enter for translate, Alt-C for clear)
* Source language is recognized or set manually, settings are saved 
* Shows quality estimation
* If no API key has been set, a dialog appears prompting you to enter your API key.

### Saving your settings
* Source and target language settings (top line) can be stored in __settings.json__
* The API Key is stored in __api.json__

### Features I might implement in future:
* MT adaptation: upload TMX files to improve the MT output
* Choose how much each TMX file influences the MT output (use of context vectors)
* Guessing of best context vector by MMT 
