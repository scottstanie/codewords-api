# A serializer mixin that takes an additional `fields` argument that controls
# which fields should be displayed.

# How to add to your serializers example:
# class MySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = MyModel

class DynamicFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if not self.context:
            return

        fields = self.context['request'].query_params.get('fields', None)

        # Drop any fields that are not specified in the `fields` argument.
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
