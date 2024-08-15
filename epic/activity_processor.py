from datetime import datetime
from epic_sdk_scripts_rbdundas.models.Activity import Activity

import epic.processor
from amsforms.models import AMSObjectType, AMSObjectValueDefault, FormToAMSValueMapping
from amsforms import processor


def set_activity_defaults(activity: Activity):
    ams_value_defaults = AMSObjectValueDefault.objects.filter(AMSObjectType__AMSObjectType='Activity').all()
    activity.StatusOption.OptionName = 'Open'
    activity.StatusOption.Value = '0'
    now = datetime.now()
    activity.DetailValue.FollowUpStartDate = now.strftime("%Y-%m-%dT%H:%M:%S")
    return activity


def create_ams_object(ams_object: Activity, converted_values: dict, ams_object_type: AMSObjectType) -> Activity:
    activity = ams_object
    activity = set_activity_defaults(activity)
    mappings = FormToAMSValueMapping.objects.filter(AMSObjectType=ams_object_type, AMSObjectValue__AMSField='NoteText').all()
    activity.Notes = []
    note_item = activity.NoteItem()
    for mapping in mappings:
        field = next(epic.processor.get_value_from_nested_dict(converted_values, mapping.FormField))
        note_item.NoteText += field + '\r\n'
    activity.Notes.append(note_item)
    return activity
