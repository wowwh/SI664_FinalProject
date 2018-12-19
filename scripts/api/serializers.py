from googleapp.models import AndroidVersion,Category,ContentRating,Genre,PayType,App,AppGenre
from rest_framework import response, serializers, status


class AndroidVersionSerializer(serializers.ModelSerializer):

	class Meta:
		model = AndroidVersion
		fields = ('android_version_id', 'android_version')


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ('category_id', 'category_name')


class ContentRatingSerializer(serializers.ModelSerializer):

	class Meta:
		model = ContentRating
		fields = ('content_rating_id', 'content_rating')


class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name',)




class PayTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = PayType
		fields = ('pay_type_id', 'pay_type_name',)





class AppGenreSerializer(serializers.ModelSerializer):
	app_id = serializers.ReadOnlyField(source='heritage_site.heritage_site_id')
	genre_id = serializers.ReadOnlyField(source='country_area.country_area_id')

	class Meta:
		model = AppGenre
		fields = ('app_id', 'genre_id')


class AppSerializer(serializers.ModelSerializer):
	app_name = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	rating = serializers.CharField(
		allow_blank=True,
		max_length=10
	)
	reviews = serializers.IntegerField(
		allow_null=True
	)
	size = serializers.CharField(
		allow_null=True,
		max_length=20
	)

	install = serializers.CharField(
		allow_null=True,
		max_length=20
	)

	price = serializers.CharField(
		allow_null=True,
		max_length=10
	)

	updated_time = serializers.CharField(
		allow_null=True,
		max_length=20
	)

	current_version = serializers.CharField(
		allow_null=True,
		max_length=50
	)

	
	


	category = CategorySerializer(
		many=False,
		read_only=True
	)
	category_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=Category.objects.all(),
		source='category'
	)


	pay_type = PayTypeSerializer(
		many=False,
		read_only=True
	)
	pay_type_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=PayType.objects.all(),
		source='pay_type'
	)

	content_rating = ContentRatingSerializer(
		many=False,
		read_only=True
	)
	content_rating_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=ContentRating.objects.all(),
		source='content_rating'
	)

	android_version = AndroidVersionSerializer(
		many=False,
		read_only=True
	)
	android_version_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=AndroidVersion.objects.all(),
		source='content_rating'
	)

	




	app_genre = AppGenreSerializer(
		source='app_genre_set', # Note use of _set
		many=True,
		read_only=True
	)
	app_genre_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Genre.objects.all(),
		source='app_genre'
	)

	class Meta:
		model = App
		fields = ('app_id', 'app_name', 'rating', 'reviews', 'size','install','price','updated_time','current_version','category','category_id','pay_type','pay_type_id','content_rating','android_version','content_rating_id','android_version_id','app_genre','app_genre_ids')


	def create(self, validated_data):
		

		# print(validated_data)

		genres = validated_data.pop('app_genre')
		app = App.objects.create(**validated_data)

		if genres is not None:
			for genre in genres:
				AppGenre.objects.create(
					app_id=app.app_id,
					genre_id=genre.genre_id
				)
		return app

	def update(self, instance, validated_data):
		app_id = instance.app_id
		new_genres = validated_data.pop('app_genre')

		instance.app_name = validated_data.get(
			'app_name',
			instance.app_name
		)
		instance.rating = validated_data.get(
			'rating',
			instance.rating
		)
		instance.reviews = validated_data.get(
			'reviews',
			instance.reviews
		)
		instance.size = validated_data.get(
			'size',
			instance.size
		)
		instance.install = validated_data.get(
			'install',
			instance.install
		)
		instance.price = validated_data.get(
			'price',
			instance.price
		)
		instance.updated_time = validated_data.get(
			'updated_time',
			instance.updated_time
		)
		instance.category_id = validated_data.get(
			'category_id',
			instance.category_id
		)
		instance.current_version = validated_data.get(
			'current_version',
			instance.current_version
		)
		instance.pay_type_id = validated_data.get(
			'pay_type_id',
			instance.pay_type_id
		)
		instance.content_rating_id = validated_data.get(
			'content_rating_id',
			instance.content_rating_id
		)
		instance.android_version_id = validated_data.get(
			'android_version_id',
			instance.android_version_id
		)
		instance.save()

		# If any existing country/areas are not in updated list, delete them
		new_ids = []
		old_ids = AppGenre.objects \
			.values_list('genre_id', flat=True) \
			.filter(app_id__exact=app_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched country entries
		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				AppGenre.objects \
					.create(app=app,genre=genre)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				AppGenre.objects \
					.filter(app_id=app.app_id, genre_id=old_id) \
					.delete()

		return instance