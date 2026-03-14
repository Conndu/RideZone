# magazin_moto/request_logger.py
import datetime
from collections import Counter

class GlobalAccessLog:

    log = []
    counter = 0
    path_counts = Counter() # Pentru statistici

    @classmethod
    def add_access(cls, request):
        # Definim paginile pe care le monitorizăm
        paths_to_log = ['/', '/info', '/log']
        
        # Verificăm dacă request.path începe cu una din rute
        if any(request.path.startswith(p) for p in paths_to_log):
            cls.counter += 1
            
            # Pentru statistici, folosim calea de bază (fără query params)
            base_path = request.path.split('?')[0]

            log_entry = {
                'id': cls.counter,
                'path': request.path, # Calea completă cu query string
                'base_path': base_path, # Doar calea (/info, /log, /)
                'timestamp': datetime.datetime.now(),
                'method': request.method,
                'params': request.GET.copy(), # Salvăm o copie a parametrilor
            }
            cls.log.append(log_entry)
            cls.path_counts[base_path] += 1

    @classmethod
    def get_log(cls):
        # Returnăm o copie
        return cls.log[:]

    @classmethod
    def get_count(cls):
        return len(cls.log)

    @classmethod
    def get_stats(cls):
        if not cls.path_counts:
            return None, None
        
        # .most_common() returnează o listă de tupluri (item, count)
        most_common = cls.path_counts.most_common()
        most_accessed = most_common[0][0]
        least_accessed = most_common[-1][0]
        return most_accessed, least_accessed

    @classmethod
    def get_logs_by_ids(cls, id_list):
        # Căutare eficientă folosind un dicționar
        logs_by_id_map = {entry['id']: entry for entry in cls.log}
        
        found_logs = []
        for id_val in id_list:
            log = logs_by_id_map.get(id_val)
            if log:
                found_logs.append(log)
        return found_logs