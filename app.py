import datetime
from flask import Flask, request, jsonify
from db_dummy import vacancies_database, events_database, current_user_id


app = Flask(__name__)


@app.route('/vacancy/', methods=['GET', 'POST'])
def vacancy_resource():

    if request.method == 'POST':
        vacancy_kwargs = request.args
        return jsonify(vacancies_database.add_entry(**vacancy_kwargs))

    else:
        return jsonify(vacancies_database.filter_by_key_and_value('user_id', current_user_id))


@app.route('/vacancy/<int:vacancy_id>/', methods=['GET', 'PUT', 'DELETE'])
def vacancy_vacancy_id(vacancy_id):
    vacancy_to_work_with = vacancies_database.get_entry_by_id(vacancy_id)

    if not vacancy_to_work_with:
        return f'requested vacancy_id:{vacancy_id} not found'
    if vacancy_to_work_with.get('user_id', None) != current_user_id:
        return f'vacancy_id:{vacancy_id} was not found in current user, user_id:{current_user_id}'

    if request.method == 'PUT':
        vacancy_args = request.args
        return jsonify(vacancies_database.update_entry(vacancy_id, **vacancy_args))

    elif request.method == 'DELETE':
        return vacancies_database._delete_entry(vacancy_id)

    else:
        return jsonify(vacancy_to_work_with)


@app.route('/vacancy/<int:vacancy_id>/events/', methods=['GET', 'POST'])
def events_resource(vacancy_id):

    if request.method == 'POST':
        events_args = request.args
        return jsonify(events_database.add_entry(vacancy_id=vacancy_id, **events_args))

    else:
        return jsonify(events_database.filter_by_key_and_value('vacancy_id', vacancy_id))


@app.route('/vacancy/<int:vacancy_id>/events/<int:event_id>/', methods=['GET', 'PUT', 'DELETE'])
def events_id(vacancy_id, event_id):
    event_to_work_with = events_database.get_entry_by_id(event_id)

    if not event_to_work_with:
        return f'requested event_id:{event_id} not found'
    if event_to_work_with.get('vacancy_id', None) != vacancy_id:
        return f'event_id:{event_id} was not found in vacancy_id:{vacancy_id}'
    if vacancies_database.get_entry_by_id(vacancy_id).get('user_id', None) != current_user_id:
        return f'event_id:{event_id} was not found in current user, user_id:{current_user_id}'

    if request.method == 'PUT':
        event_kwargs = request.args
        return jsonify(events_database.update_entry(event_id, **event_kwargs))

    elif request.method == 'DELETE':
        return events_database._delete_entry(event_id)

    else:
        return jsonify(event_to_work_with)


@app.route('/vacancy/history/', methods=['GET'])
def vacancy_history():
    return 'show history of all vacancies'


@app.route('/', methods=['GET'])
@app.route('/user/', methods=['GET'])
def user_main_page():
    return 'show user\'s main page'


@app.route('/user/calendar/', methods=['GET'])
def user_calendar():
    return 'show user\'s calendar'


@app.route('/user/mail/', methods=['GET'])
def user_mail(*args, **kwargs):
    return f'show user\'s e-mail {args} {kwargs}. Some '


@app.route('/user/settings/', methods=['GET', 'PUT'])
def user_settings():
    if request.method == 'PUT':
        return 'change user\'s settings'
    else:
        return 'show user\'s settings'


@app.route('/user/documents/', methods=['GET', 'POST'])
def user_documents():
    if request.method == 'POST':
        return 'create/upload new document'
    else:
        return 'show user\'s documents'


@app.route('/user/documents/<int:document_id>', methods=['GET', 'DELETE'])
def user_documents_document_id(document_id):
    if request.method == 'DELETE':
        return f'delete document with id: {document_id}'
    else:
        return f'show content of document with id: {document_id}'


@app.route('/user/templates/', methods=['GET', 'POST'])
def user_templates():
    if request.method == 'POST':
        return 'create new template'
    else:
        return 'show user\'s templates list'


@app.route('/user/templates/<int:template_id>', methods=['GET', 'PUT', 'DELETE'])
def user_templates_template_id(template_id):
    if request.method == 'PUT':
        return f'change template with id: {template_id}'
    elif request.method == 'DELETE':
        return f'delete template with id: {template_id}'
    else:
        return f'show content of template with id: {template_id}'


if __name__ == '__main__':
    app.run()