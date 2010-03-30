from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from correios import Correios

class YQLPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write('<?xml version="1.0" encoding="UTF-8"?>')
        
        encomenda = None
        try:
            encomenda = Correios.encomenda(self.request.get('numero', default_value=''))
        except Exception, e:
            pass #will return empty result :)
        
        if encomenda:
            self.response.out.write('<results>')
        
            for status in encomenda.status:
                detalhes = status.detalhes if status.detalhes else ''
                self.response.out.write('   <status>')
                self.response.out.write('       <data><![CDATA[%s]]></data>' % status.data)
                self.response.out.write('       <local><![CDATA[%s]]></local>' % status.local)
                self.response.out.write('       <situacao><![CDATA[%s]]></situacao>' % status.situacao)
                self.response.out.write('       <detalhes><![CDATA[%s]]></detalhes>' % detalhes)
                self.response.out.write('   </status>')
        
            self.response.out.write('</results>')
        else:
            self.response.out.write('<results />')

application = webapp.WSGIApplication(
                                     [('/yql.*', YQLPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()