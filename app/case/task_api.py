from flask import Blueprint, request
from . import case_core as CaseModel
from . import common_core as CommonModel
from . import task_core as TaskModel
from . import case_core_api as CaseModelApi

from flask_restx import Api, Resource
from ..decorators import api_required, editor_required

api_task_blueprint = Blueprint('api_task', __name__)
api = Api(api_task_blueprint,
        title='flowintel API', 
        description='API to manage a case management instance.', 
        version='0.1', 
        default='GenericAPI', 
        default_label='Generic flowintel API', 
        doc='/doc/'
    )




@api.route('/<tid>')
@api.doc(description='Get a task by id', params={"tid": "id of a task"})
class GetTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            loc = dict()
            loc["users_assign"], loc["is_current_user_assign"] = TaskModel.get_users_assign_task(task.id, CaseModelApi.get_user_api(request.headers))
            loc["task"] = task.to_json()
            return loc, 200
        return {"message": "Task not found"}, 404
    

@api.route('/title', methods=["POST"])
@api.doc(description='Get a task by title')
class GetTaskTitle(Resource):
    method_decorators = [api_required]
    @api.doc(params={"title": "Title of a task"})
    def post(self):
        if "title" in request.json:
            task = CommonModel.get_task_by_title(request.json["title"])
            if task:
                return task.to_json(), 200
            return {"message": "Task not found"}, 404
        return {"message": "Need to pass a title"}, 404
    
    
