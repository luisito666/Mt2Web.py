from rest_framework import serializers
from apps.account.models import Account


class AccountSerializer(serializers.Serializer):
	login = serializers.CharField(read_only=True)
	real_name = serializers.CharField()
	email = serializers.CharField()
	coins = serializers.IntegerField()
	a_points = serializers.IntegerField(default=0)
	votecoins = serializers.IntegerField(default=0)

	def create(self):
		pass

	def update(self):
		pass

class RegisterSerializers(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('login', 'password', 'real_name', 'email', 'social_id')

	def create(self, validated_data):
		passwd = Account.micryp(validated_data['password'],validated_data['password'])
		cuenta = Account(
				login = validated_data['login'],
				password = passwd,
				real_name = validated_data['real_name'],
				email = validated_data['email'],
				social_id = validated_data['social_id']
			)
		cuenta.save()
		return {
			'login': validated_data['login'],
			'password': 'privado',
			'real_name': validated_data['real_name'],
			'email': validated_data['email'],
			'social_id': validated_data['social_id']
		}




class SerializersTop(serializers.Serializer):
	account_id = serializers.IntegerField()
	name = serializers.CharField()
	guild_name = serializers.CharField()
	level = serializers.IntegerField()
	exp = serializers.IntegerField()
	ranking = serializers.IntegerField()

	def create(self):
		pass

	def update(self):
		pass

class SerializersGuild(serializers.Serializer):
    name = serializers.CharField()
    level = serializers.IntegerField()
    exp = serializers.IntegerField()
    ladder_point = serializers.IntegerField()

    def create(self):
    	pass

    def update(self):
    	pass

class SerializersDescargas(serializers.Serializer):
	provedor = serializers.CharField()
	peso = serializers.DecimalField(max_digits=5, decimal_places=3)
	fecha = serializers.DateTimeField()
	link = serializers.CharField()

	def create(self):
		pass

	def update(self):
		pass

class SerializersGremios(serializers.Serializer):
	name = serializers.CharField()
	level = serializers.IntegerField()
	exp = serializers.IntegerField()
	ladder_point = serializers.IntegerField()
