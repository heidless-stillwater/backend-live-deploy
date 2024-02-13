from rest_framework import serializers
from .models import Research, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ResearchSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Research
        fields = ('name', 'description', 'link', 'link_blog', 'image', 'tags')