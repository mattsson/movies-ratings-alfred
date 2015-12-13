import sys
import urllib
from workflow import Workflow, ICON_WEB, web

def main(wf):
  
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None
        
    if len(query) < 2:
        wf.add_item(title = 'Enter a movie title',
                    subtitle = 'Please enter more than 2 characters.')
        wf.send_feedback()
        return

    imdbURL = 'http://www.imdb.com/title/'

    moviesData = web.get('http://www.omdbapi.com/?s=' + urllib.quote(query) + '&r=json').json()
    
    if 'Response' in moviesData:
      wf.add_item(title = 'Nothing was found.')
      
    elif 'Search' in moviesData:

        for movie in moviesData['Search']:
            extendedMovieData = web.get('http://www.omdbapi.com/?tomatoes=true&i=' + movie['imdbID'] + '&r=json').json()

            wf.add_item(title = '%s (%s)' % (movie['Title'], movie['Year']),
                        subtitle = 'IMDb: %s RT: %s%s Metacritic: %s' % (extendedMovieData['imdbRating'], extendedMovieData['tomatoMeter'], '' if extendedMovieData['tomatoMeter'] == 'N/A' else '%', extendedMovieData['Metascore']),
                        arg = imdbURL + movie['imdbID'],
                        valid = True,
                        )

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))