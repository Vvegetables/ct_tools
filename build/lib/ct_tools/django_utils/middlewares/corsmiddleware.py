class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        try:
            response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN") #cors use
        except:
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS" 
            response["Access-Control-Max-Age"] = 1000 
            response["Access-Control-Allow-Headers"] = "*" 

        # Code to be executed for each request/response after
        # the view is called.

        return response