from rest_framework.renderers import JSONRenderer


class CustomJsonRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if renderer_context:
            response = renderer_context['response']
            code = response.status_code
            if isinstance(data, dict):
                code = data.pop('code', code)
                data = data.pop('data', data)
            if code != 200 and data:
                code = data.pop('code', code)
                data = data.pop('data', data)
                res = {
                    'status': code,
                    'data': data,
                }
                return super().render(res, accepted_media_type, renderer_context)

            response.status_code = 200
            res = {
                'status': code,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)