# -*- coding: utf-8 -*- 
#dsdsdsd
import urllib2
import urllib
#from mydb import NLPdb
import sys
import json
import random
reload(sys)
sys.setdefaultencoding('utf-8')
word_dict={'a':'adjective',
           'b':'other_noun_modifier',
           'c':'conjunction',
           'd':'adverb',
           'e':'exclamation',
           'g':'morpheme',
           'h':'prefix',
           'i':'idiom',
           'j':'abbreviation',
           'k':'suffix',
           'm':'number',
           'n':'general_noun',
           'nd':'direction_noun',
           'nh':'person_name',
           'ni':'organization_name',
           'nl':'location_noun',
           'ns':'geographical_name',
           'nt':'temporal_noun',
           'nz':'other_proper_noun',
           'o':'onomatopoeia',
           'p':'preposition',
           'q':'quantity',
           'r':'pronoun',
           'u':'auxiliary',
           'v':'verb',
           'wp':'punctuation',
           'ws':'foreign_words',
        'x':'non_lexeme',
           }
person_name_list=['你确定是***唱的？',
          '***有唱过这首歌吗？',
          '最喜欢***的歌了,',
          '之前看***的现场好像还听过这首歌,',
          '***好像在电视里也唱过这首,',
          '以前看电影好像***也唱过,']

adjective_list=['这首歌还挺***的,',
    '听上去会是***的感觉,',
    '感觉其实听起来反而不那么***,',
    '要是能再***一点就好了,',
    '***的感觉不是每次听都能体会,',
    '以前不觉得有多***,']

geographical_name_list=['好像真的在***听过,',
    '以前在***读书的时候听过,',
    '在***旅游的时候好像在那儿的酒吧里听过,',
    '***是个好地方,']

other_proper_noun_list=['乍一听应该是一首***歌,',
    '你确定这是一首***歌？',
    '歌手的嗓音很适合演绎这类***歌,']

temporal_noun_list=['每一个***，我都会戴上耳机陷入类似的情绪,',
    '每当***来临，好像都会听到这类声音,',
    '***是最适合听歌的时候,']

man_woman_list=['你确定这首歌是***歌手唱的？',
    '乍一听应该是国外的***歌手唱的',
    '这类***性的声音还是挺不错的',
    '***性的嗓音唱成这样很不容易',
    '不是所有***人都能唱出这类声音的']

class NLP_process(object):
    def talk_handler(self,pos,cont):
        if pos=='person_name':
            return random.choice(person_name_list).replace('***',cont)
        if pos=='adjective':
            return random.choice(adjective_list).replace('***',cont)
        if pos=='geographical_name':
            return random.choice(geographical_name_list).replace('***',cont)
        if pos=='other_proper_noun':
            return random.choice(other_proper_noun_list).replace('***',cont)
        if pos=='temporal_noun':
            return random.choice(temporal_noun_list).replace('***',cont)
        if cont=='男' or cont=='女':
            return random.choice(man_woman_list).replace('***',cont)
        return ''



    def reply(self,sentence):
        try:
            sentence=sentence.replace('?','')
            sentence_url='http://ltpapi.voicecloud.cn/analysis/?api_key=62S5e8g1Rwab5wIgSIOyeUBUpqkXIjLVKo7GlxDz&text='+sentence+'&pattern=all&format=json'
            msg=urllib2.urlopen(sentence_url).read()
            json_info=json.loads(msg)
            reply_word=''
            
            for info in json_info[0][0]:
                pos= word_dict.get(info["pos"])
                cont= info["cont"].encode('utf-8')#.decode('utf-8')
                print '获得词性：',pos,cont
                reply_word=reply_word+self.talk_handler(pos,cont)

            return reply_word
        except Exception, e:
            print e
