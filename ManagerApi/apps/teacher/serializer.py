from rest_framework import serializers
from users.models import User

class GetAllStudentsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    house_number = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'gender', 'is_active','user_type','house_number']
    def get_name(self, obj):
        return obj.last_name + obj.first_name
    def get_house_number(self, obj):
        if obj.house_number:
            house_number = obj.house_number.floor.floor_name + '-' + obj.house_number.hostel_number
            return house_number
        return "无"
