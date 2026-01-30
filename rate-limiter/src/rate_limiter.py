from typing import Dict, Tuple, Optional
from src.models import Request
from collections import deque, defaultdict

class RateLimiter:
    def __init__(self, endpoint_policies: Dict[str, Tuple[int, int]]):
        """
        endpoint_policies maps endpoint -> (max_requests, window_seconds)

        If an endpoint is NOT present in endpoint_policies, it is unlimited.
            Example:
                {
                "/search": (3, 10),
                "/checkout": (2, 60),
                }
        """
        self.policies: Dict[str, Tuple[int, int]] = endpoint_policies
        
        # Maps each (user,endpoint) to a bucket deque (with just timestamps) which allows to see 
        #   if they are blocked or not for that endpoint
        self.user_calls: defaultdict[Tuple[str, str], deque] = defaultdict(deque)
    
    # -----------------------------------
    # HELPERS
    # -----------------------------------

    def _get_request_data(self, req: Request) -> Tuple[str, str, int]:
        return (req.user_id, req.endpoint, req.timestamp)

    def _add_user_endpoint(self, user_id: str, endpoint: str, ts: int):
        user_key = (user_id, endpoint)
        self.user_calls[user_key].append((ts))

    # -----------------------------
    # API Function
    # -----------------------------
    
    def allow(self, req: Request) -> bool:
        '''
        Given a req, return true if the request is allowed or not. If req.endpoint is not in the policies, its able to be called unlimited amount of times  
    
        Parameter req is of type Request and it has info about user_id endpoint, and timestamp
        
        Returns:
            - True if allowed
            - False if not allowed 
        '''

        if req.endpoint not in self.policies:
            return True # unlimited allows

        # Request data 
        user_id, endpoint, ts = self._get_request_data(req)

        if (user_id, endpoint) not in self.user_calls:
            # First time calling endpoint
            self._add_user_endpoint(user_id, endpoint, ts)
            return True

        all_timestamps = self.user_calls[(user_id, endpoint)]
        max_requests = self.policies[endpoint][0]
        time_window = self.policies[endpoint][1]

        if (ts - all_timestamps[0]) < time_window:
            # check if it is able to be added            
            if len(all_timestamps) >= max_requests:
                return False
            # add and return
            self._add_user_endpoint(user_id, endpoint, ts)
            return True

        else:
            # cleanup process and then check
            while all_timestamps and (ts - all_timestamps[0]) >= time_window:
                all_timestamps.popleft()

            if len(all_timestamps) > max_requests:
                return False
            # add and return
            self._add_user_endpoint(user_id, endpoint, ts)
            return True
