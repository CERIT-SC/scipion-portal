from django import forms

class ScipoTextInput(forms.TextInput):
    def __init__(self, classes='', *args, **kwargs):
        super(ScipoTextInput, self).__init__(*args, **kwargs)

        if classes:
            self.attrs['class'] = classes


class InstancesForm(forms.Form):
    instance_name       = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Instance name")
    od_dataset_host     = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Dataset host")
    od_dataset_token    = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Dataset token")
    od_dataset_space_id = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Dataset Space ID")
    od_project_host     = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Project host")
    od_project_token    = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Project token")
    od_project_space_id = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Project Space ID")
