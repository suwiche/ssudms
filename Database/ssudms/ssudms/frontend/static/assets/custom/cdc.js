$(document).ready(() => {

    $('#cdcTable').DataTable({
        "order": [0, 'desc'],
        "processing": true,
        "serverSide": true,
        "ajax": '/dashboard/api/cdc?format=datatables',
        "columnDefs": [
            {
                "targets": [1, 3, 4, 5, 6, 7],
                "orderable": false,
                "searchable": false
            }
        ]
    });

    $('#cdwTable').DataTable({
        "order": [0, 'desc'],
        "processing": true,
        "serverSide": true,
        "ajax": '/dashboard/api/cdw?format=datatables',
        "columnDefs": [
            {
                "targets": [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "orderable": false,
                "searchable": false
            },
        ]
    });

    $('#cdccdwTable').DataTable({
        "order": [0, 'desc'],
        "processing": true,
        "serverSide": true,
        "ajax": '/dashboard/api/cdccdw?format=datatables',
        "columnDefs": [
            {
                "render": function(data, type, row){
                    return 'Assessed by Deputized Accreditor'
                },
                "targets": [13]
            }
        ]
    });

    $('#createCdcBtn').on('click', () => {
        $('#createCDCFormModal').modal('toggle');
    });

    $('#createCdwBtn').on('click', () => {
        $('#createCDWFormModal').modal('toggle');
    });

    $('.cdcSelectProvince').select2({
            dropdownParent: $('#createCDCFormModal'),
            width: 'resolve',
            placeholder: 'Select Province'
    });

    $('.cdwSelectProvince').select2({
            dropdownParent: $('#createCDWFormModal'),
            width: 'resolve',
            placeholder: 'Select Province'
    });

    $('.cdcSelect').select2({
            dropdownParent: $('#createCDWFormModal'),
            width: 'resolve',
            placeholder: 'Select Center'
    });

    $('#createCDCFormModal').on('hidden.bs.modal', function () {
        location.reload();
    });

    $('#createCDWFormModal').on('hidden.bs.modal', function () {
        location.reload();
    });

    $('.cdcSelectProvince').on('change', () => {
      const province = $(".cdcSelectProvince option:selected").val();
      if(province != "" || province == null){
        $.ajax({
        type: 'GET',
        url: `/dashboard/cdc/`,
        data: {'province': province},
        success: (result) => {
            const city = JSON.parse(result['city']);

            $('.cdcSelectCity').select2({
                    dropdownParent: $('#createCDCFormModal'),
                    placeholder: 'Select City'
            });

            if($(".cdcSelectCity").length == 0){
                    $('#cdc_address').append('<div class="form-group mb-3 col-lg-4 cdcSelectCityDiv"><label>Select City <span class="text-danger" title="Required">*</span></label><select class="cdcSelectCity form-control" required></select></div>');
                    $('.cdcSelectCity').select2({
                            dropdownParent: $('#createCDCFormModal'),
                            placeholder: 'Select City'
                    });
            }else{
                $('.cdcSelectCity').empty();
            }
            city.forEach((item) => {
                const data = {
                        id: item['pk'],
                        text: item['fields']['name']
                    };

                    const newOption = new Option(data.text, data.id, false, false);
                    $('.cdcSelectCity').append(newOption);
            });
            $('.cdcSelectCity').trigger('change');
            /* CDC Select City Event */
            $('.cdcSelectCity').on('change', () => {
                const city = $(".cdcSelectCity option:selected").val();
                if(city != "" || city != null){
                    $.ajax({
                    type: 'GET',
                    url: `/dashboard/cdc/`,
                    data: {'city': city},
                    success: (result) => {
                        const barangay = JSON.parse(result['barangay']);
                        $('.cdcSelectBarangay').select2({
                                dropdownParent: $('#createCDCFormModal'),
                                placeholder: 'Select Barangay'
                        });

                        if($(".cdcSelectBarangay").length == 0){
                                $('#cdc_address').append('<div class="form-group mb-3 col-lg-4 cdcSelectBarangayDiv"><label>Select Barangay <span class="text-danger" title="Required">*</span></label><select class="cdcSelectBarangay form-control" name="barangay" required></select></div>');
                                $('.cdcSelectBarangay').select2({
                                        dropdownParent: $('#createCDCFormModal'),
                                        placeholder: 'Select Barangay'
                                });
                        }else{
                            $('.cdcSelectBarangay').empty();
                        }

                        barangay.forEach((item) => {
                            const data = {
                                    id: item['pk'],
                                    text: item['fields']['name']
                                };

                                const newOption = new Option(data.text, data.id, false, false);
                                $('.cdcSelectBarangay').append(newOption).trigger('change');
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

    $('.cdwSelectProvince').on('change', () => {
      const province = $(".cdwSelectProvince option:selected").val();
      if(province != "" || province == null){
        $.ajax({
        type: 'GET',
        url: `/dashboard/cdc/`,
        data: {'province': province},
        success: (result) => {
            const city = JSON.parse(result['city']);

            $('.cdwSelectCity').select2({
                    dropdownParent: $('#createCDWFormModal'),
                    placeholder: 'Select City'
            });

            if($(".cdwSelectCity").length == 0){
                    $('#cdw_address').append('<div class="form-group mb-3 col-lg-4 cdwSelectCityDiv"><label>Select City <span class="text-danger" title="Required">*</span></label><select class="cdwSelectCity form-control" required></select></div>');
                    $('.cdwSelectCity').select2({
                            dropdownParent: $('#createCDWFormModal'),
                            placeholder: 'Select City'
                    });
            }else{
                $('.cdwSelectCity').empty();
            }
            city.forEach((item) => {
                const data = {
                        id: item['pk'],
                        text: item['fields']['name']
                    };

                    const newOption = new Option(data.text, data.id, false, false);
                    $('.cdwSelectCity').append(newOption);
            });
            $('.cdwSelectCity').trigger('change');
            /* CDC Select City Event */
            $('.cdwSelectCity').on('change', () => {
                const city = $(".cdwSelectCity option:selected").val();
                if(city != "" || city != null){
                    $.ajax({
                    type: 'GET',
                    url: `/dashboard/cdc/`,
                    data: {'city': city},
                    success: (result) => {
                        const barangay = JSON.parse(result['barangay']);
                        $('.cdwSelectBarangay').select2({
                                dropdownParent: $('#createCDWFormModal'),
                                placeholder: 'Select Barangay'
                        });

                        if($(".cdwSelectBarangay").length == 0){
                                $('#cdw_address').append('<div class="form-group mb-3 col-lg-4 cdwSelectBarangayDiv"><label>Select Barangay <span class="text-danger" title="Required">*</span></label><select class="cdwSelectBarangay form-control" name="barangay" required></select></div>');
                                $('.cdwSelectBarangay').select2({
                                        dropdownParent: $('#createCDWFormModal'),
                                        placeholder: 'Select Barangay'
                                });
                        }else{
                            $('.cdwSelectBarangay').empty();
                        }

                        barangay.forEach((item) => {
                            const data = {
                                    id: item['pk'],
                                    text: item['fields']['name']
                                };

                                const newOption = new Option(data.text, data.id, false, false);
                                $('.cdwSelectBarangay').append(newOption).trigger('change');
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

    $('#cdcForm').on('submit', (e) => {
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
            const formData = $('#cdcForm').serialize();
            $.ajax({
                type: 'POST',
                url: '/dashboard/cdc/',
                data: formData,
                success: (result) => {
                    const statusMsg = result['statusMsg'];
                    Swal.fire(
                      'Success!',
                      statusMsg,
                      'success'
                    ).then(() => {
                        $('#cdcForm').trigger('reset');
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

    $('#cdwForm').on('submit', (e) => {
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
            const formData = $('#cdwForm').serialize();
            $.ajax({
                type: 'POST',
                url: '/dashboard/cdw/',
                data: formData,
                success: (result) => {
                    const statusMsg = result['statusMsg'];
                    Swal.fire(
                      'Success!',
                      statusMsg,
                      'success'
                    ).then(() => {
                        $('#cdwForm').trigger('reset');
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

    $('#generateReportFilterBtn').on('click', () => {
        $('#generateReportFilterModal').remove();
        $('#generate-modal').append(`
        <div class="modal fade" id="generateReportFilterModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="exampleModalLabel">Filter</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form id="generateReportFilterForm" method="GET">
                                                    <div class="form-group mb-3">
                                                        <label>Program:</label>
                                                        <select class="form-control" name="program" required>
                                                            <option value="worker">Child Development Worker</option>
                                                            <option value="center">Child Development Center</option>
                                                        </select>
                                                    </div>
                                                    <div class="form-group">
                                                        <label>Type:</label>
                                                        <select class="form-control" name="type" required>
                                                            <option value="issued">Issued</option>
                                                            <option value="expiry">Expiry</option>
                                                        </select>
                                                    </div>
                                                    <br>
                                                    <div class="form-group">
                                                        <label>From:</label>
                                                        <input name="from" type="date" class="form-control" required>
                                                    </div>
                                                    <br>
                                                    <div class="form-group">
                                                        <label>To:</label>
                                                        <input name="to" type="date" class="form-control" required>
                                                    </div>
                                                    <div class="d-flex justify-content-between mt-3">
                                                        <label id="generateReportFilterMessage"></label>
                                                        <button class="btn btn-success" style="height:38px;">Submit</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                            </div>`);
        $('#generateReportFilterModal').modal('toggle');
        generateReportFilterFunc();
    });

    const generateReportFilterFunc = () => {
        $('#generateReportFilterForm').on('submit', (e) => {
            e.preventDefault();
            const formData = $('#generateReportFilterForm').serialize();
            $.ajax({
                type: 'GET',
                url: '/dashboard/cdc/generate',
                data: formData,
                success: (result) => {
                    const form1 = result['form1'];
                    const form2 = result['form2'];
                    const count = result['count'];
                    $('#generateReportFilterMessage').empty();
                    $('#generateReportFilterMessage').append(` <div class="d-flex justify-content-center"> Download ${count} result(s) &nbsp; ${form1} &nbsp;|&nbsp; ${form2}</div>`).removeClass('text-danger');
                },
                error: (result) => {
                    const statusMsg = result['responseJSON']['statusMsg'];

                    $('#generateReportFilterMessage').empty();
                    $('#generateReportFilterMessage').append(statusMsg).addClass('text-danger');
                }
            });
        });
    }




});