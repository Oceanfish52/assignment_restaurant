from flask import jsonify, request
from flask_restful import Resource

from model.menu import MenuModel
from schema.menu import MenuSchema


class MenuResource(Resource):
    def get(self):
        error_msg = {'message': "The /URL is not available"}
        return jsonify(result=error_msg,
                       status=404,
                       error={})

    def post(self):
        data_json = request.get_json()  # incoming json request 
        if not data_json:
            return jsonify(result={},
                           status=400.,
                           error={'message': 'No input data provide'})
        else:
            menu = MenuSchema(many=True).load(data_json)
            if menu.errors:
                return jsonify(result={},
                               status=500,
                               error=menu.errors)
            else:
                for item in menu.data:
                    item = MenuModel(
                        name=item['name'],
                        description=item['description'],
                        image=item['image'],
                        price=item['price'],
                        detail=item['detail']
                    )
                    try:
                        item.save_to_db()
                    except Exception as err:
                        return jsonify(result={},
                                       status=505.,
                                       error={'message': 'Internal error {}'.format(err.args)})

                return jsonify(result=menu.data,
                               status=200,
                               error={})


class MenuItem(Resource):
    def post(self):
        data_json = request.get_json()  # incoming json request
        menu = MenuSchema(many=True).load(data_json)
        if menu.errors:
            return jsonify(result={},
                           status=500,
                           error=menu.errors)
        else:
            menu = menu.data
            for item in menu:
                menu_item = MenuModel.search_menu(name=item['name'])
                if menu_item:
                    return jsonify(result=MenuSchema(many=True).dump(menu_item).data,
                                   status=200,
                                   error={})
                else:
                    error_msg = {'message': 'not found menu name'.format(menu)}
                    return jsonify(result={},
                                   status=404,
                                   error=error_msg)


class MenuListing(Resource):
    def get(self):
        items = MenuModel.search_all()
        return jsonify(result=MenuSchema(many=True).dump(items).data,
                       status=200,
                       error={})


class MenuKeywordMatching(Resource):
    @staticmethod
    def merge_text(txtdict):
        text = ''
        for k, v in txtdict.items():
            text = text + ' ' + str(v)
        return text

    def get(self, keyword):
        keyword = str(keyword)
        menu_all = MenuSchema(many=True).dump(MenuModel.search_all()).data
        menu_keyword = {}
        match, result = [], []
        for item in menu_all:
            menu_keyword[item['name']] = MenuKeywordMatching.merge_text(item)

        for k, v in menu_keyword.items():
            if keyword in v:
                match.append(k)

        for item in match:
            menu_item = MenuModel.search_menu(name=item)
            result.append(menu_item[0])

        if result:
            return jsonify(result=MenuSchema(many=True).dump(result).data,
                           status=200,
                           error={})
        else:
            error_msg = {'message': 'not found menu by keyword'.format(keyword)}
            return jsonify(result={},
                           status=404,
                           error=error_msg)
