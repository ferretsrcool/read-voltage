import httplib2

def request(url, method):
    """HTTP request function."""
    try:
      h = httplib2.Http(".cache")
      return h.request(url, method)
    except Exception as e:
      pass