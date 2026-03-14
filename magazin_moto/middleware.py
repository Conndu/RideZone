from .views import Accesare, GLOBAL_LOG, GLOBAL_PATH_COUNTS

class NewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

            paths_to_log = ['/', '/info', '/log']

            if any(request.path_info.startswith(p) for p in paths_to_log):

                log_entry = Accesare(request)

                GLOBAL_LOG.append(log_entry)

                GLOBAL_PATH_COUNTS[log_entry.base_path] += 1
 

            request.proprietate_noua=17       
            response = self.get_response(request)      

            response['header_nou'] = 'valoare'
            if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
                content = response.content.decode('utf-8')

                response['Content-Length'] = len(response.content)
        
            return response
        