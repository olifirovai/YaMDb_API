from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from content.models import Category, Title, Genre, Comment, Review
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        default=email)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField()


class UserRoleSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        title = (self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Вы уже поставили оценку')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
