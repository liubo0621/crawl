# enconding = utf8
f=file("hello.txt","w+")

li=["hello world\n","hello china\n"]

f.writelines(li)

f.close()