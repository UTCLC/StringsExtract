Search strings from whole file<br>
Regex pattern: ```\"(?:\\\.|[^\"\\\])*\"```<br>
Output JSON key pattern: ```Filename:Line:Num```<br>
Filename = File name, contains relative path<br>
Line = Line number<br>
Num = The number of strings that appear in this line

从整个文件中搜寻字符串<br>
正则表达式：```\"(?:\\\.|[^\"\\\])*\"```<br>
输出的 JSON 的键格式：```文件名:行:个```<br>
文件名：文件名，包含相对路径<br>
行：第几行<br>
个：这行出现的第几个字符串