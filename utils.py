
def paginate(list_: list, page_num, per_page=9)->list:
    result = list_[(page_num-1)*per_page:(page_num)*per_page]
    return result

def max_split_on_pages(list_: list, per_page=9)->int:
    import math
    max_pages = math.ceil((len(list_)/per_page))
    max_pages = max_pages if max_pages>0 else 1
    return max_pages

def generate_pagination(current_page, max_pages)-> list:
    if max_pages == 1:
        pagination = [1]
        return pagination
    if current_page == 1:
        pagination = [1,2]
    elif current_page == max_pages:
        pagination = [max_pages-1, max_pages]
    else:
        pagination = [current_page-1, current_page, current_page+1]
    return pagination