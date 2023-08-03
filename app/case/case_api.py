from flask import Blueprint, request
from . import case_core as CaseModel
from . import case_core_api as CaseModelApi

from flask_restx import Api, Resource
from ..decorators import api_required, editor_required

api_case_blueprint = Blueprint('api_case', __name__)
api = Api(api_case_blueprint,
        title='Flowintel-cm API', 
        description='API to manage a case management instance.', 
        version='0.1', 
        default='GenericAPI', 
        default_label='Generic Flowintel-cm API', 
        doc='/doc'
    )



@api.route('/all')
@api.doc(description='Get all cases')
class GetCases(Resource):
    method_decorators = [api_required]
    def get(self):
        cases = CaseModel.get_all_cases()
        return {"cases": [case.to_json() for case in cases]}

@api.route('/not_completed')
@api.doc(description='Get all cases')
class GetCases_not_completed(Resource):
    method_decorators = [api_required]
    def get(self):
        cases = CaseModel.get_case_by_completed(False)
        return {"cases": [case.to_json() for case in cases]}
    
@api.route('/completed')
@api.doc(description='Get all cases')
class GetCases_not_completed(Resource):
    method_decorators = [api_required]
    def get(self):
        cases = CaseModel.get_case_by_completed(True)
        return {"cases": [case.to_json() for case in cases]}


@api.route('/<cid>')
@api.doc(description='Get a case', params={'cid': 'id of a case'})
class GetCase(Resource):
    method_decorators = [api_required]
    def get(self, cid):
        case = CaseModel.get_case(cid)
        if case:
            case_json = case.to_json()
            orgs = CaseModel.get_orgs_in_case(cid)
            case_json["orgs"] = list()
            for org in orgs:
                case_json["orgs"].append({"id": org["id"], "uuid": org["uuid"], "name": org["name"]})
            
            return case_json
        return {"message": "Case not found"}
    

@api.route('/<cid>/complete')
@api.doc(description='Complete a case', params={'cid': 'id of a case'})
class CompleteCase(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            case = CaseModel.get_case(cid)
            if case:
                if CaseModel.complete_case(cid, current_user):
                    return {"message": f"Case {cid} completed"}
                return {"message": f"Error case {cid} completed"}
            return {"message": "Case not found"}, 404
        return {"message": "Permission denied"}, 401
    

@api.route('/<cid>/create_template', methods=["POST"])
@api.doc(description='Create a template form case', params={'cid': 'id of a case'})
class CreateTemplate(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"title_template": "Title for the template that will be create"})
    def post(self, cid):
        if "title_template" in request.json:
            if CaseModel.get_case(cid):
                new_template = CaseModel.create_template_from_case(cid, request.json["title_template"])
                if type(new_template) == dict:
                    return new_template
                return {"template_id": new_template.id}, 201
            return {"message": "Case not found"}, 404
        return {"message": "'title_template' is missing"}, 400


@api.route('/<cid>/recurring', methods=['POST'])
@api.doc(description='Set a case recurring')
class RecurringCase(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={
        "once": "Date(%Y-%m-%d)", 
        "daily": "Boolean", 
        "weekly": "Date(%Y-%m-%d). Only the day of the week will be keep.", 
        "monthly": "Date(%Y-%m-%d). Only the day will be keep."
    })
    def post(self, cid):
        if request.json:
            verif_dict = CaseModelApi.verif_set_recurring(request.json)

            if "message" not in verif_dict:
                CaseModel.change_recurring(verif_dict, cid)
                return {"message": "Recurring changed"}
            return verif_dict
        return {"message": "Please give data"}


@api.route('/<cid>/tasks')
@api.doc(description='Get all tasks for a case', params={'cid': 'id of a case'})
class GetTasks(Resource):
    method_decorators = [api_required]
    def get(self, cid):
        case = CaseModel.get_case(cid)
            
        tasks = list()
        for task in case.tasks:
            tasks.append(task.to_json())

        return tasks


@api.route('/<cid>/task/<tid>')
@api.doc(description='Get a specific task for a case', params={"cid": "id of a case", "tid": "id of a task"})
class GetTask(Resource):
    method_decorators = [api_required]
    def get(self, cid, tid):
        task = CaseModel.get_task(tid)
        if task:
            if int(cid) == task.case_id:
                loc = dict()
                loc["users_assign"], loc["is_current_user_assign"] = CaseModel.get_users_assign_task(task.id, CaseModelApi.get_user_api(request.headers["X-API-KEY"]))
                task.notes = CaseModel.markdown_notes(task.notes)
                loc["task"] = task.to_json()
                return loc
            else:
                return {"message": "Task not in this case"}
        return {"message": "Task not found"}


