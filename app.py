# coding: utf-8
import renren
import sprintfield
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

result = open('episode.txt', 'w')

sname, season, name, ename, pic, desc = renren.renrenfetch('http://www.zimuzu.tv/resource/34004')

result.write(name + ' ' + ename + ' ' + u'全集第' + season + u'季第1集剧本完整版\n\n')
result.write(u'剧本 台词 字幕 笔记 中英文对照 纯英文 学英语 文本 PDF 文档 电子版 纸质版\n\n')
result.write('[img]' + pic + '[/img]\n\n')
result.write(desc + '\n\n')
result.write(u'【剧本】：\n')

script = sprintfield.springfiledfetch(sname, season)
result.write(script)



