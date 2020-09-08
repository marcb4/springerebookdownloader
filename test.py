import wget


file1 = open('isbn.txt', 'r') 
count = 0


while True:
    count += 1

    line = file1.readline()

    if not line: 
        break
    url = "https://link.springer.com/content/pdf/10.1007%2F{}".format(line.strip())+".pdf"
    filename = wget.download(url)
#    print(url)
