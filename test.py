def fun1():
    pageNum = [1]
    print(len(pageNum))
    pageNum = len(pageNum) == 0 and 0 and pageNum[0]
    print(pageNum)
fun1()