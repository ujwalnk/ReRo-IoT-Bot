import requests

def push_2_server(value: str, type: str):
    """
    Push value to the server with type
    
    @param:
        - value (str): Value to be sent
        - type (str): Type of value being sent (error / print)

    """

    try:

        url = ""

        if type == "error":
            url = "http://localhost:8080/iot/dump"
        elif type == "print":
            url = "http://localhost:8080/iot/dump"

        print("URL", url)

        params = {"data": value}

        print(params)
        response = requests.get(url, params=params)
        print(response)
        
        if response.status_code != 200:
            print("Unable to print data")
        
        return response.json()
    except Exception as e:
        print(e)