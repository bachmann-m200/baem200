# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:14:04 2019

@author: neumann
"""
import json
import re
import os
import pprint

class MConfig():
    """module to create and handle ini-files"""
    def __init__(self):
        self._mconfig = {}
        self._mconfigStrg = ''
        self._PN_MODcount = 0
        self._PN_IOCRcount = 0

#     def __init__(self, filename):
#         if filename:
#             with open(filename, "r") as jsonfile:
#                 self._mconfig = json.load(jsonfile)
#         else:
#             self._mconfig = {}
        
    def addSection(self, sectionname):
        """add a section a the ini file\n
        example:
            from bae.mconfug import MConfig\n 
            myconfig = MConfig()\n
            myconfig.addSection('SectionName')
        """
        if not sectionname in self._mconfig:
            self._mconfig[sectionname] = {}

    def addGroup(self, sectionname, groupname):
        """add a group in a ini file"""
        self.addSection(sectionname)
        if not groupname in self._mconfig[sectionname]:
            self._mconfig[sectionname][groupname] = {}

    def addSet(self, sectionname, groupname, setname):
        self.addGroup(sectionname, groupname)
        if not setname in self._mconfig[sectionname][groupname]:
            self._mconfig[sectionname][groupname][setname] = {}

    def addUnit(self, sectionname, groupname, setname, unitname):
        self.addSet(sectionname, groupname, setname)
        if not unitname in self._mconfig[sectionname][groupname][setname]:
            self._mconfig[sectionname][groupname][setname][unitname] = {}

    def addKeyword(self, sectionname, groupname, keyword, value):
        self.addGroup(sectionname, groupname)
        self._mconfig[sectionname][groupname][keyword] = value
                
    def addKeywordExt(self, sectionname, groupname, setname, unitname, keyword, value):
        if unitname != '':
            self.addUnit(sectionname, groupname, setname, unitname)
            self._mconfig[sectionname][groupname][setname][unitname][keyword] = value
        else:
            self.addSet(sectionname, groupname, setname)
            self._mconfig[sectionname][groupname][setname][keyword] = value
        
    def changeValue(self, sectionname, groupname, keyword, value):
        self._mconfig[sectionname][groupname][keyword] = value


    def readMConfig(self, filename):
        regex = r"(\[\w*\.?\d?\])|(\(\w*\.?\d?\))|(\{\w*\.?\d?\})|(\|\w*\.?\d?\|)|(\w*)\s*=\s*(\"?[a-zA-Z0-9-_., \/]*\"?)"
        
        with open(filename) as mconfigfile:
            mconfigcontent = mconfigfile.read()
        
        matches = re.finditer(regex, mconfigcontent, re.MULTILINE)
        _section = ' '
        _group = ''
        _set = ''
        _unit = ''
        _keyword = ''
        _value = ''
        
        for matchNum, match in enumerate(matches, start=1):    
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                if groupNum == 1 and match.group(groupNum) != None:
                    _section = match.group(groupNum)
                    _group = ''
                    _set = ''
                    _unit = ''
                    _keyword = ''
                    _value = ''
                    
                if groupNum == 2 and match.group(groupNum) != None:
                    if match.group(groupNum).startswith('(PN_MOD'):
                        _group = str(self._PN_MODcount).zfill(2) + match.group(groupNum)
                        self._PN_MODcount+=1                        
                    elif match.group(groupNum).startswith('(PN_IOCR'):
                        _group = str(self._PN_IOCRcount).zfill(2) + match.group(groupNum)
                        self._PN_IOCRcount+=1                        
                    else:
                        _group = match.group(groupNum)
                    _set = ''
                    _unit = ''
                    _keyword = ''
                    _value = ''
        
                if groupNum == 3 and match.group(groupNum) != None:
                    _set = match.group(groupNum)
                    _unit = ''
                    _keyword = ''
                    _value = ''
        
                if groupNum == 4 and match.group(groupNum) != None:
                    _unit = match.group(groupNum)
                    _keyword = ''
                    _value = ''
        
                if groupNum == 5 and match.group(groupNum) != None:
                    _keyword = match.group(groupNum)
        
                if groupNum == 6 and match.group(groupNum) != None:
                    if _section != '' and _section not in self._mconfig:
                        self._mconfig[_section] = {}
                    if _group != '' and _group not in self._mconfig[_section]:
                        self._mconfig[_section][_group] = {}                        
                    if _set != '' and _set not in self._mconfig[_section][_group]:
                        self._mconfig[_section][_group][_set] = {}
                    if _unit != '' and _unit not in self._mconfig[_section][_group][_set]:
                        self._mconfig[_section][_group][_set][_unit] = {}
                    
                    _value = match.group(groupNum)
                    
                    if _section and _group and _set and _unit and _keyword:
                        self._mconfig[_section][_group][_set][_unit][_keyword] = _value
        
                    elif _section and _group and _set and _keyword:
                        self._mconfig[_section][_group][_set][_keyword] = _value
        
                    elif _section and _group and _keyword:
                        self._mconfig[_section][_group][_keyword] = _value
        
                else:
                    _value = ''

    def writeMConfig(self, filename, append=False):
        if os.path.isfile(filename) and append:
            with open(filename, 'a') as mconfigfile:
                mconfigfile.write(self.getMConfigStrg())            
        else:    
            with open(filename, 'w') as mconfigfile:
                mconfigfile.write(self.getMConfigStrg())


    def getMConfig(self):
        return json.dumps(self._mconfig, indent=4)
    
    
    def getMConfigStrg(self, data=None, indent=0, start=None):
        if data == None:
            data = self._mconfig            
        if start != None:
            data = self._mconfig[start]
        indent += 1
        try:
            for key in data.keys():
                if '[' in key or '(' in key or '{' in key or '|' in key or key ==' ' or key[:2].isdecimal():
                    if key[:2].isdecimal():
                        print(((indent-1)*4)*' ' + key[2:])
                        self._mconfigStrg += (((indent-1)*4)*' ' + key[2:] + '\n')
                    else:
                        print(((indent-1)*4)*' ' + key)
                        self._mconfigStrg += (((indent-1)*4)*' ' + key + '\n')
                else:

                    print(((indent-1)*4)*' ' + key + ' = ' + data[key])
                    self._mconfigStrg += (((indent-1)*4)*' ' + key + ' = ' + data[key] + '\n')
                
                self.getMConfigStrg(data[key], indent)
        except:
            pass
        return self._mconfigStrg
    
    
if __name__ == "__main__":
    inifile = MConfig()
    inifile.readMConfig('controller_empty.ini')
    print("controller_empty.ini**********")
    print(inifile.getMConfigStrg())
    
    inifile.readMConfig('controller_dev1.ini')
    print("controller_dev1.ini**********")
    print(inifile.getMConfigStrg())
    
    inifile.readMConfig('controller_aio208.ini')
    print("controller_aio208.ini**********")
    print(inifile.getMConfigStrg())
    
    inifile.readMConfig('controller_di216.ini')
    print("controller_di216.ini**********")

    inifile.writeMConfig('dev1.ini')
    
    
    pprint.pprint(inifile._mconfig)
    
    
