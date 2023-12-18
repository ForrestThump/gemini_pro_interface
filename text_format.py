class TextFormatter:
    def __init__(self, user_name:str = "user", model_name:str = "model") -> None:
        self.user_name: str = user_name
        self.model_name: str = model_name
        
    def response_to_text(self, response) -> str:
        response_str = ""        

        for chunk in response:
            response_str += ("_"*80 + "\n")
            response_str += "\n(" + self.model_name + "): \n"
            response_str += chunk.text
            response_str += ("\n"+"_"*80 + "\n")

        return response_str
    
    def query_to_text(self, query:str) -> str:
        query_str = ("_"*80 + "\n")
        query_str += "\n(" + self.user_name + "): \n"

        query_str += query

        query_str += ("\n"+"_"*80 + "\n")
        
        return query_str
        