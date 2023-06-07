$(document).ready(() => {
    $('#csoTable').DataTable({
        "order": [1, 'desc'],
        "paging":   false,
        "info":     false
    });

    $('.csoSelectProvince').select2({
            placeholder: 'Select Province'
    });

    $('.csoSelectProvince').on('change', () => {
      const province = $(".csoSelectProvince option:selected").val();
      if(province != "" || province == null){
        $.ajax({
        type: 'GET',
        url: `/cso/`,
        data: {'province': province},
        success: (result) => {
            const city = JSON.parse(result['city']);

            $('.csoSelectCity').select2({
                    placeholder: 'Select City'
            });

            if($(".csoSelectCity").length == 0){
                    $('#cso_address').append('<div class="form-group mb-3 col-lg-4 csoSelectCityDiv"><label>Select City <span class="text-danger" title="Required">*</span></label><select class="csoSelectCity form-control" required></select></div>');
                    $('.csoSelectCity').select2({
                            placeholder: 'Select City'
                    });
            }else{
                $('.csoSelectCity').empty();
            }
            city.forEach((item) => {
                const data = {
                        id: item['pk'],
                        text: item['fields']['name']
                    };

                    const newOption = new Option(data.text, data.id, false, false);
                    $('.csoSelectCity').append(newOption);
            });
            $('.csoSelectCity').trigger('change');
            /* CSO Select City Event */
            $('.csoSelectCity').on('change', () => {
                const city = $(".csoSelectCity option:selected").val();
                if(city != "" || city != null){
                    $.ajax({
                    type: 'GET',
                    url: `/cso/`,
                    data: {'city': city},
                    success: (result) => {
                        const barangay = JSON.parse(result['barangay']);
                        $('.csoSelectBarangay').select2({
                                placeholder: 'Select Barangay'
                        });

                        if($(".csoSelectBarangay").length == 0){
                                $('#cso_address').append('<div class="form-group mb-3 col-lg-4 csoSelectBarangayDiv"><label>Select Barangay <span class="text-danger" title="Required">*</span></label><select class="csoSelectBarangay form-control" name="barangay" required></select></div>');
                                $('.csoSelectBarangay').select2({
                                        placeholder: 'Select Barangay'
                                });
                        }else{
                            $('.csoSelectBarangay').empty();
                        }

                        barangay.forEach((item) => {
                            const data = {
                                    id: item['pk'],
                                    text: item['fields']['name']
                                };

                                const newOption = new Option(data.text, data.id, false, false);
                                $('.csoSelectBarangay').append(newOption).trigger('change');
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
        </div>`)
        $('#generateReportFilterModal').modal('toggle');
        generateReportFilterFunc();
    });

    const generateReportFilterFunc = () => {
        $('#generateReportFilterForm').on('submit', (e) => {
        e.preventDefault();
        const formData = $('#generateReportFilterForm').serialize();
        $.ajax({
            type: 'GET',
            url: '/dashboard/cso/generate',
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

    $('#csoForm').on('submit', (e) => {
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
            const formData = $('#csoForm').serialize();
            $.ajax({
                type: 'POST',
                url: '/cso/add/',
                data: formData,
                success: (result) => {
                    const statusMsg = result['statusMsg'];
                    Swal.fire(
                      'Success!',
                      statusMsg,
                      'success'
                    ).then(() => {
                        $('#csoForm').trigger('reset');
                    });
                },
                error: (result) => {
                    const statusMsg = result['responseJSON']['statusMsg'];
                    Swal.fire({
                        icon: 'error',
                        title: 'Ooops...',
                        text: statusMsg,
                    });
                }

            });
          }
        });
    });

    $('#csoOrgForm').on('submit', (e) => {
        e.preventDefault()
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = $('#csoOrgForm').serialize();
                const url = $('#csoOrgForm').attr('action');
                const type = $('#csoOrgForm').attr('method');
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        const statusMsg = result['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'success',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'error',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    }
                });
            }
        });
    });

    $('#csoContactForm').on('submit', (e) => {
        e.preventDefault()
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = $('#csoContactForm').serialize();
                const url = $('#csoContactForm').attr('action');
                const type = $('#csoContactForm').attr('method');
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        const statusMsg = result['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'success',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'error',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    }
                });

            }
        });
    });

    $('#csoContactPersonForm').on('submit', (e) => {
        e.preventDefault()
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = $('#csoContactPersonForm').serialize();
                const url = $('#csoContactPersonForm').attr('action');
                const type = $('#csoContactPersonForm').attr('method');
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        const statusMsg = result['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'success',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'error',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    }
                });
            }
        });
    });

    $('#csoTransactionForm').on('submit', (e) => {
        e.preventDefault()
        Swal.fire({
          title: 'Are you sure?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#28a745',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Confirm'
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = $('#csoTransactionForm').serialize();
                const url = $('#csoTransactionForm').attr('action');
                const type = $('#csoTransactionForm').attr('method');
                $.ajax({
                    type: type,
                    url: url,
                    data: formData,
                    success: (result) => {
                        const statusMsg = result['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'success',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    },
                    error: (result) => {
                        const statusMsg = result['responseJSON']['statusMsg'];
                        Swal.fire({
                          position: 'top-end',
                          icon: 'error',
                          title: statusMsg,
                          showConfirmButton: false,
                          timer: 1500
                        }).then(() => {
                            location.reload();
                        });
                    }
                });

            }
        });
    });

    $('#csoTable tbody').on('click', '#addTransactionBtn', function(){
        const table = $('#csoTable').DataTable().row( $(this).parents('tr') ).data();
        const cso_id = table[1];
        $.ajax({
            type: 'GET',
            url: `/cso/add/`,
            data: {'action': 'transaction', 'cso_id': cso_id},
            success: (result) => {
                const cso_id = result['cso_id'];

                $('#csoAddTransactionModal').remove();
                $('#generate-modal').append(`
                    <div class="modal fade" id="csoAddTransactionModal" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">>
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">
                                    Add Control No.
                                </h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                  <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <form id="csoAddTransactionForm" method="POST">
                                    <input type="hidden" name="cso_id" value="${cso_id}" required>
                                    <div class="form-group mb-3">
                                        <label>Control no <small class="text-danger">*</small></label>
                                        <input type="text" max_length="50" required name="control_no" class="form-control" placeholder="Enter Control no.">
                                    </div>
                                    <div class="form-group mb-3">
                                        <label>Date Issued <small class="text-danger">*</small></label>
                                        <input type="date" required name="date_issued" class="form-control" placeholder="Enter Date Issued.">
                                    </div>
                                    <div class="form-group">
                                        <label>Years<small class="text-danger">*</small></label>
                                        <input type="number" required name="years" class="form-control" placeholder="Enter years.">
                                    </div>
                                    <div class="d-flex justify-content-end mt-3">
                                        <button class="btn btn-primary" type="submit">Submit</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                `);
                $('#csoAddTransactionModal').modal('toggle');
                csoAddTransactionFunc(cso_id);
            }
        });
    });
    const csoAddTransactionFunc = (cso_id) => {
        $('#csoAddTransactionForm').on('submit', (e) => {
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
                    const formData = $('#csoAddTransactionForm').serialize();
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    $.ajax({
                        type: 'POST',
                        url: `/cso/add/?action=transaction&cso_id=${cso_id}`,
                        data: formData,
                        headers: { "X-CSRFToken": csrftoken },
                        success: (result) => {
                            const statusMsg = result['statusMsg'];
                            $('#csoAddTransactionModal').modal('toggle');
                            Swal.fire({
                              position: 'top-end',
                              icon: 'success',
                              title: statusMsg,
                              showConfirmButton: false,
                              timer: 1500
                            }).then(() => {
                                location.reload();
                            });
                        },
                        error: (result) => {
                            const statusMsg = result['responseJSON']['statusMsg'];
                            Swal.fire({
                              position: 'top-end',
                              icon: 'error',
                              title: statusMsg,
                              showConfirmButton: false,
                              timer: 1500
                            }).then(() => {
                                location.reload();
                            });
                        }

                    });
                }
            });
        });
    }
});
