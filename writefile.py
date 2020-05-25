def printit(a,b,c):
    html_file = open('./templates/' + a + '.html','w')
    html_file.write(b + '<br>')
    html_file.write(c)
    html_file.close()
    return True

