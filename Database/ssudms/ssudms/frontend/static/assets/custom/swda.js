$(document).ready(() => {
    $('#categoryTable').DataTable({
        "order": [0, 'desc'],
        "processing": true,
        "serverSide": true,
        "ajax": '/dashboard/api/swda/category?format=datatables',
    });

    $('#subCategoryTable').DataTable({
        "order": [0, 'desc'],
        "processing": true,
        "serverSide": true,
        "ajax": '/dashboard/api/swda/subcategory?format=datatables',
    });

    $('.categorySelect').select2({
            dropdownParent: $('#createSubCategoryFormModal'),
            width: 'resolve',
            placeholder: 'Select Category'
    });

    $('.subCategorySelect').select2({
            dropdownParent: $('#createSubCategoryFormModal'),
            width: 'resolve',
            placeholder: 'Select Category'
    });

    $('.swdaSelectProvince').select2({
            width: 'resolve',
            placeholder: 'Select Province'
    });

    $('.swdaSelectProvince').on('change', () => {
      const province = $(".swdaSelectProvince option:selected").val();
      if(province != "" || province == null){
        $.ajax({
        type: 'GET',
        url: `/dashboard/swda/`,
        data: {'province': province},
        success: (result) => {
            const city = JSON.parse(result['city']);

            $('.swdaSelectCity').select2({
                    placeholder: 'Select City'
            });

            if($(".swdaSelectCity").length == 0){
                    $('#swda_address').append('<div class="form-group mb-3 col-lg-4 swdaSelectCityDiv"><label>Select City <span class="text-danger" title="Required">*</span></label><select class="swdaSelectCity form-control" required></select></div>');
                    $('.swdaSelectCity').select2({
                            placeholder: 'Select City'
                    });
            }else{
                $('.swdaSelectCity').empty();
            }
            city.forEach((item) => {
                const data = {
                        id: item['pk'],
                        text: item['fields']['name']
                    };

                    const newOption = new Option(data.text, data.id, false, false);
                    $('.swdaSelectCity').append(newOption);
            });
            $('.swdaSelectCity').trigger('change');
            /* CDC Select City Event */
            $('.swdaSelectCity').on('change', () => {
                const city = $(".swdaSelectCity option:selected").val();
                if(city != "" || city != null){
                    $.ajax({
                    type: 'GET',
                    url: `/dashboard/swda/`,
                    data: {'city': city},
                    success: (result) => {
                        const barangay = JSON.parse(result['barangay']);
                        $('.swdaSelectBarangay').select2({
                                placeholder: 'Select Barangay'
                        });

                        if($(".swdaSelectBarangay").length == 0){
                                $('#swda_address').append('<div class="form-group mb-3 col-lg-4 swdaSelectBarangayDiv"><label>Select Barangay <span class="text-danger" title="Required">*</span></label><select class="swdaSelectBarangay form-control" name="barangay" required></select></div>');
                                $('.swdaSelectBarangay').select2({
                                        placeholder: 'Select Barangay'
                                });
                        }else{
                            $('.swdaSelectBarangay').empty();
                        }

                        barangay.forEach((item) => {
                            const data = {
                                    id: item['pk'],
                                    text: item['fields']['name']
                                };

                                const newOption = new Option(data.text, data.id, false, false);
                                $('.swdaSelectBarangay').append(newOption).trigger('change');
                        });
                    },
                    error: (result) => {
                        console.log(result)
                    }
                  });
                }
            });

            /* End */

        },
        error: (result) => {
            console.log(result)
        }
      });
      }
    });

    $('#id_aoo_province').select2({
            width: 'resolve',
            placeholder: 'Select Province'
    });

    $('#id_aoo_province').on('change', () => {
      const province = $("#id_aoo_province option:selected").val();
      if(province != "" || province == null){
        $.ajax({
        type: 'GET',
        url: `/dashboard/swda/`,
        data: {'province': province},
        success: (result) => {
            const city = JSON.parse(result['city']);

            $('.id_aoo_city').select2({
                    placeholder: 'Select City'
            });

            if($(".id_aoo_city").length == 0){
                    $('#aoo_address').append('<div class="form-group mb-3 col-lg-4 aooSelectCityDiv"><label>Select City <span class="text-danger" title="Required">*</span></label><select class="id_aoo_city form-control" required></select></div>');
                    $('.id_aoo_city').select2({
                            placeholder: 'Select City'
                    });
            }else{
                $('.id_aoo_city').empty();
            }
            city.forEach((item) => {
                const data = {
                        id: item['pk'],
                        text: item['fields']['name']
                    };

                    const newOption = new Option(data.text, data.id, false, false);
                    $('.id_aoo_city').append(newOption);
            });
            $('.id_aoo_city').trigger('change');
            /* CDC Select City Event */
            $('.id_aoo_city').on('change', () => {
                const city = $(".id_aoo_city option:selected").val();
                if(city != "" || city != null){
                    $.ajax({
                    type: 'GET',
                    url: `/dashboard/swda/`,
                    data: {'city': city},
                    success: (result) => {
                        const barangay = JSON.parse(result['barangay']);
                        $('.id_aoo_barangay').select2({
                                placeholder: 'Select Barangay'
                        });

                        if($(".id_aoo_barangay").length == 0){
                                $('#aoo_address').append('<div class="form-group mb-3 col-lg-4 aooSelectBarangayDiv"><label>Select Barangay <span class="text-danger" title="Required">*</span></label><select class="id_aoo_barangay form-control" name="aoobarangay" required></select></div>');
                                $('.id_aoo_barangay').select2({
                                        placeholder: 'Select Barangay'
                                });
                        }else{
                            $('.id_aoo_barangay').empty();
                        }

                        barangay.forEach((item) => {
                            const data = {
                                    id: item['pk'],
                                    text: item['fields']['name']
                                };

                                const newOption = new Option(data.text, data.id, false, false);
                                $('.id_aoo_barangay').append(newOption).trigger('change');
                        });
                    },
                    error: (result) => {
                        console.log(result)
                    }
                  });
                }
            });

            /* End */

        },
        error: (result) => {
            console.log(result)
        }
      });
      }
    });

    $('.subCategorySelect').select2({
            width: 'resolve',
            placeholder: 'Select sub category'
    });


    $('#createCategoryBtn').on('click', () => {
        $('#createCategoryFormModal').modal('toggle');
    });

    $('#createSubCategoryBtn').on('click', () => {
        $('#createSubCategoryFormModal').modal('toggle');
    });

    $('#categoryForm').on('submit', (e) =>{
        e.preventDefault();
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
          if (result.isConfirmed) {
            const formData = $('#categoryForm').serialize();
            $.ajax({
                type: 'POST',
                url: '/dashboard/swda/?action=category',
                data: formData,
                success: (result) => {
                    const statusMsg = result['statusMsg'];
                    Swal.fire(
                      'Success!',
                      statusMsg,
                      'success'
                    ).then(() => {
                        $('#categoryForm').trigger('reset');
                    });
                },
                error: (result) => {
                    console.log(result)
                    setTimeout(() => {
                        const statusMsg = result['responseJSON']['statusMsg'];

                        $('.csoFormMessage').addClass('text-danger').removeClass('text-success').text(statusMsg);
                        $('#loadingSpinnerModal').modal('toggle');
                    }, 500);
                }

            });
          }
        });
    });

    $('#subCategoryForm').on('submit', (e) =>{
        e.preventDefault();
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
          if (result.isConfirmed) {
            const formData = $('#subCategoryForm').serialize();
            $.ajax({
                type: 'POST',
                url: '/dashboard/swda/?action=subcategory',
                data: formData,
                success: (result) => {
                    const statusMsg = result['statusMsg'];
                    Swal.fire(
                      'Success!',
                      statusMsg,
                      'success'
                    ).then(() => {
                        $('#subCategoryForm').trigger('reset');
                    });
                },
                error: (result) => {
                    setTimeout(() => {
                        const statusMsg = result['responseJSON']['statusMsg'];

                        $('.csoFormMessage').addClass('text-danger').removeClass('text-success').text(statusMsg);
                        $('#loadingSpinnerModal').modal('toggle');
                    }, 500);
                }

            });
          }
        });
    });

    $('#swdaForm').on('submit', (e) => {
        e.preventDefault();
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = $('#swdaForm').serialize();
                $.ajax({
                    type: 'POST',
                    url: '/dashboard/swda/?action=swdaform',
                    data: formData,
                    success: (result) => {
                        const statusMsg = result['statusMsg'];
                        const errors = result['errors'];
                        console.log(errors)
                        if(errors.length > 0){
                            Swal.fire({
                            title: '<strong>Errors!</strong',
                            icon: 'warning',
                            html: 'Errors with duplicate number, click <a href="/dashboard/swda/?action=updateswda">here</a> to update.',
                            showCloseButton: true,
                            }).then(() => {
                                $('#swdaForm').trigger('reset');
                            })
                        }

                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        Swal.fire(
                          'Error!',
                          statusMsg,
                          'error'
                        ).then(() => {
                            $('#subCategoryForm').trigger('reset');
                        });
                    }

                });
            }
        });
    });

});