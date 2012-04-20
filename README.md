**Description**

I decided to add a list of strongly connected pages to each search result. I used Kosaraju's algorithm to find strongly connected components of the directed graph of all crawled pages. I think that pages that contain similar information usually link to each other and listing related pages under each search result provides extra information that a user could use to assess the quality of search results.

Here is the graph of the sample web pages included in the code. There are two clusters of pages. One about python snakes and the other about the python language. The two strongly connected component groups are colored.

![enter image description here][1]

Here is an example result of running the search_with_scc.py

    zeus:~/projects/CS101 (master)$ python search_with_scc.py 
    Search results for ['python', 'language']
    http://udacity.com/python/language7.html
       Strongly connected web pages:
        http://udacity.com/python/language8.html
        http://udacity.com/python/language6.html
    http://udacity.com/python/language8.html
       Strongly connected web pages:
        http://udacity.com/python/language6.html
        http://udacity.com/python/language7.html
    http://udacity.com/python/language6.html
       Strongly connected web pages:
        http://udacity.com/python/language8.html
        http://udacity.com/python/language7.html
    http://udacity.com/python/language9.html
    http://udacity.com/pythons.html

As you can see each search result for keywords "python language" is followed by a list of strongly connected (interlinked) web pages.

I think my code provides an interesting extension of what I have learned in the CS101 class without additional complexity. 

I wish Google had such a feature :)

**Code Repository**

https://github.com/dracco/CS101/blob/master/search_with_scc.py

**Members**

apliszka


  [1]: https://github.com/dracco/CS101/raw/master/web_graph.png