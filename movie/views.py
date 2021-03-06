from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
# from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
# from apps.clients.models import OrgSchema
from movie.models import Picture
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
# from json import json_util
import json

from django.template import RequestContext
# def add(request):
#     #logic
#     return render_to_response("category/add.html", {"form": form}, 
#         context_instance = RequestContext(request))    


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


permission_classes = (IsAuthenticated,)
def getMovies(request):
    print(request.GET["id"])
    id_obj=request.GET["id"]
    print(request.user)
    print(request.user.get_user_permissions())
    result={}
    result_obj=None
    data=[]

    try:
    
        if(str(id_obj).lower()=='all'):
            '''
            To Get all The Movies.
            Api_Endpoint: http://127.0.0.1:8000/movie/getpictures/?id=all
            Response: Object with List Of Data

            '''
            # data = list(Picture.objects.values())  # wrap in list(), because QuerySet is not JSON serializable
            data = Picture.objects.all()
            print(data)
            result_obj=data
            print('endd')
            
        else:
            print('else')
            '''
                To Get Movies By id.
                Api_Endpoint: http://127.0.0.1:8000/movie/getpictures/?id=1
                Response: Object with List Of Data
                
            '''
            print(id_obj)
            data_by_id= Picture.objects.get(id=id_obj)
            # data_by_id= Picture.objects.get(id=id_obj)
            # Picture.objects.filter(genre__contains = str(search_genre)).values()
            data.append({'id':data_by_id.id,'name':data_by_id.name,'director':data_by_id.director,'genre':data_by_id.genre,'imdb_score':data_by_id.imdb_score,'dire99popularity':data_by_id.dire99popularity})
            result_obj=data
        # result['data']=data
        
        # print(User.objects.all())
        template="movie.html"
    except Exception as e:
        print('Error Occured, please try again later!')
        template="error.html"
    finally:

        return render(request,template,{'results':result_obj})

permission_classes = (IsAuthenticated,)
def searchMovie(request):
    action=request.GET['action']
    result={}
    result_obj=None
    status=None
    '''
        To check whether user belongs to staff
        
    '''
    if(User.objects.get(username=request.user).is_staff):
        # result={}
        
        if(str(action).lower()=='search_by_name'):
            
            '''
                To Search MOvies By Name.
                Api_Endpoint: http://127.0.0.1:8000/movie/searchPictures/?action=search_by_name&search_string=test
                Response: Object with List Of Matchng Data

            '''

           
            try:
                print('search_by_name')
                # search_string=request.data['search_string']
                search_string=request.GET['search_string']
                print(search_string)
                # f=Picture.objects.filter(name__contains = search_string).values()
                f=Picture.objects.filter(name__contains = search_string).all()
                # print(list(f))
                print(f)
                result['movies']=f
                result_obj=f
                if(f):
                    result['status']='Got Your ' 
                else:
                    result['status']='No Record For your Searched '
                template="moviesearch.html"
            except:
                template="error.html"
                result['status']='Something Went Wrong!!'
                pass
            finally:
                status=result['status']
                print('in finally')
                print(result_obj)
                # return Response(result,status=status.HTTP_200_OK)
                return render(request,template,{'results':result_obj,'status':status})

        
        elif(str(action).lower()=='search_by_genre'):
            '''
                To Search MOvies By Genre.
                Api_Endpoint: http://127.0.0.1:8000/movie/searchPictures/?action=search_by_genre&search_string=comedy
                Response: Object with List Of Matchng Data

            '''
            try:
                print('in search genre')
                search_genre=request.GET['search_string']
                # res=Picture.objects.filter(genre__contains = str(search_genre)).values()
                res=Picture.objects.filter(genre__contains = str(search_genre)).all()
                # print(list(res))
                # print(res)
                result['data']=res
                result_obj=res
                if(res):
                    result['status']='Got Your'
                else:
                    result['status']='No Record For your Searched '
                template="moviesearch.html"
            except Exception as e:
                print(e)
                template="error.html"
                result['status']='Something Went Wrong'
                pass
            finally:
                status=result['status']
                print('in finally')
                # return Response(result,status=status.HTTP_200_OK)
                print(result_obj)
                return render(request,template,{'results':result_obj,'status':status})
        

    else:
        result['status']='User Not Authenticated to perform action'
        # return Response(result,status=status.HTTP_200_OK)
        return render(request,"error.html",{'result':result})

    # return Response(result,status=status.HTTP_200_OK)

