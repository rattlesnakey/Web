from flask import Flask, render_template, request, session, redirect, url_for
import json
import config
import re
import pymssql

#连接数据库
conn = pymssql.connect(
                        server='.',
                        user='sa',
                        password='ZHJF2019eggs',  #用户名和密码根据个人设置需要修改                        
                        database='LangKe',
                        )

cursor = conn.cursor()

app = Flask(__name__)
app.config.from_object(config)                    

app.secret_key='Lang Ke'

#限制对应的身份进入对应的页面
@app.before_request
def is_login():
    
    if request.path =='/':
        return redirect('/login/')
    if request.path =='/login/':
        return None
    if request.path =='/logout/':
        return None
    if '/static'in str(request):
        return None
    if session.get('userID')==None:
        return redirect('/login/') 
    if session['role']== 'GM' and '/GM'in request.path:
        return None
    if session['role']== 'AM' and '/AM'in request.path:
        return None
    if session['role']== 'PM' and '/PM'in request.path:
        return None
    else:
        return '无法访问该界面'

#根据userID在数据库中查询username
def fillinusername(userID):
    sql="select username from dbo.[user] where email='"+userID+"'"
    cursor.execute(sql)
    userName=cursor.fetchall()
    try:
        return userName[0][0]
    except IndexError:
        return ''
    # if(len(userName)):
    #     userName=userName[0][0]
    # else:
    #     userName = ''
    # return userName        

#注销界面
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

#登陆界面
@app.route('/login/', methods = ['POST','GET'])
def login():
    if request.method=='GET':
        #userID和password匹配后，根据不同的role重定向至不同页面

        if session.get('userID'):
            if session.get('role')== 'GM' :
                return redirect(url_for('indexGM'))
            elif session.get('role')== 'AM' :
                return redirect(url_for('indexAM'))
            elif session.get('role')=='PM':
                return redirect(url_for('indexPM'))
        else:
            return render_template('index.html', error=None)
    elif request.method=='POST':
        error=None
        userID = request.form['loginemail']
        pwd = request.form['loginpassword']
        
#============================================================================    
# 用户名 密码是否都已经输入    
        if not all([userID,pwd]):
            if userID == "":
                error = "请输入用户名"
                return render_template('index.html',error=error)
            else:
                error = "请输入密码"
                return render_template('index.html',error=error)
# 在数据库中查询用户名 密码是否匹配
        arg = (userID,pwd)
        sql1 = "select email from dbo.[user] where email=%s and password=%s"
        cursor.execute(sql1,arg)
        rs_userid = cursor.fetchall()
                
# 用户名和密码匹配        
        if(len(rs_userid) != 0):
            #用户登录设置session的userID和username
            session['userID']=userID
            session['username']=fillinusername(userID)

            #在数据库中根据用户名查询身份
            sql2 = "select role from [user] where email =\'"+userID+"\'"
            cursor.execute(sql2)
            rs_roleid= cursor.fetchall()
            roleID=sorted(rs_roleid)[-1][0] # 取最大的roleID，避免多重身份影响
            #根据不同角色重定向至不同页面
            if(roleID==1):
                #将用户角色加入session
                session['role']='GM'
                return redirect(url_for('indexGM'))
            elif(roleID==2):
                session['role']='AM'
                return redirect(url_for('indexAM'))
            elif(roleID==3):
                session['role']='PM'
                return redirect(url_for('indexPM'))
        else: # 用户名和密码不匹配    
            error="账号或密码错误"
            return render_template('index.html',error = error)

def deny():
    return "Permission denied"

@app.route('/AM/indexAM', methods=['GET','POST'])
def indexAM():
    return render_template('indexAM.html')

@app.route('/GM/indexGM', methods=['GET','POST'])
def indexGM():
    return render_template('indexGM.html')

@app.route('/PM/indexPM', methods=['GET','POST'])
def indexPM():
    return render_template('indexPM.html')

if __name__ == '__main__':
    app.run(debug=True)