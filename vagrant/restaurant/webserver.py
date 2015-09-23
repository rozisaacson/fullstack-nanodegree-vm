from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import database_setup


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
    	print "trying to handle..."
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                <html><body>
                <h1>Hello!</h1>
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" ><input type="submit" value="Submit"></form>
                </body></html>
                '''
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '''
                <html><body>
                <h1>Hola!</h1>
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" ><input type="submit" value="Submit"></form>
                <a href='/hello'>Go back to hello</a>
                </body></html>
                '''
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                content = database_setup.getRestaurants()
                output = "<html><body><h1>Restaurant</h1><div>{}</div></body></html>".format(content)
                self.wfile.write(output)
                print output
                return                

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = '''
            <html><body>
            <h2> Okay, how about this: </h2>
            <h1> %s </h1> 
            <form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>
            </body></html>''' % messagecontent[0]


            self.wfile.write(output)
            print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        print "debug"
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()