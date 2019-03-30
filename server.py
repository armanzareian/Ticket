import os.path
import mysql.connector
# import tornado.escape
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
import os
from binascii import hexlify
import tornado.web
from tornado.options import define, options





define("port", default=1104, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            #GET METHOD :
            (r"/getticketmod", getticketmod),
            (r"/getticketcli", getticketcli),
            # POST METHOD :
            (r"/signup", signup),
            (r"/login",login),
            (r"/logout", logout),
            (r"/sendticket", sendticket),
            (r"/changeaccess", changeAccess),
            (r"/restoticketmod", restoticketmod),
            (r"/changestatus", changestatus),
            (r"/closeticket", closeticket),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="arman1378",
            database="Ticket"
        )


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def check_user(self,user):
        print(user)
        cs=self.db.cursor()
        cs.execute("SELECT * FROM Users WHERE username = '{}'".format(user))
        resuser = cs.fetchall()
        if resuser:
            print("true")
            return True
        else :
            print("false")
            return False

    def check_api(self,api):
        cs = self.db.cursor()
        cs.execute("SELECT * FROM Users WHERE token = '{}'".format(api))
        resuser = cs.fetchall()
        if resuser:
            print(resuser)
            cs.execute("UPDATE Users SET token = %s WHERE username = %s ", ('', resuser[0][0]))
            self.db.commit()
            return True
        else:
            return False


    def check_auth(self,username,password):
        cs = self.db.cursor()
        cs.execute("SELECT * FROM Users WHERE username = '{}' and password = '{}'".format(username,password))
        resuser = cs.fetchall()

        if resuser:
            api_token = hexlify(os.urandom(16)).decode('utf-8')
            print(api_token)
            cs.execute("UPDATE Users SET token = %s WHERE username = %s ",(api_token,username))
            self.db.commit()
            return api_token
        else:
            return False

    def getUserName(self,token):
        cs = self.db.cursor()
        cs.execute("SELECT * FROM Users WHERE token = '{}'".format(token))
        resuser = cs.fetchall()
        if resuser:
            return resuser[0]
        else:
            return False