@api.route('/<cid>/delete')
@api.doc(description='Delete a case', params={'cid': 'id of a case'})
class DeleteCase(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            if CaseModel.delete_case(cid, current_user):
                return {"message": "Case deleted"}, 200
            else:
                return {"message": "Error case deleted"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/task/<tid>/delete')
@api.doc(description='Delete a specific task in a case', params={'cid': 'id of a case', "tid": "id of a task"})
class DeleteTask(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    if CaseModel.delete_task(tid):
                        return {"message": "Task deleted"}, 201
                    else:
                        return {"message": "Error task deleted"}, 201
                else:
                    return {"message": "Task not in this case"}
            return {"message": "Task not found"}
        return {"message": "Permission denied"}, 403
        

@api.route('/add', methods=['POST'])
@api.doc(description='Add a case')
class AddCase(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={
        "title": "Required. Title for a case", 
        "description": "Description of a case", 
        "deadline_date": "Date(%Y-%m-%d)", 
        "deadline_time": "Time(%H-%M)"
    })
    def post(self):
        user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])

        if request.json:
            verif_dict = CaseModelApi.verif_add_case_task(request.json, True)

            if "message" not in verif_dict:
                case = CaseModel.add_case_core(verif_dict, user)
                return {"message": f"Case created, id: {case.id}"}

            return verif_dict
        return {"message": "Please give data"}


@api.route('/<cid>/add_task', methods=['POST'])
@api.doc(description='Add a task to a case', params={'cid': 'id of a case'})
class AddTask(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={
        "title": "Required. Title for a task", 
        "description": "Description of a task",
        "url": "Link to a tool or a ressource",
        "deadline_date": "Date(%Y-%m-%d)", 
        "deadline_time": "Time(%H-%M)"
    })
    def post(self, cid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            if request.json:
                verif_dict = CaseModelApi.verif_add_case_task(request.json, False)

                if "message" not in verif_dict:
                    task = CaseModel.add_task_core(verif_dict, cid)
                    return {"message": f"Task created for case id: {cid}"}

                return verif_dict
            return {"message": "Please give data"}
        return {"message": "Permission denied"}, 403


@api.route('/<id>/edit', methods=['POST'])
@api.doc(description='Edit a case', params={'id': 'id of a case'})
class EditCase(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"title": "Title for a case", "description": "Description of a case", "deadline_date": "Date(%Y-%m-%d)", "deadline_time": "Time(%H-%M)"})
    def post(self, id):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(id, current_user) or current_user.is_admin():
            if request.json:
                verif_dict = CaseModelApi.verif_edit_case(request.json, id, True)

                if "message" not in verif_dict:
                    CaseModel.edit_case_core(verif_dict, id)
                    return {"message": f"Case {id} edited"}

                return verif_dict
            return {"message": "Please give data"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/task/<tid>/edit', methods=['POST'])
@api.doc(description='Edit a task in a case', params={'cid': 'id of a case', "tid": "id of a task"})
class EditTake(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"title": "Title for a case", "description": "Description of a case", "deadline_date": "Date(%Y-%m-%d)", "deadline_time": "Time(%H-%M)"})
    def post(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user):
            if request.json:
                task = CaseModel.get_task(tid)
                if task:
                    if int(cid) == task.case_id:
                        verif_dict = CaseModelApi.verif_edit_task(request.json, tid, False)

                        if "message" not in verif_dict:
                            CaseModel.edit_task_core(verif_dict, tid)
                            return {"message": f"Task {tid} edited"}

                        return verif_dict
                    else:
                        return {"message": "Task not in this case"}
                else:
                    return {"message": "Task not found"}
            return {"message": "Please give data"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/task/<tid>/complete')
@api.doc(description='Complete a task in a case', params={'cid': 'id of a case', "tid": "id of a task"})
class CompleteTake(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    if CaseModel.complete_task(tid):
                        return {"message": f"Task {tid} completed"}
                    return {"message": f"Error task {tid} completed"}
                else:
                    return {"message": "Task not in this case"}
            return {"message": "Task not found"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/task/<tid>/get_note')
@api.doc(description='Get note of a task in a case', params={'cid': 'id of a case', "tid": "id of a task"})
class GetNoteTask(Resource):
    method_decorators = [api_required]
    def get(self, cid, tid):
        task = CaseModel.get_task(tid)
        if task:
            if int(cid) == task.case_id:
                note = CaseModel.get_note_text(tid)
                return {"note": note}
            else:
                return {"message": "Task not in this case"}
        return {"message": "Task not found"}


@api.route('/<cid>/task/<tid>/modif_note', methods=['POST'])
@api.doc(description='Edit note of a task in a case', params={'cid': 'id of a case', "tid": "id of a task"})
class ModifNoteTask(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"note": "note to create or modify"})
    def post(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            if "note" in request.json:
                task = CaseModel.get_task(tid)
                if task:
                    if int(cid) == task.case_id:
                        if CaseModel.modif_note_core(tid, request.json["note"]):
                            return {"message": f"Note for Task {tid} edited"}
                        return {"message": f"Error Note for Task {tid} edited"}
                    else:
                        return {"message": "Task not in this case"}
                return {"message": "Task not found"}
            return {"message": "Key 'note' not found"}
        return {"message": "Permission denied"}, 403



@api.route('/<cid>/add_org', methods=['POST'])
@api.doc(description='Add an org to the case', params={'cid': 'id of a case'})
class AddOrgCase(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"name": "Name of the organisation", "oid": "id of the organisation"})
    def post(self, cid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            if "name" in request.json:
                org = CaseModel.get_org_by_name(request.json["name"])
            elif "id" in request.json:
                org = CaseModel.get_org(request.json["oid"])
            else:
                return {"message": "Required an id or a name of an Org"}

            if org:
                if not CaseModel.get_org_in_case(org.id, cid):
                    if CaseModel.add_orgs_case({"org_id": [org.id]}, cid):
                        return {"message": f"Org added for Case {cid} edited"}
                    return {"message": f"Error Org added for Case {cid} edited"}
                else:
                    return {"message": "Org already in case"}
            return {"message": "Org not found"}

        return {"message": "Permission denied"}, 403


@api.route('/<cid>/remove_org/<oid>', methods=['GET'])
@api.doc(description='Add an org to the case', params={'cid': 'id of a case', "oid": "id of an org"})
class RemoveOrgCase(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid, oid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            org = CaseModel.get_org(oid)

            if org:
                if CaseModel.get_org_in_case(org.id, cid):
                    if CaseModel.remove_org_case(cid, org.id):
                        return {"message": f"Org deleted for Case {cid} edited"}
                    return {"message": f"Error Org deleted for Case {cid} edited"}
                else:
                    return {"message": "Org not in case"}
            return {"message": "Org not found"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/take_task/<tid>', methods=['GET'])
@api.doc(description='Assign user to the task', params={'cid': 'id of a case', "tid": "id of a task"})
class AssignTask(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)

            if task:
                if int(cid) == task.case_id:
                    user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
                    if CaseModel.assign_task(tid, user):
                        return {"message": f"Task Take"}
                    else:
                        return {"message": f"Error Task Take"}
                else:
                    return {"message": "Task not in this case"}
            return {"message": "Task not found"}
        return {"message": "Permission denied"}, 403


@api.route('/<cid>/remove_assign_task/<tid>', methods=['GET'])
@api.doc(description='Assign user to the task', params={'cid': 'id of a case', "tid": "id of a task"})
class RemoveOrgCase(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
                    if CaseModel.remove_assign_task(tid, user):
                        return {"message": f"User Removed from assignment"}
                    return {"message": f"Error User Removed from assignment"}
                else:
                    return {"message": "Task not in this case"}
            return {"message": "Task not found"}
        return {"message": "Permission denied"}, 401
    

@api.route('/<cid>/get_all_users', methods=['GET'])
@api.doc(description='Get list of user that can be assign', params={'cid': 'id of a case'})
class GetAllUsers(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, cid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            case = CaseModel.get_case(cid)
            if case:
                users_list = list()
                for org in CaseModel.get_all_users_core(case):
                    for user in org.users:
                        if not user == current_user:
                            users_list.append(user.to_json())
                return {"users": users_list}
            return {"message": "Case not found"}, 404
        return {"message": "Permission denied"}, 401
    


@api.route('/<cid>/task/<tid>/assign_users', methods=['POST'])
@api.doc(description='Assign users to a task', params={'cid': 'id of a case', "tid": "id of a task"})
class AssignUser(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"users_id": "List of user id"})
    def post(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    users_list = request.json["users_id"]
                    for user in users_list:
                        CaseModel.assign_task(tid, user, flag_current_user=False)
                    return {"message": "Users Assigned"}, 200
                return {"message": "Task not in this case"}, 404
            return {"message": "Task not found"}, 404
        return {"message": "Permission denied"}, 401


@api.route('/<cid>/task/<tid>/remove_assign_user', methods=['POST'])
@api.doc(description='Remove an assign user to a task', params={'cid': 'id of a case', "tid": "id of a task"})
class AssignUser(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"user_id": "Id of a user"})
    def post(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    user_id = request.json["user_id"]
                    if CaseModel.remove_assign_task(tid, user_id, flag_current_user=False):
                        return {"message": "User Removed from assignment"}, 200
                return {"message": "Task not in this case"}, 404
            return {"message": "Task not found"}, 404
        return {"message": "Permission denied"}, 401
    


@api.route('/<cid>/task/<tid>/change_status', methods=['POST'])
@api.doc(description='Change status of a task', params={'cid': 'id of a case', "tid": "id of a task"})
class ChangeStatus(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"status_id": "Id of the new status"})
    def post(self, cid, tid):
        current_user = CaseModelApi.get_user_api(request.headers["X-API-KEY"])
        if CaseModel.get_present_in_case(cid, current_user) or current_user.is_admin():
            task = CaseModel.get_task(tid)
            if task:
                if int(cid) == task.case_id:
                    if CaseModel.change_status_task(request.json["status_id"], task):
                        return {"message": "Status changed"}, 200
                return {"message": "Task not in this case"}, 404
            return {"message": "Task not found"}, 404
        return {"message": "Permission denied"}, 401


@api.route('/list_status', methods=['GET'])
@api.doc(description='List all status')
class ChangeStatus(Resource):
    method_decorators = [api_required]
    def get(self):
        return [status.to_json() for status in CaseModel.get_all_status()]