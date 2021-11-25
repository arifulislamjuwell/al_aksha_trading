from course.models import Category

def host(request):
    return "{}/media/".format(request.META['HTTP_HOST'])


def category_info(category_id, request):
    result_dic={}
    category= Category.objects.get(id= category_id)
    scheme = "https://" if request.is_secure() else "http://"

    result_dic['name']= category.name
    result_dic["image"]= scheme + host(request)+ str(category.image) if category.image else ''
    result_dic['course_count']= len(category.courses.all())
    return result_dic