class signup(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if not self.check_user(username):
            print(username,password)
            cs = self.db.cursor()
            cs.execute("INSERT INTO Users (username, password, token) VALUES (%s, %s ,%s)",(username,password,''))
            self.db.commit()
            output = {
                    'message' : 'Signed Up Successfully',
                    'code': '200'
            }
            self.write(output)
        else:
            output = {
                'message': 'This Username Exist',
                'code': '400'
            }
            self.write(output)


class login(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        token=self.check_auth(username,password)
        print(token)
        if token:
            print(username,password)


            output = {
                      'message' : 'Logged in successfully',
                      'code' : '200',
                      'token' : token
            }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Username or Password',
                'code': '400'
            }
            self.write(output)

class logout(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        if self.check_api(token):
            output = {
                'message': 'Logged Out Successfully',
                'code':'200'
                      }
            self.write(output)
        else:
            output = {
                'message': 'Token Is Wrong',
                'code': '400'
            }
            self.write(output)
class sendticket(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        text = self.get_argument('text')
        subject = self.get_argument('subject')
        user=self.getUserName(token)
        if user:
            cs = self.db.cursor()
            cs.execute("INSERT INTO comments (username, ask, status, subject) VALUES (%s, %s ,%s ,%s)", (user[0], text, 'open', subject))
            self.db.commit()
            output={
                'message':'Ticket Sent Successfully',
                'code':'200'
            }
            self.write(output)
        else:
            output = {
                'message': 'Token Is Wrong',
                'code':'400'
            }
            self.write(output)

class restoticketmod(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        text = self.get_argument('text')
        commentId = self.get_argument('commentId')
        user=self.getUserName(token)
        if user:
            if user[3] is 1:
                cs = self.db.cursor()
                cs.execute("UPDATE comments SET answer = %s ,status = %s WHERE id = %s ", (text,'closed', int(commentId)))
                self.db.commit()
                output={
                    'message':'Response to Ticket With id -{}- Sent Successfully'.format(commentId),
                    'code':'200'
                }

            else:
                output = {
                    'message': 'you are not admin',
                    'code':'400'
                }
            self.write(output)
        else:
            output = {
                'message': 'Token Is Wrong',
                'code':'400'
            }
            self.write(output)
class changestatus(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        commentId = self.get_argument('commentId')
        status = self.get_argument('status')
        user = self.getUserName(token)
        if user:
            if user[3] is 1:
                cs = self.db.cursor()
                cs.execute("UPDATE comments SET status = %s WHERE id = %s ", (status, int(commentId)))
                self.db.commit()
                output = {
                    'message': 'Status Ticket With id -{}- Changed Successfully'.format(commentId),
                    'code':'200'
                }

            else:
                output = {
                    'message': 'you are not admin',
                    'code': '200'
                }
            self.write(output)
        else:
            output = {
                'meassage': 'Token Is Wrong',
                'code':'400'
            }
            self.write(output)
class closeticket(BaseHandler):
    def post(self):
        token = self.get_argument('token')
        commentId = self.get_argument('commentId')
        user = self.getUserName(token)
        if user:
            cs = self.db.cursor()
            cs.execute("SELECT * FROM comments WHERE username = '{}'".format(user[0]))
            resuser = cs.fetchall()
            for index in resuser:
                if index[0] is int(commentId):
                    cs = self.db.cursor()
                    cs.execute("UPDATE comments SET status = %s WHERE id = %s ", ('closed', int(commentId)))
                    self.db.commit()
                    output = {
                        'message': 'Ticket With id -{} Closed Succsessfully'.format(commentId),
                        'code':'200'
                    }
                    self.write(output)



        else:
            output = {
                'message': 'Token Is Wrong',
                'code':'400'
            }
            self.write(output)

class getticketcli(BaseHandler):
    def get(self):
        token = self.get_argument('token')
        status = self.get_argument('status')
        print(type(status))
        user = self.getUserName(token)
        if user:
            cs = self.db.cursor()
            if user[3] is 0:
                cs.execute("SELECT * FROM comments WHERE username = '{}'".format(user[0]))
                resuser = cs.fetchall()
                output = {
                    'code': '200'
                }
                z = 0
                for index in resuser:
                    # agar baz=1 & entezar = 2
                    out = {}
                    if index[2] == status:
                        out["subject"] = index[5]
                        out["id"] = index[0]
                        # out["username"]=index[1]
                        out["status"] = index[2]
                        out["ask"] = index[3]
                        out["answer"] = index[4]

                        output['block {}'.format(z)] = out
                        z = z + 1

                output["tickets"]='There Are -{}- Ticket'.format(z)
                self.write(output)

            else:
                output = {
                    'message': 'you are admin user',
                    'code':'400'
                }
                self.write(output)

        else:
            output = {
                'message': 'Token Is Wrong',
                'code': '400'
            }
            self.write(output)
class getticketmod(BaseHandler):
    def get(self):
        token = self.get_argument('token')
        status = self.get_argument('status')
        print(type(status))
        user = self.getUserName(token)
        if user:
            cs = self.db.cursor()
            if user[3] is 0:
                output = {
                    'message': 'you are normal user',
                    'code':'400'
                }
                self.write(output)
            else:
                cs.execute("SELECT * FROM comments")
                resuser = cs.fetchall()
                print(resuser)
                output = {
                    'code': '200'
                }
                z = 0
                for index in resuser:
                    # agar baz=1 & entezar = 2
                    out={}
                    if index[2] == status:
                        out["subject"] = index[5]
                        out["id"]=index[0]
                        # out["username"]=index[1]
                        out["status"]=index[2]
                        out["ask"]=index[3]
                        out["answer"]=index[4]

                        output['block {}'.format(z)] = out
                        z = z + 1

                output["tickets"] = 'There Are -{}- Ticket'.format(z)
                self.write(output)

        else:
            output = {
                'message': 'Token Is Wrong',
                'code':'400'
            }
            self.write(output)

class changeAccess(BaseHandler):
    def post(self):
        username = self.get_argument('username')
        rootPass = self.get_argument('rootPass')
        admin = self.get_argument('admin')
        if rootPass == "arman1378":
            cs = self.db.cursor()
            cs.execute("UPDATE Users SET admin = %s WHERE username = %s ", (int(admin), username))
            self.db.commit()
            output = {
                'message': 'Access of User:{} Was Changed'.format(username),
                'code':'200'
            }
            self.write(output)
        else:
            output = {
                'message': 'Wrong Root Password',
                'code':'200'
            }
            self.write(output)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