@api.route('/<tid>/edit', methods=['POST'])
@api.doc(description='Edit a task', params={"tid": "id of a task"})
class EditTake(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"title": "Title for a task", "description": "Description of a task", "deadline_date": "Date(%Y-%m-%d)", "deadline_time": "Time(%H-%M)"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if request.json:
                    verif_dict = CaseModelApi.verif_edit_task(request.json, tid)

                    if "message" not in verif_dict:
                        TaskModel.edit_task_core(verif_dict, tid, current_user)
                        return {"message": f"Task {tid} edited"}, 200

                    return verif_dict, 400
                return {"message": "Please give data"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404

@api.route('/<tid>/delete')
@api.doc(description='Delete a task', params={"tid": "id of a task"})
class DeleteTask(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.delete_task(tid, current_user):
                    return {"message": "Task deleted"}, 200
                return {"message": "Error task deleted"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404


@api.route('/<tid>/complete')
@api.doc(description='Complete a task', params={"tid": "id of a task"})
class CompleteTask(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.complete_task(tid, current_user):
                    return {"message": f"Task {tid} completed"}, 200
                return {"message": f"Error task {tid} completed"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404

    
@api.route('/<tid>/get_all_notes')
@api.doc(description='Get all notes of a task', params={"tid": "id of a task"})
class GetAllNotesTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            return {"notes": [note.to_json() for note in task.notes]}, 200
        return {"message": "Task not found"}, 404
    
@api.route('/<tid>/get_note')
@api.doc(description='Get note of a task', params={"note_id": "id of a note in task"})
class GetNoteTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            if "note_id" in request.args:
                task_note = CommonModel.get_task_note(request.args.get("note_id"))
                if task_note:
                    return {"note": task_note.note}, 200
                return {"message": "Note not found"}, 404
            return {"message": "Need to pass a note id"}, 400
        return {"message": "Task not found"}, 404


@api.route('/<tid>/modif_note', methods=['POST'])
@api.doc(description='Edit note of a task in a case', params={"tid": "id of a task"})
class ModifNoteTask(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"note": "note to create or modify", "note_id": "id of the note"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if "note_id" in request.json:
                    if "note" in request.json:
                        res = TaskModel.modif_note_core(tid, current_user, request.json["note"], request.json["note_id"])
                        if type(res) == dict:
                            return res, 400
                        return {"message": f"Note for task {tid} edited"}, 200
                    return {"message": "Need to pass a note"}, 400
                return {"message": "Need to pass a note id"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404
    
@api.route('/<tid>/create_note', methods=['POST'])
@api.doc(description='Create a new note for a task', params={"tid": "id of a task"})
class CreateNoteTask(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"note": "note to create"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if "note" in request.json:
                    res = TaskModel.modif_note_core(tid, current_user, request.json["note"], '-1')
                    if type(res) == dict:
                        return res, 400
                    return {"message": f"Note for task {tid} edited"}, 200
                return {"message": "Need to pass a note"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404
    

@api.route('/<tid>/delete_note')
@api.doc(description='Delete a note of a task', params={"note_id": "id of a note in task"})
class GetNoteTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            if "note_id" in request.args:
                if TaskModel.delete_note(tid, request.args.get("note_id")):
                    return {"message": "Note deleted"}, 200
            return {"message": "Need to pass a note id"}, 400
        return {"message": "Task not found"}, 404


@api.route('/<tid>/take_task', methods=['GET'])
@api.doc(description='Assign current user to the task', params={"tid": "id of a task"})
class AssignTask(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            print(current_user.to_json())
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.assign_task(tid, user=current_user, current_user=current_user, flag_current_user=True):
                    return {"message": f"Task Take"}, 200
                return {"message": f"Error Task Take"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404


@api.route('/<tid>/remove_assignment', methods=['GET'])
@api.doc(description='Remove assigment of current user to the task', params={"tid": "id of a task"})
class RemoveOrgCase(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.remove_assign_task(tid, user=current_user, current_user=current_user, flag_current_user=True):
                    return {"message": f"Removed from assignment"}, 200
                return {"message": f"Error Removed from assignment"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404


@api.route('/<tid>/assign_users', methods=['POST'])
@api.doc(description='Assign users to a task', params={"tid": "id of a task"})
class AssignUsers(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"users_id": "List of user id"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                users_list = request.json["users_id"]
                for user in users_list:
                    TaskModel.assign_task(tid, user=user, current_user=current_user, flag_current_user=False)
                return {"message": "Users Assigned"}, 200
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404


@api.route('/<tid>/remove_assign_user', methods=['POST'])
@api.doc(description='Remove an assign user to a task', params={"tid": "id of a task"})
class RemoveAssignUser(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"user_id": "Id of a user"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                user_id = request.json["user_id"]
                if TaskModel.remove_assign_task(tid, user=user_id, current_user=current_user, flag_current_user=False):
                    return {"message": "User Removed from assignment"}, 200
                return {"message": "Error removing user from assignment"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404
    

@api.route('/list_status', methods=['GET'])
@api.doc(description='List all status')
class ListStatus(Resource):
    method_decorators = [api_required]
    def get(self):
        return [status.to_json() for status in CommonModel.get_all_status()], 200

@api.route('/<tid>/change_status', methods=['POST'])
@api.doc(description='Change status of a task', params={"tid": "id of a task"})
class ChangeStatus(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={"status_id": "Id of the new status"})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.change_task_status(request.json["status_id"], task, current_user):
                    return {"message": "Status changed"}, 200
                return {"message": "Error chnaging status"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task not found"}, 404


@api.route('/<tid>/files')
@api.doc(description='Get list of files', params={"tid": "id of a task"})
class DownloadFile(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            file_list = [file.to_json() for file in task.files]
            return {"files": file_list}, 200
        return {"message": "Task Not found"}, 404


@api.route('/<tid>/upload_file')
@api.doc(description='Upload a file')
class UploadFile(Resource):
    method_decorators = [editor_required, api_required]
    @api.doc(params={})
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                if TaskModel.add_file_core(task, request.files, current_user):
                    return {"message": "File added"}, 200
                return {"message": "Error file added"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task Not found"}, 404
    

@api.route('/<tid>/download_file/<fid>')
@api.doc(description='Download a file', params={"tid": "id of a task", "fid": "id of a file"})
class DownloadFile(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid, fid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                file = CommonModel.get_file(fid)
                if file and file in task.files:
                    return TaskModel.download_file(file)
            return {"message": "Permission denied"}, 403
        return {"message": "Task Not found"}, 404
    
@api.route('/<tid>/delete_file/<fid>')
@api.doc(description='Delete a file', params={"tid": "id of a task", "fid": "id of a file"})
class DeleteFile(Resource):
    method_decorators = [editor_required, api_required]
    def get(self, tid, fid):
        task = CommonModel.get_task(tid)
        if task:
            current_user = CaseModelApi.get_user_api(request.headers)
            if CaseModel.get_present_in_case(task.case_id, current_user) or current_user.is_admin():
                file = CommonModel.get_file(fid)
                if file and file in task.files:
                    if TaskModel.delete_file(file, task, current_user):
                        return {"message": "File Deleted"}, 200
                    return {"message": "Error File Deleted"}, 400
            return {"message": "Permission denied"}, 403
        return {"message": "Task Not found"}, 404


@api.route('/<tid>/get_taxonomies_task', methods=['GET'])
@api.doc(description='Get all tags and taxonomies in a task')
class GetTaxonomiesTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        if CommonModel.get_task(tid):
            tags = CommonModel.get_task_tags(tid)
            taxonomies = []
            if tags:
                taxonomies = [tag.split(":")[0] for tag in tags]
            return {"tags": tags, "taxonomies": taxonomies}
        return {"message": "Task Not found"}, 404


@api.route('/<tid>/get_galaxies_task', methods=['GET'])
@api.doc(description='Get all tags and taxonomies in a task')
class GetGalaxiesTask(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        if CommonModel.get_task(tid):
            clusters = CommonModel.get_task_clusters(tid)
            galaxies = []
            if clusters:
                for cluster in clusters:
                    loc_g = CommonModel.get_galaxy(cluster.galaxy_id)
                    if not loc_g.name in galaxies:
                        galaxies.append(loc_g.name)
                    index = clusters.index(cluster)
                    clusters[index] = cluster.tag
            return {"clusters": clusters, "galaxies": galaxies}
        return {"message": "task Not found"}, 404
        
@api.route('/get_connectors', methods=['GET'])
@api.doc(description='Get all connectors and instances')
class GetConnectors(Resource):
    method_decorators = [api_required]
    def get(self):
        current_user = CaseModelApi.get_user_api(request.headers)
        connectors_list = CommonModel.get_connectors()
        connectors_dict = dict()
        for connector in connectors_list:
            loc = list()
            for instance in connector.instances:
                if CommonModel.get_user_instance_both(user_id=current_user.id, instance_id=instance.id):
                    loc.append(instance.to_json())
            if loc:
                connectors_dict[connector.name] = loc
        return {"connectors": connectors_dict}, 200

@api.route('/<tid>/get_connectors_task', methods=['GET'])
@api.doc(description='Get all connectors for a task')
class GetConnectors(Resource):
    method_decorators = [api_required]
    def get(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            return {"connectors": [CommonModel.get_instance(task_instance.instance_id).name for task_instance in CommonModel.get_task_connectors(task.id) ]}, 200
        return {"message": "task Not found"}, 404

@api.route('/<tid>/get_connectors_task_id', methods=['POST'])
@api.doc(description='Get all identifier for connectors instances')
class GetConnectors(Resource):
    method_decorators = [api_required]
    @api.doc(params={
        'instances': 'Required. List of name of instances'
    })
    def post(self, tid):
        task = CommonModel.get_task(tid)
        if task:
            if "instances" in request.json:
                loc = dict()
                instances = request.json["instances"]
                for instance in instances:
                    ident = CommonModel.get_task_connector_id(CommonModel.get_instance_by_name(instance).id, task.id)
                    if ident:
                        loc[instance] = ident.identifier
                return {"instances": loc}, 200
            return {"Need to pass 'instances'"}, 400
        return {"message": "Task Not found"}, 404