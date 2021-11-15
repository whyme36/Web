# Request

The ```requests``` module allows you to send HTTP requests using Python.

The HTTP request returns a Response Object with all the response data (content, encoding, status, etc).

This package is similar to selenium, but it is much faster because it does not use a browser, the queries are directed directly to the pages/server.

The problem for the package however is scripts (AJAX) on the page, at which point the ```selenium``` library is recommended.

# Beautiful Soup
Beautiful Soup is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. It commonly saves programmers hours or days of work.
## Usage
* downloading data from the internet
* Web Crawling

## Caution 
You can not use this library on pages without first knowing its rules, often sites prohibit the download of data from their pages, in an automatic manner, or indicate a certain number of requests per second. This has to do with the functioning of the server, which by a large number of requests can have problems with serving other users.

