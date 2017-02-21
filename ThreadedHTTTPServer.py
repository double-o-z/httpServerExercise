from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi
import os
import logging

IP = '127.0.0.1'
PORT = 8080
LOG_FORMAT = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s' + '\tFrom {}:{}'.format(IP, PORT)

logging.basicConfig(filename="logs/server.log",
                    filemode='a',
                    format=LOG_FORMAT,
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('ServerLog')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.currentThread().getName()
        logger.info(message)
        return

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        logger.info('Client: %s' % str(self.client_address))
        logger.info('Path: %s' % self.path)
        logger.info('Form data:')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_path = "saved_files\\%s" % field_item.filename
                try:
                    os.remove(file_path)
                finally:
                    write_file = open("saved_files\\%s" % field_item.filename, "wb")
                    write_file.write(file_data)
                    write_file.close()
                file_len = len(file_data)
                del file_data
                logger.info('Uploaded %s as "%s" (%d bytes)' % \
                            (field, field_item.filename, file_len))
                # Send file to VirusTotal API and get response
                
                # Send respose to client as JSON with self.wfile.write(JSONResponse)
            else:
                # Regular form value
                logger.info('%s=%s' % (field, form[field].value))
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer((IP, PORT), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
