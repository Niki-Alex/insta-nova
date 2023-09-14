from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserFollowing


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "biography",
            "phone_number",
            "avatar",
            "password",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(UserSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    @staticmethod
    def get_followers(obj):
        return UserFollowersSerializer(obj.followers.all(), many=True).data

    @staticmethod
    def get_following(obj):
        return UserFollowingSerializer(obj.following.all(), many=True).data

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_of_birth",
            "biography",
            "phone_number",
            "avatar",
            "followers",
            "following",
        )


class UserFollowingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="following_user_id.id")
    first_name = serializers.ReadOnlyField(source="following_user_id.first_name")
    last_name = serializers.ReadOnlyField(source="following_user_id.last_name")

    class Meta:
        model = UserFollowing
        fields = ("id", "first_name", "last_name")


class UserFollowersSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user_id.first_name")
    last_name = serializers.ReadOnlyField(source="user_id.last_name")

    class Meta:
        model = UserFollowing
        fields = ("user_id", "first_name", "last_name")
