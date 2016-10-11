import configparser

cf = configparser.ConfigParser()

print ("use ConfigParser() read")
cf.read("crawl.conf")
print (cf.get("portal", "url"))

print ("use ConfigParser() write")
cf.set("portal", "url2", "%(host)s:%(port)s")
print (cf.get("portal", "url2"))