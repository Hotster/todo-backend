from rest_framework import serializers

from goals.models import Goal, Folder


class ChildGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ['id', 'name']


class ChildFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ['id', 'name']


class FolderSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    child_goals = ChildGoalSerializer(many=True, required=False)
    parent_goals = ChildGoalSerializer(many=True, required=False, read_only=True)
    child_folders = ChildFolderSerializer(many=True, required=False)
    parent_folders = ChildFolderSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'

    def validate_child_goals(self, attrs):
        child_goals = [item['id'] for item in attrs]
        for goal in child_goals:
            if Goal.objects.get(pk=goal).owner != self.context['request'].user:
                raise serializers.ValidationError('Child goal owner should be the same as goal owner')
        return attrs

    def validate_parent_goals(self, attrs):
        parent_goals = [item['id'] for item in attrs]
        for goal in parent_goals:
            if Goal.objects.get(pk=goal).owner != self.context['request'].user:
                raise serializers.ValidationError('Parent goal owner should be the same as goal owner')
        return attrs

    def validate_child_folders(self, attrs):
        child_folders = [item['id'] for item in attrs]
        for folder in child_folders:
            if Folder.objects.get(pk=folder).owner != self.context['request'].user:
                raise serializers.ValidationError('Child folder owner should be the same as goal owner')
        return attrs

    def validate_parent_folders(self, attrs):
        parent_folders = [item['id'] for item in attrs]
        for folder in parent_folders:
            if Folder.objects.get(pk=folder).owner != self.context['request'].user:
                raise serializers.ValidationError('Folder owner should be the same as goal owner')
        return attrs

    def create(self, validated_data):
        child_goals = validated_data.pop('child_goals', [])
        child_goals_ids = [item['id'] for item in child_goals]
        child_folders = validated_data.pop('child_folders', [])
        child_folders_ids = [item['id'] for item in child_folders]

        goal = super(FolderSerializer, self).create(validated_data)
        goal.child_goals.set(child_goals_ids)
        goal.child_folders.set(child_folders_ids)

        return goal


class GoalSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    creation_date = serializers.DateTimeField(read_only=True)
    child_goals = ChildGoalSerializer(many=True, required=False)
    parent_goals = ChildGoalSerializer(many=True, required=False, read_only=True)
    child_folders = ChildFolderSerializer(many=True, required=False)
    parent_folders = ChildFolderSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'

    def validate_child_goals(self, attrs):
        child_goals = [item['id'] for item in attrs]
        for goal in child_goals:
            if Goal.objects.get(pk=goal).owner != self.context['request'].user:
                raise serializers.ValidationError('Child goal owner should be the same as goal owner')
        return attrs

    def validate_parent_goals(self, attrs):
        parent_goals = [item['id'] for item in attrs]
        for goal in parent_goals:
            if Goal.objects.get(pk=goal).owner != self.context['request'].user:
                raise serializers.ValidationError('Parent goal owner should be the same as goal owner')
        return attrs

    def validate_child_folders(self, attrs):
        child_folders = [item['id'] for item in attrs]
        for folder in child_folders:
            if Folder.objects.get(pk=folder).owner != self.context['request'].user:
                raise serializers.ValidationError('Child folder owner should be the same as goal owner')
        return attrs

    def validate_parent_folders(self, attrs):
        parent_folders = [item['id'] for item in attrs]
        for folder in parent_folders:
            if Folder.objects.get(pk=folder).owner != self.context['request'].user:
                raise serializers.ValidationError('Folder owner should be the same as goal owner')
        return attrs

    def create(self, validated_data):
        child_goals = validated_data.pop('child_goals', [])
        child_goals_ids = [item['id'] for item in child_goals]
        child_folders = validated_data.pop('child_folders', [])
        child_folders_ids = [item['id'] for item in child_folders]

        goal = super(GoalSerializer, self).create(validated_data)
        goal.child_goals.set(child_goals_ids)
        goal.child_folders.set(child_folders_ids)

        return goal
