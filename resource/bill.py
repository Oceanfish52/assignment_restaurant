from flask import jsonify, request
from flask_restful import Resource
from model.bill import BillModel, BillMenu
from schema.bill import BillSchema, BillCheckSchema, MenuOrder, BillDeleteSchema, BillMenuSchema


class BillResource(Resource):
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
            bill_load = BillSchema().load(data_json)
            if bill_load.errors:
                return jsonify(result={},
                               status=500,
                               error=bill_load.errors)
            else:
                bill_item = bill_load.data
                bill = BillModel(
                    bill_id=bill_item['bill_id'],
                    total_price=bill_item['total_price'])

                if bill_item['menu']:
                    try:
                        bill.save_to_db()
                        order = MenuOrder(many=True).load(bill_item['menu'])
                        # todo error
                        for menuorder in order.data:
                            order_item = BillMenu(
                                bill_id=bill_item['bill_id'],
                                name=menuorder['name'],
                                order_time=menuorder['order_time'],
                                quantities=menuorder['quantities']
                            )
                            try:
                                order_item.save_to_db()
                            except Exception as err:
                                order_item.rollback_from_db()
                                return jsonify(result={},
                                               status=505,
                                               error={'message': 'Internal error {}'.format(err.args)})
                    except Exception as err:
                        bill.rollback_from_db()
                        return jsonify(result={},
                                       status=505,
                                       error={'message': 'Internal error {}'.format(err.args)})

            return jsonify(result=BillSchema().dump(bill_item).data,
                           status=200,
                           error={})


class BillOrderManagement(Resource):
    def put(self):
        data_json = request.get_json()  # incoming json request
        bill = BillSchema().load(data_json)
        if bill.errors:
            return jsonify(result={},
                           status=500,
                           error=bill.errors)
        else:
            bill = bill.data
            exists_bill = BillModel.search_bill(bill_id=bill['bill_id'])
            if exists_bill:
                more_order = bill['menu']
                order = MenuOrder(many=True).load(more_order)
                for menuorder in order.data:
                    order_item = BillMenu(
                        bill_id=bill['bill_id'],
                        name=menuorder['name'],
                        order_time=menuorder['order_time'],
                        quantities=menuorder['quantities']
                    )
                    try:
                        order_item.save_to_db()
                    except Exception as err:
                        order_item.rollback_from_db()
                        return jsonify(result={},
                                       status=505,
                                       error={'message': 'Internal error {}'.format(err.args)})
                exists_bill = BillModel.search_bill_order(bill_id=bill['bill_id'])

                menu = []
                bill_id = {'bill_id': bill['bill_id']}
                for i in exists_bill:
                    menu.append(i[1])
                menu_dict = {'menu': menu}
                return jsonify(result=BillSchema().dump({**bill_id, **menu_dict}).data,
                               status=200,
                               error={})
            else:
                return jsonify(result={},
                               status=505,
                               error={'message': 'Not found #Bill {}'.format(bill['bill_id'])})

    def post(self):
        success, error = [], []
        data_json = request.get_json()  # incoming json request
        bill = BillDeleteSchema(many=True).load(data_json)
        if bill.errors:
            return jsonify(result={},
                           status=500,
                           error=bill.errors)
        else:
            bill = bill.data
            for item in bill:
                bill_order = BillMenu.search_billoreder(billid=item['bill_id'], ordertime=item['order_time'])
                if bill_order:
                    try:
                        bill_order.delete_from_db()
                        success.append({'message': 'delete {}'.format(bill['bill_id'])})
                    except:
                        bill_order.rollback_from_db()
                        error.append({'message': 'error on deleting #Bill {} in order time {}'
                                     .format(item['bill_id'], item['order_time'])})
                else:
                    error.append({'message': 'Not found #Bill {}'.format(item['bill_id'])})

            if success and not error:
                return jsonify(status="Delete Successfully",
                               result=success,
                               error=error)

            elif success and error:
                return jsonify(status="Delete Partially, There're some error",
                               result=success,
                               error=error)
            else:
                return jsonify(status="Delete Failed and There're error",
                               result={},
                               error=error)


class BillUpdateQuantity(Resource):
    def put(self):
        data_json = request.get_json()  # incoming json request
        bill = BillMenuSchema().load(data_json)
        if bill.errors:
            return jsonify(result={},
                           status=500,
                           error=bill.errors)
        else:
            bill = bill.data
            bill_name = BillMenu.search_billname(billid=bill['bill_id'],
                                                 name=bill['name'],
                                                 ordertime=bill['order_time'])
            if bill_name:
                bill_update = BillMenu(
                    quantities=bill['quantities']
                )
                try:
                    bill_update.update_to_db()
                    return jsonify(result={'message': 'update successful'},
                                   status=200,
                                   error={})
                except Exception as err:
                    bill_name.rollback_from_db()
                    return jsonify(result={},
                                   status=505,
                                   error={'message': 'Internal error {}'.format(err.args)})
            else:
                return jsonify(result={},
                               error={'message': 'Not found #Bill {}'.format(bill['bill_id'])},
                               status=404)


class BillChecking(Resource):
    def post(self):
        data_json = request.get_json()  # incoming json request
        if not data_json:
            return jsonify(result={},
                           status=400.,
                           error={'message': 'No input data provide'})
        else:
            bill_load = BillCheckSchema().load(data_json)
            if bill_load.errors:
                return jsonify(result={},
                               status=500,
                               error=bill_load.errors)
            else:
                bill_item = bill_load.data
                exists_bill = BillModel.search_bill_order(bill_id=bill_item['bill_id'])

                menu = []
                bill_id = {'bill_id': bill_item['bill_id']}
                for i in exists_bill:
                    menu.append(i[1])
                menu_dict = {'menu': menu}
                return jsonify(result=BillSchema().dump({**bill_id, **menu_dict}).data,
                               status=200,
                               error={})


class BillSummary(Resource):
    def get(self, bill_id):
        bill_id = str(bill_id)
        exists_bill = BillModel.search_bill_order(bill_id=bill_id)
        if exists_bill:
            print(exists_bill)
            menu = []
            for i in exists_bill:
                menu.append(i[1])
            sum_price = 0
            menu_count = {}
            for item in menu:
                if item.name in menu_count:
                    menu_count[item.name] += 1
                else:
                    menu_count[item.name] = 1
            for key, value in menu_count.items():
                price = BillMenu.search_price(key)
                sum_price += (price[1] * value)

            return jsonify(result={'bill_id': bill_id,
                                   'menu': menu_count,
                                   'total_price': sum_price},
                           status=200,
                           error={})
        else:
            return jsonify(result={},
                           status=404,
                           error={})
