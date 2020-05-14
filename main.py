from flask import Flask, jsonify, render_template, request
from git import Repo
app = Flask(__name__)


#rendering the HTML page which has the button
@app.route('/')
def begin():
    return render_template('index.html')

#Adds article in the background without refreshing webpage
@app.route('/addArticle',methods=['POST'])
def addArticle():
    xx=request.form['article']
    print(xx)

    #needs article='</div>,<div class gdocs><iframe youtube></div>];',
    #needs categ='<h1>Category</h1>', choice=int(0-9),

    #get current article structure status
    '''qts=[]
    with open("mvrtlibid.txt","r") as f:
    	for line in f:
    		qts.append(int(line))
    id=qts[0]+1
    qts[0]=id

    #add new article to articles.js
    with open("../jatinsoni006.github.io/assets/js/articles.js","r+") as hf:
    	contents = hf.read().replace("</div>'];", article)
    	hf.seek(0)
    	hf.truncate()
    	hf.write(contents)
    location=["left","center","right"]
    linenum=0
    section=False
    #finds out where next card will go based on current status
    with open("../jatinsoni006.github.io/mvrtlibcopy.html","r") as f:
    	for line in f:
    		if categ in line: section=True
    		if section and location[qts[choice+1]-1] in line:
    			linenum+=1
    			break
    		linenum+=1

    #get all of mvrtlibcopy
    f = open("../jatinsoni006.github.io/mvrtlibcopy.html", "r")
    contents = f.readlines()
    f.close()

    #update mvrtlibcopy with card for new article
    contents.insert(linenum, card)
    f = open("../jatinsoni006.github.io/mvrtlibcopy.html", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

    #update mvrtlibid.txt
    if qts[choice+1]<3: qts[choice+1]+=1
    else: qts[choice+1]=1
    with open("../jatinsoni006.github.io/mvrtlibid.txt","w") as f2:
    	for numero in qts:
    		f2.write(str(numero)+"\n")

    #update github with changes
    repo_dir='../jatinsoni006.github.io'
    repo=Repo(repo_dir)
    files=['C:\\Users\\Jatin\\Documents\\mvrtsite\\jatinsoni006.github.io\\assets\\js\\articles.js']     #possible to add more files here
    msg='Added new article'             #later add info abt article
    repo.index.add(files)
    repo.index.commit(msg)
    repo.remote('origin').push() '''       #pushes changes to git
    print("hi there!")
    return ("nothing")

if __name__ == '__main__':
   app.run()
