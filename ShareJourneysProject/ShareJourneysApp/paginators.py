from rest_framework import pagination



class CommentPaginator(pagination.PageNumberPagination):
    page_size = 4
class UserPostsPaginator(pagination.PageNumberPagination):
    page_size =3
    page_size_query_param = 'page_size'