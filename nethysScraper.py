#!python3
import json
import requests
from spellScraper import SpellParser

def fetchSpell(spellName):
    url = 'http://archivesofnethys.com/SpellDisplay.aspx?ItemName=%s' % spellName
    html = requests.get(url).text
    parser = SpellParser()
    result = parser.parseSpellHtml(html)
    with open('spells/%s.json' % result.name, 'w') as outfile:
        json.dump(result.toJson(), outfile, indent=4)

def tryme():
    aaa = requests.get('http://archivesofnethys.com/SpellDisplay.aspx?ItemName=Bleed')
    bbb = SpellParser()
    ccc = bbb.parseSpellHtml(aaa.text)
    return ccc

if __name__ == '__main__':
    aaa = tryme()
    aaa.consolePrint()
    
