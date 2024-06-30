from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from ShareJourneysApp import serializers, paginators, perm
from ShareJourneysApp.models import *
from rest_framework.decorators import action
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import joblib
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from pyvi import ViTokenizer
# Tải các tài nguyên cần thiết cho tiếng Việt (cần thực hiện lần đầu tiên)

# Tải các tài nguyên cần thiết cho tiếng Việt (cần thực hiện lần đầu tiên)


from ShareJourneysApp.serializers import ReportSerializer, ChangePasswordSerializer


def index(request):
    return render(request, 'index.html', context={'name': 'Tuan'})


# content_check/views.py


# Tải mô hình
model_path = os.path.join(os.path.dirname(__file__), 'content_model.pkl')
model = joblib.load(model_path)
import re


def preprocess_text(text):
    # Xóa các ký tự đặc biệt, các số và các dấu câu
    text = re.sub(r'[^a-zA-ZÀ-Ỹà-ỹ0-9\s]', '', text)
    # Xóa các khoảng trắng thừa
    text = ' '.join(text.split())
    print(text)
    return text


def preprocess_text_with_pyvi(text):
    # Tách từ với pyvi
    words = ViTokenizer.tokenize(text)
    print("dada", words)
    # Loại bỏ các ký tự đặc biệt và số
    words = ' '.join([word for word in words.split() if word.isalpha()])
    return words


@csrf_exempt
def xet_duyet(request):
    context = {}
    # if request.method == 'POST':
    # URL của API khác để fetch nội dung bài viết
    # api_url = request.POST.get('api_url', '')
    #
    # # Gọi API để lấy nội dung bài viết
    # response = requests.get(api_url)
    # if response.status_code == 200:
    #     article_text = response.text
    # else:
    #     article_text = ''
    #     context['error'] = 'Không thể lấy nội dung từ API'
    #
    # if article_text:
    #     # Dự đoán tỉ lệ nội dung nhạy cảm
    print(model);
    text = preprocess_text("Vũng Tàu có bãi biễn đẹp ghê mà không ai đi thì tiếc lắm nha!!")
    print(text)
    probability = model.predict_proba([text])[0][1]
    # else:
    #     probability = None

    # Thêm kết quả vào context
    print(probability)
    threshold = 0.6
    if probability >= threshold:
        print(f"Văn bản '{text}' có xác suất nhạy cảm là: {probability:.2f}")
        print("Được xem xét là văn bản nhạy cảm.")
    else:
        print(f"Văn bản '{text}' có xác suất nhạy cảm là: {probability:.2f}")
        print("Được xem xét là văn bản không nhạy cảm.")
    context['probability_of_sensitive_content'] = probability
    # context['article_text'] = article_text

    return render(request, 'xetduyet.html', context)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Old password validation is already handled in serializer
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(username=email)
                new_password = serializer.validated_data['new_password']
            except User.DoesNotExist:
                return Response({"error": "Người dùng với địa chỉ email này không tồn tại."},
                                status=status.HTTP_404_NOT_FOUND)

            # Tạo mật khẩu tạm thời
            user.set_password(new_password)
            user.save()

            # Trả về mật khẩu tạm thời
            return Response({"detail": "Đổi mật khẩu thành công"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPostUser:
    @staticmethod
    def get_post_user(request, user):
        posts = Posts.objects.filter(user_NV=user, state=None).order_by('-id')
        paginator = paginators.UserPostsPaginator()
        page = paginator.paginate_queryset(posts, request)
        if page is not None:
            serializer = serializers.PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.PostSerializer.data)


from oauth2_provider.models import AccessToken


# Truy vấn access token của user


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    print("vao user")
    queryset = User.objects.filter(is_active=True)
    print("vao user lan 1")
    serializer_class = serializers.UserSerializer
    print("vao user lan 2")
    parser_classes = [MultiPartParser, ]
    print("vao user lan 3")

    @staticmethod
    def get_access_token(user):
        access_token = AccessToken.objects.filter(user=user).first()
        return access_token

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], url_path="loginStaff", detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=400)

        user = User.objects.filter(username=username).first()
        access_token = self.get_access_token(user)
        if not user:
            return Response({'error': 'User not found'}, status=404)

        if not user.is_staff:
            return Response({'error': 'Unauthorized access'}, status=403)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=401)
        if not access_token:
            return Response({'error': 'Access token not found'}, status=status.HTTP_404_NOT_FOUND)
        serialized_user = serializers.UserSerializer(user).data
        response_data = {
            'user': serialized_user,
            'access_token': access_token.token,
            'expires': access_token.expires,
        }
        # If authentication is successful, serialize the user data
        return Response(response_data)

    @action(methods=['get'], url_path='postsXetDuyet', detail=True,
            permission_classes=[IsAuthenticated])  # user/id/posts: cho xem trang cá nhan ng khac
    def get_posts_userNV(self, request, pk=None):
        user = self.get_object()
        print(user)
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Kiểm tra xem người dùng có phải là nhân viên không
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        return GetPostUser.get_post_user(request=request, user=user)

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()
        return Response(serializers.UserSerializer(user).data)


