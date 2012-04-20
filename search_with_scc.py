#
# Exam search functions
#
def multi_lookup(index, query):
    keywords = query
    urls = []
    for match in index[keywords[0]]:
        if len(keywords) == 1:
            union(urls, [match[0]])
        else:
            union(urls, find(index, keywords[1:], match[1]+1))
    return urls

def find(index, keywords, i):
    matches = []
    for match in index[keywords[0]]:
        if match[1] == i:
            if len(keywords) == 1:
                union(matches, [match[0]])
            else:
                union(matches, find(index, keywords[1:], match[1]+1))
    return matches

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for i in range(len(words)):
        word = words[i]
        add_to_index(index, word, url, i)

def add_to_index(index, keyword, url, i):
    if keyword in index:
        index[keyword].append([url, i])
    else:
        index[keyword] = [[url, i]]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        print "Page not in cache: " + url
        return None

#
# Functions for computing strongly connected components (web pages)
#

# notmalize the graph by adding missing nodes
def normilize_graph(graph):
    normalized_graph = {}
    for u in graph:
        for v in graph[u]:
            if v not in normalized_graph:
                normalized_graph[v] = []
            if u not in normalized_graph:
                normalized_graph[u] = []
            normalized_graph[u].append(v)
    return normalized_graph

# reverse the directed of all graph edges
def reverse_graph(graph):
    reversed_graph = {}
    for u in graph:
        for v in graph[u]:
            if v not in reversed_graph:
                reversed_graph[v] = []
            if u not in reversed_graph:
                reversed_graph[u] = []
            reversed_graph[v].append(u)
    return reversed_graph

# helper function that uses depth first search to timestamp all vertices
def dfs_timestamp(graph, explored, timestamps, i):
    global timestamp
    explored[i] = 1
    for v in graph[i]:
        if v not in explored:
            dfs_timestamp(graph, explored, timestamps, v)
    timestamp += 1
    timestamps[timestamp] = i

# timestamp all vertices of the graph
def timestamp_graph(graph):
    explored = {}
    timestamps = {}
    for v in sorted(graph.keys(), reverse=True):
        if v not in explored:
            dfs_timestamp(graph, explored, timestamps, v)
    return timestamps

# helper fuction that uses depth firts search to set leader vertex of all graph
# verticies
def dfs_leader(graph, explored, leaders, i, leader):
    explored[i] = 1
    leaders[i] = leader
    for v in graph[i]:
        if v not in explored:
            dfs_leader(graph, explored, leaders, v, leader)

# set leaders for all the vertices of the graph
def graph_leaders(graph, timestamps):
    explored = {}
    leaders = {}
    for t in sorted(timestamps.keys(), reverse=True):
        i = timestamps[t]
        if i not in explored:
            leader = i
            dfs_leader(graph,explored, leaders, i, leader)
    return leaders

# Ohh, nooo ... a global variable :(
timestamp = 0

# high level fuction for setting leaders of all graph verticies
def compute_leaders(graph):
    G = normilize_graph(graph)
    Grev = reverse_graph(G)

    timestamps = timestamp_graph(G)

    return graph_leaders(Grev, timestamps)

# sample web geaph with two clustes of pages
# one cluster about python snakes
# the other cluster about python language
cache = {
   'http://udacity.com/pythons.html': """
   python snake
   python language
<a href="http://udacity.com/python/snakes2.html">A</a><br>
<a href="http://udacity.com/python/language6.html">A</a><br>
<a href="http://udacity.com/python/language7.html">A</a><br>
   """,

# cluster about python snakes
   'http://udacity.com/python/snakes1.html': """
   python snake
<a href="http://udacity.com/python/snakes2.html">A</a><br>
   """,
   'http://udacity.com/python/snakes2.html': """
   python snake
<a href="http://udacity.com/python/snakes3.html">A</a><br>
<a href="http://udacity.com/python/snakes4.html">A</a><br>
   """,
   'http://udacity.com/python/snakes3.html': """
   python snake
<a href="http://udacity.com/python/snakes1.html">A</a><br>
   """,
   'http://udacity.com/python/snakes4.html': """
   python snake
   """,

# cluster about python language
   'http://udacity.com/python/language6.html': """
   python language
<a href="http://udacity.com/python/language7.html">A</a><br>
   """,
   'http://udacity.com/python/language7.html': """
   python language
<a href="http://udacity.com/python/language8.html">A</a><br>
<a href="http://udacity.com/python/language9.html">A</a><br>
   """,
   'http://udacity.com/python/language8.html': """
   python language
<a href="http://udacity.com/python/language6.html">A</a><br>
   """,
   'http://udacity.com/python/language9.html': """
   python language
   """,
}

# crawl and index the webpages
index, graph = crawl_web('http://udacity.com/pythons.html')

# find strongly connected web pages
leaders = compute_leaders(graph)

# print "index", index
# print "graph", graph
# print "leaders", leaders

# search
keywords = ['python', 'language']
# keywords = ['python', 'snake']
results = multi_lookup(index, keywords)

search_results = []

for result in results:
    leader = leaders[result]
    connected = []
    for c in leaders.keys():
        if leaders[c] == leader and c != result:
            connected.append(c)
    search_results.append({'url': result, 'related': connected })

# print results
print "Search results for", keywords
for r in sorted(search_results, key = lambda result: len(result['related']),
                reverse=True):
    print r['url']
    if r['related']:
        print "   Strongly connected web pages:"
        for c in r['related']:
            print "   ", c

