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

    od_dataset_space_name = forms.TypedChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Dataset Space ID",
        choices=[], # Empty for now, will be populated by constructor
        coerce=str
    )

    od_project_host     = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Project host")
    od_project_token    = forms.CharField(required=True, widget=ScipoTextInput(classes="form-control"), label="Project token")

    od_project_space_name = forms.TypedChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Project Space ID",
        choices=[], # Empty for now, will be populated by constructor
        coerce=str
    )

    def __init__(self, dataset_space_names, project_space_names, *args, **kwargs):
        super(InstancesForm, self).__init__(*args, **kwargs)

        dataset_space_names = [(item, item) for item in dataset_space_names]
        project_space_names = [(item, item) for item in project_space_names]

        self.fields['od_dataset_space_name'].choices = dataset_space_names
        self.fields['od_project_space_name'].choices = project_space_names
