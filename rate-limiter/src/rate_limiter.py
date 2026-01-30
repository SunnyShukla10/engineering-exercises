from typing import Dict, Tuple, Optional
from starter import *

class RateLimiter:
    def __init__(self, endpoint_policies: Dict[str, Tuple[int, int]]):
        '''
        This initalizes the policies of each endpoint. 

        The format will be as follows {endpoint: (number of calls , time)}  --> {"/search" : (3, 10)} = "/search" can be called max of 3 times in 10 seconds 
        '''
        self.policies = endpoint_policies
        

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


        # Case: Endpoint is in policies
        # If count of this request has not been more than the max time then  
        #   return true
        # if count of the request surpassed the max time per request then
        #   return false         
