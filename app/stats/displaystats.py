import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from stats import PerUserTotals, PerUserStats, PerRoundStats

class MainPage(webapp.RequestHandler):
  def get(self):
    usertotals = PerUserTotals.all().order('-cupsDrunk').fetch(999)
    pastweek  = PerUserStats.all().fetch(50)
    
    template_values = {
        'usertotals': usertotals,
        'pastweek': pastweek,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'statstemplate.html')
    self.response.out.write(template.render(path, template_values))
      
application = webapp.WSGIApplication([('/stats', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