def predict_sensitive_content(text):
    print("adjasdas", text)
    processed_text = preprocess_text(text)
    print("dadads", processed_text)
    probability = model.predict_proba([processed_text])[0][1]
    print(probability)
    return probability


class PostViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Posts.objects.prefetch_related('tags')
    serializer_class = serializers.PostDetailSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.PostDetailSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ['add_comments', ' add_comment_reply', 'add_rating', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # Check dao van cua bai post chi dinh
    @action(methods=['get'], url_path='checkBaiViet', detail=True,
            description="Lay 1 bai viet kem so luong rep voi cai dau tick")
    def check_BaiViet(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        content = instance.content

        # Check sensitive content for title and content
        title_prob = predict_sensitive_content(title) if title else 0
        content_prob = predict_sensitive_content(content) if content else 0
        print(title_prob, content_prob)
        # Determine if the post is sensitive based on a threshold
        threshold = 0.6
        is_sensitive = (
                title_prob >= threshold or
                content_prob >= threshold
        )
        response_data = self.serializer_class(instance).data
        response_data['sensitive_content_probabilities'] = {
            'title': title_prob,
            'content': content_prob,
        }
        response_data['is_sensitive'] = is_sensitive

        return Response(response_data)

    @action(methods=['get'], url_path='comment', detail=True,
            description="Lay ds commet kem so luong rep voi cai dau tick")
    def get_comments(self, request, pk):
        comments = self.get_object().comments_set.select_related('user').order_by('-id')
        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=["patch"], url_path="updatePost", detail=True, description="cập nhật bài post để khóa comment")
    def update_post(self, request, pk):
        print("Vo xem")
        try:
            lc = Posts.objects.get(id=pk)
            print(lc.active)
            if lc:
                print("Vo cap nhat active")
                lc.active = not lc.active
                lc.save()
        except Exception:
            return Response({'status': False, 'message': 'Bài post không tìm thấy'})

        return Response(serializers.PostDetailSerializer(lc).data)

    @action(methods=["patch"], url_path="updateXetDuyetPost", detail=True,
            description="cập nhật bài post để xét duyêt post")
    def update_XetDuyetPost(self, request, pk):
        print("Vo xem")
        try:
            lc = Posts.objects.get(id=pk)
            print(lc.state)
            if lc:
                print("Vo cap nhat active")
                lc.state = request.data.get("state")
                lc.save()
        except Exception:
            return Response({'status': False, 'message': 'Bài post không tìm thấy'})

        return Response({'status': True, 'message': 'Cập nhật trạng thái thành công'})

    @action(methods=['post'], url_path='comments', detail=True, description="Lưu comment của user đã comment")
    def add_comment(self, request, pk):
        c = self.get_object().comments_set.create(content=request.data.get('content'),
                                                  user=request.user)
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='rates', detail=True,
            description="Lưu rating của user đó thuộc bài đăng đó")
    def add_rating(self, request, pk):
        c = self.get_object().rating_set.create(rate=request.data.get('rate'),
                                                user=request.user)
        return Response(serializers.RatingSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='comments/(?P<comment_id>[0-9]+)/tick', detail=True,
            description='Lưu ds nguời đi cùng được tick đồng thời lưu tạo mới tick ')
    def travelCompanion(self, request, pk, comment_id):
        # if comment_id:
        #     li, created =CommentTick.objects.get_or_create(cmtTick=)
        #     if not created:
        #         li.active = not li.active
        #         li.save()
        comment = Comments.objects.get(id=comment_id)
        if request.method.__eq__("POST"):
            print("vao duoc")
            print(self.get_object())
            print(request.user)
            li, created = TravelCompanion.objects.get_or_create(posts=self.get_object(),
                                                                user=User.objects.get(id=request.data.get("idUser")),
                                                                active=False)
            lc, created_tic = CommentTick.objects.get_or_create(cmtTick=comment)
            print("chay duoc",created_tic)
            # cap nhat cai active
            if not created_tic:# có r thì vào update
                print("dada",created_tic,"dadadad",lc.active)
                print("vo dadada")
                lc.active = not lc.active
                lc.save()
                print("lc",lc.active)
                if not lc.active: # active của tick là false
                    print("voduoc xoa")
                    travelCompanion_Del = self.get_object().travelcompanion_set.filter(
                        user=User.objects.get(id=request.data.get("idUser")))
                    travelCompanion_Del.delete()
                print("thoat dc")

            return Response(serializers.PostDetailSerializer(self.get_object()).data)

    @action(methods=["delete"], url_path='travelCompanion', detail=True,
            description="Xoa danh người đi cùng của bài post đó và có thể dùng trong trường hợp hủy lời mời")
    def del_travelCompanion(self, request, pk):
        if request.method.__eq__("DELETE"):
            # print("vao xoa user di cung")
            # print(self.get_object())
            # travelCompanion_Del = self.get_object().travelcompanion_set.filter(
            #     user=User.objects.get(id=request.data.get("idUser")))
            # print(travelCompanion_Del)
            # travelCompanion_Del.delete()

            comments = self.get_object().comments_set.filter(user=User.objects.get(id=request.data.get("idUser")))
            try:
                CommentTick.objects.filter(cmtTick__in=comments).update(active=False)

            except ObjectDoesNotExist:
                return Response({"error": "Không tìm thấy CommentTick cho comment"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], url_path="updateAcceptPost", detail=True,
            description="cập nhật active cuả người đi cùng và thêm dữ lieu cho bang userroute")
    def update_UserRoute(self, request, pk):
        print("Vo xem")
        try:
            lc = self.get_object().travelcompanion_set.filter(user=request.user)
            print(lc.id)
            lc.active =True
            if request.data.get("id_NoiDen"):
                 id_NoiDi= DiaDiemDungChan.objects.filter(id=request.data.get("id_NoiDi"))
            if request.data.get("id_NoiDen"):
                id_NoiDen= DiaDiemDungChan.objects.filter(id=request.data.get("id_NoiDen"))
            if id_NoiDi and id_NoiDen:
                userRoute=UserRoute.objects.get_or_create(id_noiDi=id_NoiDi,id_noiDen=id_NoiDen,id_User=lc.id)
          
            lc.save()
        except Exception:
            return Response({'status': False, 'message': 'Bài post không tìm thấy'})

        return Response({'status': True, 'message': 'Cập nhật trạng thái thành công'})



class LocalViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Local.objects.all()
    serializer_class = serializers.LocalSerializer


class TransportationViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Transportation.objects.all()
    serializer_class = serializers.TransportationsSerilializer


class TagViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class PictureViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = JourneyPictures.objects.all()
    serializer_class = serializers.ImageSerializer


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer

    # permission_classes = [perm.CommentOwner]
    def get_permissions(self):
        if self.action in ['add_and_get_comment_reply'] and self.request.POST:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post', 'get'], url_path='replies', detail=True,
            description="Lay va luu danh sach rep cua 1 comment")
    def add_and_get_comment_reply(self, request, pk):
        comment = self.get_object()
        if request.method.__eq__('POST'):
            reply = CommentReply.objects.create(cmtRep=comment, user=request.user)
            return Response(serializers.ReplySerializer(reply).data, status=status.HTTP_201_CREATED)
        if request.method.__eq__('GET'):
            rep = comment.comment_reply.all().order_by('-id')
            return Response(serializers.ReplySerializer(rep, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)


class ReportViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Reports.objects.all()
    serializers_class = serializers.ReportSerializer

    def get_serializer_class(self):
        return ReportSerializer

    @action(methods=['post'], url_path='userReport', detail=True, description="Lưu user nào bị report nào")
    def UserReport(self, request, pk):
        print(request.data.get("idUser"))
        ur_create = Users_Report.objects.create(report=self.get_object(),
                                                user=User.objects.get(id=request.data.get("idUser")))
        return Response(status=status.HTTP_201_CREATED)


class SendEmail(APIView):
    def post(self, request):
        if request.method == 'POST':
            if request.data.get("user"):
                client_email = "tuannguyen13@gmail.com"
                email = request.data
                nd = email.get('nd') + "\n" + "Người Vi pham:" + email.get('user')
                print(email)
                email_word = EmailMessage('Report user',
                                          nd,
                                          client_email,
                                          [settings.EMAIL_HOST_USER])
                email_word.send(fail_silently=False)
                return Response({'status': True, 'message': 'Email send sucesss'})
            if request.data.get("emailUser"):
                email = request.data
                client_email = request.data.get("emailUser")
                user = User.objects.get(username=client_email)
                if not user:
                    return Response({'status': True, 'message': 'Email khong ton tai'})
                print("dada", client_email)
                nd = email.get('nd')
                print(email)
                email_word = EmailMessage('Reset Password',
                                          nd,
                                          settings.EMAIL_HOST_USER,
                                          [client_email])
                email_word.send(fail_silently=False)
                return Response({'status': True, 'message': 'Email send sucesss'})
            if request.data.get("emailClient") and request.data.get("ghiChu"):
                print("dadadsa",request.data.get("emailClient"))
                email = request.data
                client_email = request.data.get("emailClient")
                user = User.objects.get(username=client_email)
                if not user:
                    return Response({'status': True, 'message': 'Email khong ton tai'})
                print("dadadada", client_email)
                nd = email.get('ghiChu') + "\n" + "Cảm ơn bạn đã xem email này"
                print(email)
                email_word = EmailMessage('XÉT DUYỆT BÀI ĐĂNG HÀNH TRÌNH'+ " "+ request.data.get("title"),
                                          nd,
                                          settings.EMAIL_HOST_USER,
                                          [client_email])

                email_word.send(fail_silently=False)
                return Response({'status': True, 'message': 'Email send sucesss'})
