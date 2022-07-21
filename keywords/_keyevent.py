# -*- coding: utf-8 -*-

from .keywordgroup import KeywordGroup
import os, sys
import json
import time
keyIDFile = r'C:/ProgramData/AEUPTEST/autotest/keyidmap.json'
tsIDFile = r'C:/ProgramData/AEUPTEST/autotest/tsidmap.json'
os.popen('adb root')
os.popen('adb push ' + tsIDFile + ' /vendor/extools/etc')


class _KeyeventKeywords(KeywordGroup):
    def load_default(self):

        self.load(keyIDFile, tsIDFile)
        

    def load(self, keyidmapfile, tsidmapfile):

        #create a dict which maps hardkey name  to code
        p = keyidmapfile
        if os.path.exists(p):
            if sys.version_info.major < 3: 
                f = open(p, 'r')
            else:
                f = open(p, 'r', encoding = 'utf-8')

        self.key_dict = json.load(f)
        #print(self.key_dict)

        #create a dict which maps ts widgt name to code
        p = tsidmapfile
        if os.path.exists(p):
            if sys.version_info.major < 3:
                f = open(p, 'r')
            else:
                f = open(p, 'r', encoding = 'utf-8')
        dict = json.load(f)
        
        self.ts_dict = {}
        for key, value in dict.items():
            self.ts_dict[value["name"]] = key
        #print(self.ts_dict)
    # Public
    def press_keycode(self, keycode, metastate=None):
        """Sends a press of keycode to the device.

        Android only.

        Possible keycodes & meta states can be found in
        http://developer.android.com/reference/android/view/KeyEvent.html

        Meta state describe the pressed state of key modifiers such as
        Shift, Ctrl & Alt keys. The Meta State is an integer in which each
        bit set to 1 represents a pressed meta key.

        For example
        - META_SHIFT_ON = 1
        - META_ALT_ON = 2

        | metastate=1 --> Shift is pressed
        | metastate=2 --> Alt is pressed
        | metastate=3 --> Shift+Alt is pressed

         - _keycode- - the keycode to be sent to the device
         - _metastate- - status of the meta keys
        """
        driver = self._current_application()
        try:
            keycode = self.key_dict[str(keycode).lower()]
            driver.press_keycode(int(keycode), metastate)
        except:
            driver.press_keycode(int(keycode), metastate)

    def long_press_keycode(self, keycode, metastate=None):
        """Sends a long press of keycode to the device.

        Android only.

        See `press keycode` for more details.
        """
        driver = self._current_application()
        driver.long_press_keycode(int(keycode), metastate)

    def click_element_ts(self, name):     
        code = self.ts_dict[str(name).lower()]
        code = int(code, 16) 
        self.press_keycode(code, metastate=None)
       

    def set_element_ts_value(self, name, value=10):      
        code = self.ts_dict[str(name).lower()]
        code = int(code, 16) | value 
        
        self.press_keycode(code, metastate=None)

    def get_element_ts_value(self,name):
    	driver = self._current_application()
    	code = self.ts_dict[str(name).lower()]
    	code = int(code, 16)
    	driver.keyevent(str(code | 0x4000))

    	for num in (1, 3):
            text = driver.get_clipboard_text()
            value_dict = json.loads(text)
            print("====code2===="+str(value_dict))
            if(value_dict['code']==code):
                return value_dict['value']
            time.sleep(1)
        return -1

