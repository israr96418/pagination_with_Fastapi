import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,

)

# when get data from 3rd party
data = httpx.get('https://jsonplaceholder.typicode.com/posts')
json_data = data.json()
data_lenght = len(data.json())
print("total number of record", data_lenght)




# for pagination first I used query parameter which is not the best approach
@app.get("/posts")
def Pagination(page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size

    #    dict(store value in the form key:value pair)
    response = {
        'json_data': json_data[start:end],
        'total': data_lenght,
        'count': page_size,
        'pagination': {}
    }

    if end >= data_lenght:
        # it means you are on the last page there is no next page:
        response['pagination']['next'] = None

        if page_num > 1:
            response['pagination']['previous'] = f'/posts?page_num={page_num - 1}&page_size={page_size}'

        else:
            response['pagination']['previous'] = None
    else:
        if page_num > 1:
            response['pagination']['previous'] = f'/posts?page_num={page_num - 1}&page_size={page_size}'
        else:
            response['pagination']['previous'] = None

        response['pagination']['next'] = f'/posts?page_num={page_num + 1}&page_size={page_size}'

    return response