permission_classes = (IsAuthenticated,)
def createMovies(request):
    print('request,request',request)
    print('request,request',request.user)
    action=request.GET['action']
    result={}
    '''
        To check whether user belongs to staff
        
    '''
    print('hereree')
    print('hereree',request.user)
    print(User.objects.get(username=request.user).is_superuser)
            
    if(User.objects.get(username=request.user).is_superuser):
        '''
            To add movie 
            Api_Endpoint: http://127.0.0.1:7000/movie/createPictures/?action=create
            Request Body: {
                                "action":"create",
                                "formdata":[{
                                    "name":"About Time",
                                    "director":"Richrd Curtis",
                                    "genre":"{'comedy','drama'}",
                                    "dire99popularity":"98",
                                    "imdb_score":"7.8"
                                }]
                            }
            Response: About Time Successfully added!

    
        '''
        
        if(action=='create'):
            try:
                # print(request.data['formdata'])
                # print(json.dumps({"comedy":True}))
                formdata=[{
                                        "name":"test4",
                                        "director":"test",
                                        "genre":"{'comedy','adventure'}",
                                        "dire99popularity":"56",
                                        "imdb_score":"9"
                                    }]
                # formdata=request.data['formdata']
                for item in formdata:
                    y=Picture.objects.create(name = item['name'],director=item['director'],genre=item['genre'],dire99popularity=item['dire99popularity'],imdb_score=item['imdb_score'])
                    if(y):
                        result['status']=item['name']+' Successfully added!'
                    
                # Picture.save()
                template="create.html"
            except Exception as e:
                result['status']=e
                print(e)
                template="error.html"
                pass
            finally:
                # Picture.save()
                status=result['status']
                print('in finally')
                return render(request,template,{'status':status})
                    
    else:
        
        '''
            User Authentication Failed!!!
        
        '''
        result['status']='User Not Authenticated to perform action'
        return render(request,"authenticate.html",{'result':result})
    
        # return Response(result,status=status.HTTP_200_OK)

    # return Response(result,status=status.HTTP_200_OK)

permission_classes = (IsAuthenticated,)
def deleteMovie(request):
    result={}
    result_obj=None
    status=None
    try:
        '''
            Validation Check to delete movie by id (only superuser can delete)
            Api EndPoint: http://127.0.0.1:7000/movie/deletePictures/?id=6
            Response: Movie_Name deleted successfully!
        '''
        if(User.objects.get(username=request.user).is_superuser):
            print('delete')
            delete_id=request.GET['id']
            print(delete_id)
            # Not using get as it results in exception if id does not exists
            res=Picture.objects.filter(id = delete_id).first()
            print(res)
            if(res):
                delete_status=res.delete()
                print(delete_status)
                result['status']=res.name+' deleted successfully!'
            else:
                result['status']='Record does not exists!'
            template="delete.html"
        else:
            result['status']='User Not Authenticated'
            template="authenticate.html"
        
    except Exception as e:
        print(e)
        template="error.html"
        result['status']='Something Went Wrong'
        pass
    finally:
        status=result['status']
        print('in finally')
        # return Response(result,status=status.HTTP_200_OK)
        return render(request,template,{'results':result,'status':status})




