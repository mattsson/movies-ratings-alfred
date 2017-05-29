import sys
import urllib
from workflow import Workflow, ICON_WEB, web

log = None

def main(wf):
  
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    # log.debug('Started')
    # log.debug(query)
        
    if len(query) < 2:
        wf.add_item(
            title = 'Enter a movie title',
            subtitle = 'Please enter more than 1 character.'
        )
        wf.send_feedback()
        return

    imdbURL = 'http://www.imdb.com/title/'

    moviesData = web.get('http://www.omdbapi.com/?s=' + urllib.quote(query) + '&r=json&apikey=cfc98aff').json()
    
    if 'Response' in moviesData and moviesData['Response'] == "False":
        wf.add_item(title = 'Nothing was found.')
      
    elif 'Search' in moviesData:
        counter = 0
        for movie in moviesData['Search']:
            counter = counter + 1

            # Only show a max of 5 results to spare the OMDB API
            if counter > 5:
                break

            # We set a low timeout for subsequent requests to not block the execution of the script
            # That is, user input will be ignored until existing requests finish.
            timeout = 0.5
            subtitle = "Could not fetch details in time, try searching for this specific title to get info."

            try:
                response = web.get('http://www.omdbapi.com/?tomatoes=true&i=' + movie['imdbID'] + '&r=json&apikey=cfc98aff', timeout=timeout)

                extendedMovieData = response.json()
                imdbRating = extendedMovieData['imdbRating']
                tomatoesRating = extendedMovieData['Ratings'][1]['Value']
                subtitle = 'IMDb: %s RT: %s Metacritic: %s' % (imdbRating, tomatoesRating, extendedMovieData['Metascore'])
            except:
                log.debug("Caught timeout exception")

            wf.add_item(
                title = '%s (%s)' % (movie['Title'], movie['Year']),
                subtitle = subtitle,
                arg = imdbURL + movie['imdbID'],
                valid = True
            )

    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))