from rest_framework import serializers
from ShareJourneysApp.models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    print("Lưu server")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.avatar:  # Check if avatar field is not None
            rep['avatar'] = instance.avatar.url
        return rep

    def create(self, validated_data):
        print("vao luu duoc")
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data["password"])
        print("vao luu duoc")
        user.save()
        print("pass")

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8, max_length=128)  # Đảm bảo mật khẩu mới có ít nhất 8 ký tự

    def validate_email(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Người dùng với địa chỉ email này không tồn tại.")
        return value


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['picture'] = instance.picture.url

        return rep


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ImageSerializer(ItemSerializer):
    picture = serializers.ImageField()

    # def to_representation(self, instance):
    #     return instance.picture.url
    class Meta:
        model = JourneyPictures
        fields = ["id", "picture"]
class TransportationsSerilializer (serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = ['id','loai']


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id', 'diaChi']
class RouterSerializer(serializers.ModelSerializer):
    id_noiDi = LocalSerializer()
    id_noiDen = LocalSerializer()
    class Meta:
        model =Route
        fields = ['id_noiDi','id_noiDen']


class StopLocalSerializer(serializers.ModelSerializer):
    id_DiaDiem = LocalSerializer()
    class Meta:
        model = DiaDiemDungChan
        fields = ['id_DiaDiem','thoiGianDung']
class JourneySerializer(serializers.ModelSerializer):
    # router
    id_tuyenDuong = RouterSerializer()
    id_PhuongTien = TransportationsSerilializer()
    stoplocal = serializers.SerializerMethodField(read_only=True)


    def get_stoplocal(self,obj):
        stop = DiaDiemDungChan.objects.filter(id_HanhTrinh = obj)
        return StopLocalSerializer(stop,many=True).data #json
    class Meta:
        model = Journey
        fields = ['chiPhi','ngayDi','ngayDen','id_tuyenDuong','id_PhuongTien','stoplocal']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    journey = JourneySerializer(read_only=True)
    tags = TagSerializer(many=True,read_only=True)
    pic = ImageSerializer(many=True,read_only=True)
    class Meta:
        model = Posts
        fields = ["id", "title","content", "created_date","journey","tags","pic","user"]



class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id', 'diaChi']


class TransportationsSerilializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = ['id', 'loai']


class TravelCompanionSerializer(serializers.ModelSerializer):
    user = UserSerializer();

    class Meta:
        model = TravelCompanion
        fields = ["id", ' timeselect', 'active', 'user']


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    pic = ImageSerializer(many=True)

    soLuongnguoiDiCung = serializers.SerializerMethodField()
    travel_companion = serializers.SerializerMethodField()
    sl_rating = serializers.SerializerMethodField()

    class Meta:
        model = PostSerializer.Meta.model
        fields = PostSerializer.Meta.fields + ['content', 'tags', 'pic', 'soLuongnguoiDiCung', 'travel_companion',
                                               "sl_rating", "active"]

    def get_soLuongnguoiDiCung(self, obj):
        active_companions = obj.travelcompanion_set.filter(active=True)
        return active_companions.count()

    def get_travel_companion(self, obj):
        companions = obj.travelcompanion_set.filter(active=True)
        user_ids = [companion.user.id for companion in companions]
        users = User.objects.filter(pk__in=user_ids)
        serialized_users = UserSerializer(users, many=True)  # Use UserSerializer
        return serialized_users.data

    def get_sl_rating(self, obj):
        active_rating = obj.rating_set.filter(active=True)
        return active_rating.count()


class TickSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentTick
        fields = ['id', 'active']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    reply_count = serializers.SerializerMethodField()
    tick = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'created_date', 'user', 'reply_count', 'tick']

    def get_reply_count(self, obj):
        return obj.comment_reply.count()

    def get_tick(self, obj):
        test = obj.ticks
        print(type(obj))
        print(test)
        data = test
        serialized_users = TickSerializer(data)
        print(serialized_users.data)
        return serialized_users.data


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer();

    class Meta:
        model = Rating
        fields = ['id', 'rate', "user"]


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = CommentReply
        fields = ['id', 'content', 'created_date', 'user', 'avatar']

    # def create(self, validated_data):
    #     comment = Comments.objects.get(pk=validated_data.get('cmtRep'))
    #     reply = CommentReply.objects.create(cmtRep=comment, id=comment.id)
    #     reply.save()
    #     return reply


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['id', 'reportContent']
