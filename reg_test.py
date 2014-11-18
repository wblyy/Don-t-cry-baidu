 # encoding: UTF-8
import re
import urllib2
import urllib

class Reg_test(object):
	#def open_url(url):
	#	return urllib2.urlopen(url).read()
	def get_bing_similar(self,title,content):
		answer_url = "http://cn.bing.com/search?q="+urllib.quote(title+content+"+    -zhidao.baidu.com")
        #answer_url="http://cn.bing.com/search?q=%E8%BF%99%E9%A6%96%E6%AD%8C%E5%8F%AB%E4%BB%80%E4%B9%88%E5%90%8D%E5%AD%97+-zhidao.baidu.com"                                                                                     
		#print answer_url
		msg=urllib2.urlopen(answer_url).read()
		p = re.compile(r'class=" b_goodBadge">最佳答案(.*?)</strong> \.\.\.')
		mstr=p.findall(msg)#.decode('utf-8').encode('utf-8'))                                                                                                                                                                           
		#print msg
		answer=''
		for word in mstr:
			#print word.decode('utf-8')#.encode('utf-8')                                                                                                                                                                         
                                                                                                                                                                                                                                 
			p =re.compile(r'</?\w+[^>]*>')
			filt=p.split(word)
			for chinese in filt:
		            #print chinese.decode('utf-8')
			    answer=answer+chinese
			return answer

if __name__ == "__main__":
	#answer_url="http://cn.bing.com/search?q="+urllib.quote("这首歌叫什么名字+    -zhidao.baidu.com")
	answer_url = "http://cn.bing.com/search?q=%E6%88%91%E4%B9%9F%E4%B8%8D%E7%9F%A5%E9%81%93%E8%BF%99%E9%A6%96%E6%AD%8C%E5%8F%AB%E4%BB%80%E4%B9%88%E5%90%8D%E5%AD%97+++-zhidao.baidu.com&go=%E6%8F%90%E4%BA%A4&qs=n&form=QBRE&pq=%E6%88%91%E4%B9%9F%E4%B8%8D%E7%9F%A5%E9%81%93%E8%BF%99%E9%A6%96%E6%AD%8C%E5%8F%AB%E4%BB%80%E4%B9%88%E5%90%8D%E5%AD%97+-zhidao.baidu.com&sc=0-0&sp=-1&sk=&cvid=6005d324279b4bfbb18b3da60cad9b49"

	print answer_url
	msg =urllib2.urlopen(answer_url).read()
	print msg 
#print msg
#[^x00-xff]|#
#p = re.compile(r'最佳答案?(?:[\u4e00-\u9fa5]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	p = re.compile(r'class=" b_goodBadge">最佳答案(.*?)</strong> \.\.\.')
#p = re.compile('最佳答案')

	mstr=p.findall(msg)#.decode('utf-8').encode('utf-8'))
	answer=''
	for word in mstr:
		print word.decode('utf-8')#.encode('utf-8')
		p =re.compile(r'</?\w+[^>]*>')
		filt=p.split(word)
		for chinese in filt:
			print chinese.decode('utf-8')
			answer=answer+chinese

			print answer
### output ###
# ['1', '2', '3', '4']
