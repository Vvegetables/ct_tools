import os
import re

PinyinToneMark = {
    0: u"aoeiuv\u00fc",
    1: u"\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: u"\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: u"\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: u"\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}


class Pinyin(object):

    """translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
    `chinese\_pinyin`_ gem
    usage
    -----
    ::
        >>> from xpinyin import Pinyin
        >>> p = Pinyin()
        >>> # default splitter is `-`
        >>> p.get_pinyin(u"上海")
        'shang-hai'
        >>> # show tone marks
        >>> p.get_pinyin(u"上海", tone_marks='marks')
        'shàng-hǎi'
        >>> p.get_pinyin(u"上海", tone_marks='numbers')
        >>> 'shang4-hai3'
        >>> # remove splitter
        >>> p.get_pinyin(u"上海", '')
        'shanghai'
        >>> # set splitter as whitespace
        >>> p.get_pinyin(u"上海", ' ')
        'shang hai'
        >>> p.get_initial(u"上")
        'S'
        >>> p.get_initials(u"上海")
        'S-H'
        >>> p.get_initials(u"上海", u'')
        'SH'
        >>> p.get_initials(u"上海", u' ')
        'S H'
    请输入utf8编码汉字
    .. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin
    """

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"files",
                             'Mandarin.dat')

    def __init__(self, data_path=data_path):
        self.dict = {}
        with open(data_path) as f:
            for line in f:
                k, v = line.split('\t')
                self.dict[k] = v
        self.fu_lastname = '''
    欧阳、太史、端木、上官、司马、东方、独孤、南宫、万俟、
    闻人、夏侯、诸葛、尉迟、公羊、赫连、澹台、皇甫、宗政、濮阳、公冶、太叔、申屠、
    公孙、慕容、仲孙、钟离、长孙、宇文、司徒、鲜于、司空、闾丘、子车、亓官、司寇、
    巫马、公西、颛孙、壤驷、公良、漆雕、乐正、宰父、谷梁、拓跋、夹谷、轩辕、令狐、
    段干、百里、呼延、东郭、南门、羊舌、微生、公户、公玉、公仪、梁丘、公仲、公上、
    公门、公山、公坚、左丘、公伯、西门、公祖、第五、公乘、贯丘、公皙、南荣、东里、
    东宫、仲长、子书、子桑、即墨、达奚、褚师、吴铭
    '''

    @staticmethod
    def decode_pinyin(s):
        s = s.lower()
        r = ""
        t = ""
        for c in s:
            if "a" <= c <= 'z':
                t += c
            elif c == ':':
                assert t[-1] == 'u'
                t = t[:-1] + "\u00fc"
            else:
                if '0' <= c <= '5':
                    tone = int(c) % 5
                    if tone != 0:
                        m = re.search("[aoeiuv\u00fc]+", t)
                        if m is None:
                            # pass when no vowels find yet
                            t += c
                        elif len(m.group(0)) == 1:
                            # if just find one vowels, put the mark on it
                            t = t[:m.start(0)] \
                                + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] \
                                + t[m.end(0):]
                        else:
                            # mark on vowels which search with "a, o, e" one by one
                            # when "i" and "u" stand together, make the vowels behind
                            for num, vowels in enumerate(("a", "o", "e", "ui", "iu")):
                                if vowels in t:
                                    t = t.replace(vowels[-1], PinyinToneMark[tone][num])
                                    break
                r += t
                t = ""
        r += t
        return r

    @staticmethod
    def convert_pinyin(word, convert):
        if convert == 'capitalize':
            return word.capitalize()
        if convert == 'lower':
            return word.lower()
        if convert == 'upper':
            return word.upper()

    def get_pinyin(self, chars=u'你好', splitter=u'-',
                   tone_marks=None, convert='lower'):
        result = []
        flag = 1
        for char in chars:
            key = "%X" % ord(char)
            try:
                if tone_marks == 'marks':
                    word = self.decode_pinyin(self.dict[key].split()[0].strip())
                elif tone_marks == 'numbers':
                    word = self.dict[key].split()[0].strip()
                else:
                    word = self.dict[key].split()[0].strip()[:-1]
                word = self.convert_pinyin(word, convert)
                result.append(word)
                flag = 1
            except KeyError:
                if flag:
                    result.append(char)
                else:
                    result[-1] += char
                flag = 0
        return splitter.join(result)
    
    def get_name_pinyin(self,chars="叶朝晖",splitter="",convert='lower'):
        result,flag = [],1
        for char in chars:
            key = "%X" % ord(char)
            try:
                word = self.dict[key].split()[0].strip()[:-1]
                word = self.convert_pinyin(word,convert)
                result.append(word)
                flag = 1
            except KeyError:
                if flag:
                    result.append(char)
                else:
                    result[-1] += char
                flag = 0
        if len(chars) > 1 and chars[:2] in self.fu_lastname:
            lastname1 = result.pop(0)
            result[0].capitalize()
            result[0] = lastname1.capitalize() + result[0] + ","
            if len(result) > 2:
                result[1] = splitter.join([result[1],result.pop(2)])
        else:
            if len(result) > 1:
                result[0] += ","
                result[0] = result[0].capitalize()
            try:
                result[1] = result[1].capitalize()
            except:
                pass
            if len(result) > 2:
                result[1] = splitter.join([result[1],result.pop(2)])
        
        return " ".join(result)
    
    def get_name_initial(self, chars, splitter="", convert='lower'):
        result,flag = [],1
        if chars[:2] in self.fu_lastname:
            start = 2
        else:
            start = 1
        for char in chars[:start]:
            key = "%X" % ord(char)
            try:
                word = self.dict[key].split()[0].strip()[:-1]
                word = self.convert_pinyin(word,convert)
                result.append(word)
                flag = 1
            except KeyError:
                if flag:
                    result.append(char)
                else:
                    result[-1] += char
                flag = 0
        lastname = "".join(result+[","])
        result.clear()
        for char in chars[start:]:
            result.append(self.get_initial(char))
        firstname = splitter.join(result)
        return " ".join([lastname, firstname])
        
    def get_initial(self, char=u'你'):
        try:
            return self.dict["%X" % ord(char)].split(" ")[0][0]
        except KeyError:
            return char

    def get_initials(self, chars=u'你好', splitter=u'-'):
        result = []
        flag = 1
        for char in chars:
            try:
                result.append(self.dict["%X" % ord(char)].split(" ")[0][0])
                flag = 1
            except KeyError:
                if flag:
                    result.append(char)
                else:
                    result[-1] += char

        return splitter.join(result)
    
    
if __name__ == "__main__":
    pin = Pinyin()
    print(pin.get_name_initial("赵崇旭",splitter="-", convert="capitalize"))
    print(pin.get_name_pinyin("赵崇旭",splitter="-", convert="capitalize"))
    