from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from correios import Correios

class YQLPage(webapp.RequestHandler):
    def get(self):
        encomenda = Correios.encomenda('ES446391025BR')
        
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.response.out.write('<result>')
        
        for status in encomenda.status:
            self.response.out.write('   <status>')
            self.response.out.write('       <data><![CDATA[%s]]></data>' % status.data)
            self.response.out.write('       <local><![CDATA[%s]]></local>' % status.local)
            self.response.out.write('       <situacao><![CDATA[%s]]></situacao>' % status.situacao)
            self.response.out.write('       <detalhes><![CDATA[%s]]></detalhes>' % status.detalhes)
            self.response.out.write('   </status>')
        
        self.response.out.write('</result>')

application = webapp.WSGIApplication(
                                     [('/yql.*', YQLPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()