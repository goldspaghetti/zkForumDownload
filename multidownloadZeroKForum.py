#downloads one page of zerok forum posts by using
#multiple threads

rankDictionary = {
    '0':'gray',
    '1':'dark red',
    '2':'red',
    '3':'orange',
    '4':'bright yellow',
    '5':'blue white',
    '6':'dark blue',
    '7':'purple'
}


import os, requests, bs4, math, time, threading
#starting time
startTime = time.time()
url = 'https://zero-k.info/Forum'
os.makedirs('/Users/alan.chen/Documents/zeroKLog', exist_ok=True)
res = requests.get(url)
soup = bs4.BeautifulSoup(res.content, features='html.parser')
linkElem = soup.select('a[style="word-break:break-all;"]')
#for each forum post
def downloadZeroK(linkNum):
    #creates a title which gets rid of ' ' and '/'
    originalTitle = linkElem[linkNum].getText()
    listTitle = list(originalTitle)
    for length in range(len(listTitle)):
        if listTitle[length] == ' ':
            listTitle[length] = '_'
        if listTitle[length] == '/':
            listTitle[length] = '_or_'
    title = ''.join(listTitle)
    print(title)
    postLink = 'https://zero-k.info' + linkElem[linkNum].get('href')
    res = requests.get(postLink)
    postSoup = bs4.BeautifulSoup(res.content, features='html.parser')
    posts = postSoup.select('div[class="post"]')
    post = open('/Users/alan.chen/Documents/zeroKLog/' + title + '.txt', 'w')
    post.close()
    #bad formating
    #getting page amount
    resUrl = requests.get(url)
    forumSoup = bs4.BeautifulSoup(resUrl.content, features='html.parser')
    forumInfo = forumSoup.select('tr[class]')
    postNum = int(forumInfo[linkNum].select('td')[3].getText())
    #postAmount = postSoup.select('div[style="float:right"]')[0].getText()
    #listNum = []
    #for letters in range(len(postAmount)-1):
    #    if postAmount[letters] != ' ':
    #        listNum.append(postAmount[letters])
    #    else:
    #        break
    #postNum = int(''.join(listNum))
    pageAmount = math.ceil(postNum/20)
    #testing purposes:
    print('amount of posts: ' + str(postNum))
    #for each individual post
    for numbers in range(pageAmount):
        if postNum < 20:
            postLink = 'https://zero-k.info' + linkElem[linkNum].get('href')
        else:
            postLink = 'https://zero-k.info' + linkElem[linkNum].get('href') + '&Search=&User=&grorder=&grdesc=False&grpage=' + str(numbers + 1)
        print('downloading from: ' + postLink)
        res = requests.get(postLink)
        postSoup = bs4.BeautifulSoup(res.content, features='html.parser')
        posts = postSoup.select('div[class="post"]')
        for number in range(len(posts)):
            print(len(posts))
            print(number)
            content = posts[number].select('div[class="entry__text"]')[0].getText()
            username = posts[number].select('div[class="user__name"]')[0].getText()
            postTime = posts[number].select('div[class="user__posttime"]')[0].getText()
            #image = posts[number].select('img[src]')[0].get('src')
            #video = posts[number].select('source[type="video/webm"]')[0].get('src')
            if username[1:-1] == '{redacted}':
                post = open('/Users/alan.chen/Documents/zeroKLog/' + title + '.txt', 'a')
                post.write(f'''{username}{postTime}{content}\n--------------\n''')
                break
            #testing
            try:
                rating = posts[number].select('div[class="entry__rating"]')[0].getText()
            except IndexError:
                print('I DO NOT KNOW WHAT WENT WRONG BUT SOMETHIG IS WRONG')
            rank = rankDictionary.get(posts[number].select('div[class="user__name"]')[0].select('img[class="icon16"]')[0].get('src')[-5])
            post = open('/Users/alan.chen/Documents/zeroKLog/' + title + '.txt', 'a')
            post.write(f'''{username}{postTime}{rank}{content}{rating}\n---------------------\n''')
    post.close()
#creates and starts the threads
downloadThreads = []
for i in range(0, len(linkElem)-1):
    print(i)
    downloadThread = threading.Thread(target=downloadZeroK, args=[i])
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()

#ending time
lastTime = (time.time() - startTime)
print('time spent: ' + str(lastTime) + ' seconds')