# POSTMAN
class MyPicture(APIView):

    """
            RegiRegister User Activatestration 
            Required Parameter:-
            user_id -- (string) required
            verifycode -- (string) required            
            return Response

    """
    print('dsd')
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print(request.GET["id"])
        id_obj=request.GET["id"]
        print(request.user.get_user_permissions())
        result={}
        data=[]
        
        if(str(id_obj).lower()=='all'):
            '''
            To Get all The Movies.
            Api_Endpoint: http://127.0.0.1:7000/movie/getpictures/?id=all
            Response: Object with List Of Data

            '''
            data = list(Picture.objects.values())  # wrap in list(), because QuerySet is not JSON serializable
        
            
        else:
            '''
                To Get Movies By id.
                Api_Endpoint: http://127.0.0.1:7000/movie/getpictures/?id=1
                Response: Object with List Of Data
                
            '''
            data_by_id= Picture.objects.get(id=id_obj)
            data.append({'id':data_by_id.id,'name':data_by_id.name,'genre':data_by_id.genre,'imdb_score':data_by_id.imdb_score,'dire99popularity':data_by_id.dire99popularity})
        result['data']=data
        # print(User.objects.all())
        # return Response(result,"db.html",status=status.HTTP_200_OK)
        return render(request,"index.html",{'result':Picture.objects.all()})

    permission_classes = (IsAuthenticated,)
    def post(self, request):
        action=request.data['action']
        result={}
        '''
            To check whether user belongs to staff
            
        '''
        if(User.objects.get(username=request.user).is_staff):
            # result={}
            
            if(str(action).lower()=='search_by_name'):
                '''
                To search movie by name
                Api_Endpoint: http://127.0.0.1:7000/movie/getpictures/
                Request Body: {
                                    "action":"search_by_name",
                                    "search_string":"scary",
                                }
                Response: Object with List Of Matching Movies

            
                '''
                try:
                    print('search_by_name')
                    search_string=request.data['search_string']
                    print(search_string)
                    f=Picture.objects.filter(name__contains = search_string).values()
                    print(list(f))
                    result['movies']=f
                    if(f):
                        result['status']='Success' 
                    else:
                        result['status']='No Record Found!'
                    
                except:
                    result['status']='Something Went Wrong'
                    pass
                finally:
                    print('in finally')
                    return Response(result,status=status.HTTP_200_OK)

            
            elif(str(action).lower()=='search_by_genre'):
                '''
                To search movie by genre
                Api_Endpoint: http://127.0.0.1:7000/movie/getpictures/
                Request Body: {
                                    "action":"search_by_genre",
                                    "search_string":"scary",
                                }
                Response: Object with List Of Matching Movies

            
                '''
                try:
                    print('in search genre')
                    search_genre=request.data['search_string']
                    res=Picture.objects.filter(genre__contains = str(search_genre)).values()
                    # print(list(res))
                    # print(res)
                    result['data']=res
                    if(res):
                        result['status']='Entry found!'
                    else:
                        result['status']='No Record Found!'
                except Exception as e:
                    print(e)
                    result['status']='Something Went Wrong'
                    pass
                finally:
                    print('in finally')
                    return Response(result,status=status.HTTP_200_OK)
            

            '''
                To verify only super user can add movies
            
            '''
            if(User.objects.get(username=request.user).is_superuser):
                '''
                    To add movie 
                    Api_Endpoint: http://127.0.0.1:7000/movie/getpictures/
                    Request Body: {
                                        "action":"create",
                                        "formdata":[{
                                            "name":"About Time",
                                            "director":"Richrd Curtis",
                                            "genre":"{'comedy','drama'}",
                                            "dire99popularity":"98",
                                            "imdb_score":"7.8"
                                        }]
                                    }
                    Response: About Time Successfully added!

            
                '''
                if(action=='create'):
                    try:
                        print(request.data['formdata'])
                        # print(json.dumps({"comedy":True}))
                        for item in request.data['formdata']:
                            y=Picture.objects.create(name = item['name'],director=item['director'],genre=item['genre'],dire99popularity=item['dire99popularity'],imdb_score=item['imdb_score'])
                            if(y):
                                result['status']=item['name']+' Successfully added!'
                            
                        # Picture.save()
                    except Exception as e:
                        result['status']=e
                        print(e)
                        pass
                    finally:
                        # Picture.save()
                        print('in finally')
                        return Response(result,status=status.HTTP_200_OK)
                    try:
                        print('search_by_name')
                        search_string=request.data['search_string']
                        print(search_string)
                        f=Picture.objects.filter(name__contains = search_string).values()
                        print(list(f))
                        result['movies']=f
                        if(f):
                            result['status']='Success' 
                        else:
                            result['status']='No Record Found!'
                        
                    except:
                        result['status']='Something Went Wrong'
                        pass
                    finally:
                        print('in finally')
                        return Response(result,status=status.HTTP_200_OK)
            else:
                
                '''
                    User Authentication Failed!!!
                
                '''
                result['status']='User Not Authenticated to perform action'
                return Response(result,status=status.HTTP_200_OK)
        else:
            result['status']='User Not Authenticated to perform action'
            return Response(result,status=status.HTTP_200_OK)

        # return Response(result,status=status.HTTP_200_OK)

    permission_classes = (IsAuthenticated,)
    def delete(self,request):
        result={}
        try:
            '''
                Validation Check to delete movie by id (only superuser can delete)
                Api EndPoint: http://127.0.0.1:7000/movie/getpictures/?id=6
                Response: Movie_Name deleted successfully!
            '''
            if(User.objects.get(username=request.user).is_superuser):
                print('delete')
                delete_id=request.GET['id']
                print(delete_id)
                # Not using get as it results in exception if id does not exists
                res=Picture.objects.filter(id = delete_id).first()
                print(res)
                if(res):
                    delete_status=res.delete()
                    print(delete_status)
                    result['status']=res.name+' deleted successfully!'
                else:
                    result['status']='record does not exists'
            else:
                result['status']='User Not Authenticated'
            
        except Exception as e:
            print(e)
            result['status']='Something Went Wrong'
            pass
        finally:
            print('in finally')
            return Response(result,status=status.HTTP_200_OK)

    permission_classes = (IsAuthenticated,)
    def put(self,request):
        result={}
        '''
            To Update Exsting Movie
            Api EndPoint: http://127.0.0.1:7000/movie/getpictures/?id=19
            Request Body:{
                            "formdata":{
                                "name":"About Time",
                                "director":"Richrd Curtis",
                                "genre":"{'comedy','drama'}",
                                "dire99popularity":"56",
                                "imdb_score":"8"
                            }
                        }
            Response:Record updated successfully

        '''

        try:
            if(User.objects.get(username=request.user).is_superuser):
                print('update')
                print(request.data['formdata'])
                formdata=request.data['formdata']
                update_id=request.GET['id']
                print(update_id)
                # Not using get as it results in exception if id does not exists
                res=Picture.objects.filter(id = update_id).first()
                print(res)
                if(res):
                    print('1')
                    res.name=formdata['name']
                    res.director=formdata['director']
                    res.genre=formdata['genre']
                    res.imdb_score=formdata['imdb_score']
                    res.dire99popularity=formdata['dire99popularity']
                    update_status=res.save()
                    # print(update_status)
                    result['status']=' Record updated successfully!'
                else:
                    result['status']='record does not exists'
            else:
                result['status']='User Not Authenticated'
            
        except Exception as e:
            print(e)
            result['status']='Something Went Wrong'
            pass
        finally:
            print('in finally')
            return Response(result,status=status.HTTP_200_OK)


'''
    Formating Time As Required If Necessary(for diplay purpose)
'''
def formatTime(self,time):
        formattedTime = time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d-%b-%Y %I:%M %p') if(time) else 'NA'
        return formattedTime