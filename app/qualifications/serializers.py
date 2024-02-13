from rest_framework import serializers
from .models import Qualifications, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class QualificationsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Qualifications
        fields = ('name', 'description', 'link', 'link_blog','image', 'tags')