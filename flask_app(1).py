from flask import Flask, render_template, request
from authentication import getUStime
from PIL import Image
import os,time

from werkzeug import secure_filename

app = Flask(__name__)

def logUsage(log,program):      #logging programs-> AddArticle,Search,Authentication
    time=getUStime()
    fpath='logs/'+program+'_Log.txt'
    f=open(fpath,'a+')         #file to log activities of this article method
    f.write('<--------------------------------------------------------------------\n<- MVRT Resources '+program+' | '+time+'\n')
    f.write(log)
    f.write('<--------------------------------------------------------------------\n\n')
    f.close()

#Default Resources Page with article cards, and once clicked it shows articles
@app.route('/')
def hello_world():
    return render_template('res3.html',methods=['GET','POST'])

@app.route('/check')
def lo_world():
    return render_template('resources.html',methods=['GET','POST'])

@app.route('/login')         #render the HTML page which has the login page
def login():
    return render_template('login.html',methods=['GET','POST'])

@app.route('/authenticate',methods=['POST','GET'])
def checkLogin():
    log=''
    allowed={'0':'electricalRee','1':'mechanicalRee','2':'softwareRee','3':'financeRee','4':'marketingRee','5':'outreachRee'}
    divisions={'0':'Electrical','1':'Mechanical','2':'Software','3':'Finance','4':'Marketing','5':'Outreach'}

    divis=str(request.args.get('div'))      #retrieve encrypted login info from webpage
    cnam=str(request.args.get('nam'))
    cpwd=str(request.args.get('uwp'))
    key=int(request.args.get('key'))

    name,passwd,auth='','',False            #decrypt login info
    for char in cnam:
        name+=chr(ord(char)-key)
    for char2 in cpwd:
        passwd+=chr(ord(char2)-key)

    log+='<- Authentication Request from '+name+' for '+divisions[divis]+'\n'   #log this event and check authentication
    for div in allowed:
        if divis==div and allowed[div]==passwd:
            data={'name':name}
            log+='<- Authentication Successful\n'
            auth=True

    if not auth:
        log+='<-- Authentication Failed\n'
    logUsage(log,'Authentication')
    if auth: return render_template('editor.html',methods=['GET','POST'],data=data)
    else: return ('MVRT Resources Authentication Failed, sorry '+name+' :(')

@app.route('/editor')   #render the HTML page which has the editor page
def editor():
    return render_template('editor.html',methods=['GET','POST'],data={'name':'undefined'})

@app.route('/preview')  #render the HTML page which has the preview page
def preview():
    return render_template('preview.html',methods=['GET','POST'])

@app.route('/getimg')   #render HTML page with thumbnail image input
def funccc():
    return render_template('card_img.html',methods=['GET','POST'])

@app.route('/uploadfile',methods=['POST'])  #process image upload and convert to webp format for smaller file size
def fileup():
    f = request.files['file']
    fname='mysite/static/images/'+secure_filename(f.filename)
    f.save(fname)
    Image.open(fname).convert('RGB').save(fname.replace('png','webp'),'webp')
    os.system('rm '+fname)
    return render_template('card_text.html',methods=['GET','POST'])

@app.route('/addArticle',methods=['POST'])  #Adds article in the background without refreshing webpage
def addArticle():
    received,artjs=False,False     #will be used to make sure previous steps were completed
    article,article_title,card,categ,logtxt='','','','',''

#try to get new article, card and its category in json format from the webpage and parse it into strings and an integer
    try:
        data=request.get_json()
        article = str(data['article'])
        article=article.replace("'","\\'")
        card = str(data['card'])
        categ = int(data['categ'])
        article_title=card.split('<h2>')[1].split('</h2>')[0]
        received=True
        logtxt+='<- Article "'+article_title+'" was received successfully from website\n'
    except:
        logtxt+='<- Error occured in accessing article from website\n'

    ids=[0,0,0, 0,0,0, 0,0,0, 0,0]        #holds number of articles per category as articles.js is read

