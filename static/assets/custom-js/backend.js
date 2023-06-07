$(document).ready(() => {
    $('#extensions_table').DataTable();
    $('#level_table').DataTable();
    $('#process_table').DataTable();
    $('#services_table').DataTable();
    $('#status_table').DataTable();
    $('#types_table').DataTable();
    $('#users_table').DataTable();

    if($('#addUserForm').length){
        $('#id_group').select2({
            dropdownParent: $('#addUserForm'),
            width: 'resolve',
        });
    }else if($('#updateUserForm').length){
        $('#id_group').select2({
            width: 'resolve',
        });
    }

    if($('#addExtensionForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addExtensionModal'),
            width: 'resolve',
        });
    }else if($('#updateExtensionForm').length){
        $('#id_status').select2();
    }

    if($('#addProcessForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addProcessModal'),
            width: 'resolve',
        });
    }else if($('#updateProcessForm').length){
        $('#id_status').select2();
    }

    if($('#addServicesForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addServicesModal'),
            width: 'resolve',
        });
    }else if($('#updateServicesForm').length){
        $('#id_status').select2();
    }

    if($('#addTypeForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addTypeModal'),
            width: 'resolve',
        });
    }else if($('#updateTypeForm').length){
        $('#id_status').select2();
    }


    if($('#addFormVersion').length){
        $('#id_status').select2({
            dropdownParent: $('#addFormVersionModal'),
            width: 'resolve',
        });
    }else if($('#addFormVersion').length){
        $('#id_status').select2();
    }

    if($('#addFormVersion').length){
        $('#id_form').select2({
            dropdownParent: $('#addFormVersionModal'),
            width: 'resolve',
        });
    }else if($('#updateFormVersion').length){
        $('#id_form').select2();
    }


    if($('#addStatusForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addStatusModal'),
            width: 'resolve',
        });
    }else if($('#updateStatusForm').length){
        $('#id_status').select2();
    }

    if($('#addLevelForm').length){
        $('#id_status').select2({
            dropdownParent: $('#addLevelModal'),
            width: 'resolve',
        });
    }else if($('#updateLevelForm').length){
        $('#id_status').select2();
    }

    $("#addUserModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addExtensionModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addProcessModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addTypeModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addServicesModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addStatusModal").on('hide.bs.modal',() => {
        location.reload(true);
    });

    $("#addLevelModal").on('hide.bs.modal',() => {
        location.reload(true);
    });



    $('#addUserForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addUserForm').serialize();
                const url = $('#addUserForm').attr('action');
                const type = $('#addUserForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#id_group').val('').trigger('change');
                                $('#addUserForm').trigger('reset');
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

    $('#updateUserForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateUserForm').serialize();
                const url = $('#updateUserForm').attr('action');
                const type = $('#updateUserForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                location.reload();
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

    $('#addExtensionForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addExtensionForm').serialize();
                const url = $('#addExtensionForm').attr('action');
                const type = $('#addExtensionForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addExtensionForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateExtensionForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateExtensionForm').serialize();
                const type = $('#updateExtensionForm').attr('method');
                const url = $('#updateExtensionForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateExtensionForm').trigger('reset');
                                location.reload();
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

     $('#addProcessForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addProcessForm').serialize();
                const url = $('#addProcessForm').attr('action');
                const type = $('#addProcessForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addProcessForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateProcessForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateProcessForm').serialize();
                const type = $('#updateProcessForm').attr('method');
                const url = $('#updateProcessForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateProcessForm').trigger('reset');
                                location.reload();
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

     $('#addServicesForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addServicesForm').serialize();
                const type = $('#addServicesForm').attr('method');
                const url = $('#addServicesForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addServicesForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateServicesForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateServicesForm').serialize();
                const type = $('#updateServicesForm').attr('method');
                const url = $('#updateServicesForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateServicesForm').trigger('reset');
                                location.reload();
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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


    $('#addTypeForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addTypeForm').serialize();
                const type = $('#addTypeForm').attr('method');
                const url = $('#addTypeForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addTypeForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateTypeForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateTypeForm').serialize();
                const type = $('#updateTypeForm').attr('method');
                const url = $('#updateTypeForm').attr('action')
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateTypeForm').trigger('reset');
                                location.reload();
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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


    $('#addStatusForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addStatusForm').serialize();
                const url = $('#addStatusForm').attr('action');
                const type = $('#addStatusForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addStatusForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateStatusForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateStatusForm').serialize();
                const url = $('#updateStatusForm').attr('action');
                const type = $('#updateStatusForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateStatusForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#addLevelForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#addLevelForm').serialize();
                if (result) {
                    $.ajax({
                        type: 'POST',
                        url: '/admin/level/',
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#addLevelForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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

    $('#updateLevelForm').on('submit', (e) => {
        e.preventDefault(e);
        swal({
                title: "Are you sure?",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((result) => {
                const formData = $('#updateLevelForm').serialize();
                const url = $('#updateLevelForm').attr('action');
                const type = $('#updateLevelForm').attr('method');
                if (result) {
                    $.ajax({
                        type: type,
                        url: url,
                        data: formData,
                        success: (result) => {
                            swal({
                                title: "Success",
                                icon: "success",
                            }).then(() => {
                                $('#updateLevelForm').trigger('reset');
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
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