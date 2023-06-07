$(document).ready(() => {
    $('table.datatable').DataTable();
    var s2o = {
		placeholder: "Select",
		width: 'resolve',
    }

    if($('#addUserForm').length){
        $('#id_group').select2({
			placeholder: "Select",
            dropdownParent: $('#addUserForm'),
            width: 'resolve',
        });
    } else if($('#updateUserForm').length){
        $('#id_group').select2({
			placeholder: "Select",
            width: 'resolve',
        });
    }

    if($('#addExtensionForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addExtensionModal'),
            width: 'resolve',
        });
    } else if($('#updateExtensionForm').length){
        $('#id_status').select2(s2o);
    }

    if($('#addProcessForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addProcessModal'),
            width: 'resolve',
        });
    }else if($('#updateProcessForm').length){
        $('#id_status').select2(s2o);
    }

    if($('#addServicesForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addServicesModal'),
            width: 'resolve',
        });
    }else if($('#updateServicesForm').length){
        $('#id_status').select2(s2o);
    }

    if($('#addTypeForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addTypeForm'),
            width: 'resolve',
        });
        $('#id_has_worker').select2({
			placeholder: "Select",
            dropdownParent: $('#addTypeForm'),
            width: 'resolve',
        });
        $('#id_is_worker').select2({
			placeholder: "Select",
            dropdownParent: $('#addTypeForm'),
            width: 'resolve',
        });
    }else if($('#updateTypeForm').length){
        $('#id_status').select2(s2o);
        $('#id_has_worker').select2(s2o);
        $('#id_is_worker').select2(s2o);
    }

    if($('#addStatusForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addStatusModal'),
            width: 'resolve',
        });
    }else if($('#updateStatusForm').length){
        $('#id_status').select2(s2o);
    }

    if($('#addLevelForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addLevelModal'),
            width: 'resolve',
        });
    }else if($('#updateLevelForm').length){
        $('#id_status').select2(s2o);
    }

    if($('#addFormForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormModal'),
            width: 'resolve',
        });

        $('#id_org_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormModal'),
            width: 'resolve',
        });

        $('#id_orientation').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormModal'),
            width: 'resolve',
        });

        $('#id_form_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormModal'),
            width: 'resolve',
        });

    }else if($('#updateFormForm').length){
        $('#id_status').select2(s2o);
        $('#id_org_type').select2(s2o);
        $('#id_orientation').select2(s2o);
        $('#id_form_type').select2(s2o);
    }

    if($('#addFormVersion').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormVersionModal'),
            width: 'resolve',
        });

        $('#id_form').select2({
			placeholder: "Select",
            dropdownParent: $('#addFormVersionModal'),
            width: 'resolve',
        });

    }else if($('#updateVersionForm').length){
        $('#id_status').select2(s2o);
        $('#id_form').select2(s2o);
    }

    if($('#addDetailsAttributeForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addDetailsAttributeForm'),
            width: 'resolve',
        });
        $('#id_is_required').select2({
			placeholder: "Select",
            dropdownParent: $('#addDetailsAttributeForm'),
            width: 'resolve',
        });
        $('#id_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addDetailsAttributeForm'),
            width: 'resolve',
        });
        $('#id_input_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addDetailsAttributeForm'),
            width: 'resolve',
        });
    }else if($('#updateDetailsAttributeForm').length){
        $('#id_status').select2(s2o);
        $('#id_is_required').select2(s2o);
        $('#id_type').select2(s2o);
        $('#id_input_type').select2(s2o);
    }

    if($('#addWorkerAttributeForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addWorkerAttributeForm'),
            width: 'resolve',
        });
        $('#id_is_required').select2({
			placeholder: "Select",
            dropdownParent: $('#addWorkerAttributeForm'),
            width: 'resolve',
        });
        $('#id_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addWorkerAttributeForm'),
            width: 'resolve',
        });
        $('#id_input_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addWorkerAttributeForm'),
            width: 'resolve',
        });
    }else if($('#updateWorkerAttributeForm').length){
        $('#id_status').select2(s2o);
        $('#id_is_required').select2(s2o);
        $('#id_type').select2(s2o);
        $('#id_input_type').select2(s2o);
    }

    if($('#addTransactionAttributeForm').length){
        $('#id_status').select2({
			placeholder: "Select",
            dropdownParent: $('#addTransactionAttributeForm'),
            width: 'resolve',
        });
        $('#id_is_required').select2({
			placeholder: "Select",
            dropdownParent: $('#addTransactionAttributeForm'),
            width: 'resolve',
        });
        $('#id_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addTransactionAttributeForm'),
            width: 'resolve',
        });
        $('#id_input_type').select2({
			placeholder: "Select",
            dropdownParent: $('#addTransactionAttributeForm'),
            width: 'resolve',
        });
    }else if($('#updateTransactionAttributeForm').length){
        $('#id_status').select2(s2o);
        $('#id_is_required').select2(s2o);
        $('#id_type').select2(s2o);
        $('#id_input_type').select2(s2o);
    }


    $('form.addForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to create and save this new entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully created an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const error = result['responseJSON']['error'];
                        swal({
                            title: 'Error',
                            text: error,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.addVersionForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to create and save this new entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully created an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const error = result['responseJSON']['error'];
                        swal({
                            title: 'Error',
                            text: error,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.updateForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to update and save this entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully updated an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.updateVersionForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to update and save this entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully updated an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

     $('form.addWorkerAttributeForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to create and save this new entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully created an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.updateWorkerAttributeForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to update and save this entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully updated an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.addTransactionAttributeForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to create and save this new entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully created an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

    $('form.updateTransactionAttributeForm').on('submit', (e) => {
        var form_id = (e.target.id);
        e.preventDefault(e);
        swal({
            title: "Are you sure",
            text: "You want to update and save this entry?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((result) => {
            const formData = $('#'+form_id).serialize();
            const url = $('#'+form_id).attr('action');
            const type = $('#'+form_id).attr('method');
            if (result) {
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        swal({
                            title: "Success",
                            text: "You have successfully updated an entry.",
                            icon: "success",
                        }).then(() => {
                            location.reload(true);
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        const errors = result['responseJSON']['errors'];

                        $('.errors').empty();
                        errors.forEach((error) => {
                            $('.errors').append(`<li><label class="text-danger">${error}</label></li>`)
                        });
                        swal({
                            title: 'Error',
                            text: statusMsg,
                            icon: "error",
                        });
                    }
                });
            }
        })
    });

});

var notify_settings = {
	type:'danger',
	allow_dismiss:false,
	newest_on_top:true ,
	mouse_over:false,
	showProgressbar:false,
	spacing:10,
	timer:2000,
	placement:{
		from:'top',
		align:'right'
	},
	offset:{
		x:30,
		y:30
	},
	delay:500,
	z_index:10000,
	animate:{
		enter:'animated bounce',
		exit:'animated fadeOut'
	}
};