#!python3
from html.parser import HTMLParser
from nethys import SpellItem

class SpellBuilder(object):
    delimitingTags = ['h1','h3','b']
    debugmode = False
    def __init__(self):
        self.spellCtx = SpellItem()
        self.setNameCallback = None
        self.setSectionCallback = None
        self.setValueCallback = None
        self.ctxSection = None
        self.ctxName = None
        self.ctxValue = None
        return

    def setCtxName(self, name):
        if self.debugmode:
            print('Context Name: "%s"' % name.strip())
        self.ctxName = name.strip()
        return

    def setCtxSection(self, section):
        trimmed = section.strip()
        if trimmed == 'Description':
            self.setValueCallback = self.setSpellDescription
        else:
            if self.debugmode:
                print('Context Section: "%s"' % trimmed)
            self.ctxSection = trimmed
        return

    def appendCtxValue(self, data):
        val = data
        if self.ctxValue is None:
            self.ctxValue = ''
            val = data.strip()
        self.ctxValue += val
        return

    def storeCurrentCtx(self):
        if self.ctxName is not None:
            currentSection = self.spellCtx.attrs
            if self.ctxSection is not None:
                if not self.spellCtx.attrs.__contains__(self.ctxSection):
                    self.spellCtx.attrs[self.ctxSection] = {}
                currentSection = self.spellCtx.attrs[self.ctxSection]
            currentSection[self.ctxName] = self.ctxValue
        self.ctxName = None
        self.ctxValue = None
        return

    def storeCurrentSectionCtx(self):
        self.storeCurrentCtx()
        self.ctxSection = None
        return

    def clearCallbacks(self):
        self.setNameCallback = None
        self.setSectionCallback = None
        self.setValueCallback = None
        return

    def processData(self, data):
        if self.setSectionCallback is not None:
            self.setSectionCallback(data)
            self.setSectionCallback = None
        elif self.setNameCallback is not None:
            self.setNameCallback(data)
        elif self.setValueCallback is not None:
            self.setValueCallback(data)
        else:
            if self.debugmode:
                print('Unhandled process data: %s' % data)
        return

    def startCtx(self, tag, classValue):
        if self.delimitingTags.__contains__(tag):
            self.clearCallbacks()
            if tag == 'h1' and classValue == 'title':
                self.setValueCallback = self.setSpellName
            elif tag == 'b':
                self.storeCurrentCtx()
                self.setNameCallback = self.setCtxName
                self.setValueCallback = self.appendCtxValue
            elif tag == 'h3' and classValue == 'framing':
                self.storeCurrentSectionCtx()
                self.setSectionCallback = self.setCtxSection
        return

    def endCtx(self, tag):
        if self.delimitingTags.__contains__(tag):
            if tag == 'b':
                self.setNameCallback = None
        return

    def setSpellName(self, data):
        trimmed = data.strip()
        if self.debugmode:
            print('Spell Name: "%s"' % trimmed)
        self.spellCtx.name = trimmed
        self.setValueCallback = None
        return

    def setSpellDescription(self, data):
        if self.debugmode:
            print('Spell Description: "%s"' % data)
        self.spellCtx.description = data
        self.setValueCallback = None
        return

    def getSpell(self):
        return self.spellCtx

class SpellParser(HTMLParser):
    spellCtx = None
    ignoreFeed = True

    def parseSpellHtml(self, html):
        if self.spellCtx is not None:
            raise 'Parser context already initialized.'
        self.ignoreFeed = True
        self.feed(html)
        result = self.spellCtx.getSpell()
        self.spellCtx = None
        return result

    def handle_starttag(self, tag, attrList):
        if self.ignoreFeed:
            if tag == 'table':
                self.beginContentTable()
            return
        attrs = self.getAttrs(attrList)
        classValue = attrs['class'] if attrs.__contains__('class') else None
        self.spellCtx.startCtx(tag, classValue)
        return

    def handle_endtag(self, tag):
        if not self.ignoreFeed:
            if tag == 'table':
                self.endContentTable()
            else:
                self.spellCtx.endCtx(tag)
        return

    def handle_data(self, data):
        if not self.ignoreFeed and len(data.strip()) > 0:
            self.spellCtx.processData(data)
        return

    def getAttrs(self, attrs):
        return {x:y for (x,y) in attrs}

    def endContentTable(self):
        self.ignoreFeed = True
        return

    def beginContentTable(self):
        self.spellCtx = SpellBuilder()
        self.ignoreFeed = False
        return