#try to add new article to articles.js and find out current number of articles per category
    if received:
        try:
            with open("mysite/static/js/articles.js","r") as h:
                for line in h:
                    if "arend':" in line and "'ar" in line:
                        ln=line.split("'ar")[1].split("arend':")[0]
                        ids[int(ln.split('c')[1])]=int(ln.split('c')[0])
            idtext="'ar"+str(((ids[categ])+1))+'c'+str(categ)+"arend'"
            article=article.replace("\\'arcarend\\':",idtext+":`")

            with open("mysite/static/js/articles.js","r+") as hf:
                contents = hf.read().replace(">`};", ">`,\n\n\t\t\t\t"+article+"`};")
                hf.seek(0)
                hf.truncate()
                hf.write(contents)
            card=card.replace('onclick="showArticle()"','onclick="showArticle('+idtext+')"')    #adds the key of article in articles.js to article card html
            artjs=True
            logtxt+='<- File "article.js" was successfully updated with new article\n'
        except:
            logtxt+='<- Error occured in updating file "articles.js"\n'

    articleTitlePortion=card.split("$$##$$")[0]
    articleThumbPortion=card.split("$$##$$")[1]

    def insertStuff(fp,line,stuff):
        j = open(fp, "r")
        contents = j.readlines()                                    #get all of mvrtlibcopy
        j.close()
        contents.insert(line, ("\t\t\t\t\t\t\t\t"+stuff+"\n"))
        k = open(fp, "w")
        contents = "".join(contents)                                #update mvrtlibcopy with card for new article
        k.write(contents)
        k.close()

    if received and artjs:
        try:
            filepath="mysite/templates/res3.html"
            #location=["columnart","columnimg"]
            labels=['Design','CAD Tutorials','Manufacturing','Electrical','Software','Photography/Videography','Outreach','Finance','Marketing','Old Submissions','Rookie Training']
            linenum=0
            section=False
            #finds out where next card will go based on current status
            with open("mysite/templates/res3.html","r") as g:
            	for line in g:
            		if ("<h1>"+labels[categ]+"</h1>") in line: section=True
            		if section and "columnimg" in line:
            		    linenum+=1
            		    insertStuff(filepath,linenum,articleThumbPortion)
            		if section and "columnart" in line:
            		    linenum+=2
            		    insertStuff(filepath,linenum,articleTitlePortion)
            		    break
            		linenum+=1
            logtxt+='<- File "mvrtlib.html" was successfully updated with new article card\n'

        except:
            logtxt+='<- Error occured in updating file "mvrtlib.html"\n'

#log all the activity in log file
    logUsage(logtxt,'AddArticle')
    os.system('touch ../../var/www/mvrtresources_pythonanywhere_com_wsgi.py')
    time.sleep(5)
    return ("nothing")

@app.route('/query',methods=['POST','GET'])  #Searches articles in the background without refreshing webpage
def query():
    log=''
    results,artids,categs,titles=[],[],[],[]
    labels=['Design','CAD Tutorials','Manufacturing','Electrical','Software','Photography/Videography','Outreach','Finance','Marketing','Old Submissions','Rookie Training']
    try:
        keyword=str(request.args.get('keyword'))
        log+='<- Query received successfully for: '+keyword+'\n'
        try:
            f=open('mysite/static/js/articles.js','r')
            text=f.read().lower()
            f.close()
            sentences=text.split('.')
            log+='<- File opened successfully\n'
            for sentence in sentences:
                if "arend':" in sentence:
                    artid="ar"+str(sentence.split("arend':")[0].split("'ar")[1])
                if (keyword in sentence) and (artid not in artids):
                    if 'com' in sentence or 'http' in sentence or 'www' in sentence:
                        continue
                    results.append(str(sentence))
                    artids.append(artid)
                    categs.append(labels[int(artid.split('c')[1])])
            if not results:
                results.append('No results found for "'+keyword+'", ERR-03')
                log+='<- No search results found\n'
            else:
                log+='<- Found '+str(len(results))+' search results\n'
                try:
                    useful=[]
                    with open('mysite/templates/res3.html') as tr:
                        for line in tr:
                            if ('div onclick="showArticle(' in line) or ('" onclick="showArticle(' in line):
                                useful.append(line)
                    for article in artids:
                        for line in useful:
                            if article in line:
                                titles.append(str(line.split('</h2>')[0].split('<h2>')[1]))
                except: log+='<- Error occured in finding title\n'
        except:
            log+='<- Error occured in opening article file\n'
            results.append('Error occured in search engine, check searchlog, code ERR-02')
    except:
        log+='<- Error occured in receiving query\n'
        results.append('Error occured in search engine, check searchlog, code ERR-01')
    data={'results':results,'categs':categs,'artids':artids,'titles':titles}
    logUsage(log,'Search')
    return render_template('results.html',data=data)
