$(document).ready(() => {


    $('#csoForm').on('submit', (e) => {
        e.preventDefault();
        $('#csoFormConfirmModal').modal('toggle');

    });

});

const csoFormSubmission = () => {
    $('#csoFormConfirmModal').modal('toggle');
    $('#loadingSpinnerModal').modal('toggle');
    const formData = $('#csoForm').serialize();
    $.ajax({
        type: 'POST',
        url: '/dashboard/cso/create',
        data: formData,
        success: (result) => {
            $('#csoForm').trigger('reset');
            setTimeout(() => {
                $('#loadingSpinnerModal').modal('toggle');
                $('#successSpinnerModal').modal('toggle');
            }, 500);

            setTimeout(() => {
                $('#successSpinnerModal').modal('toggle');
            }, 3000)



        },
        error: (result) => {
            console.log(result)
        }

    });

}

const tryss = () => {
    $('#loadingSpinnerModal').modal('toggle');
}
const successFormSubmission = () => {
    $('#successSpinnerModal').modal('toggle');
}