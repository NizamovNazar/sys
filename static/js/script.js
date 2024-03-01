(function($){

    if( $('#subject-data').length ){
        new DataTable('#subject-data', {
            ordering: false,
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.11.5/i18n/uk.json'
            }
        });
    }

    if( $('.js-select2').length ){
        $('.js-select2').select2();
    };

    $('.menu-button').on('click', function(e){
        e.preventDefault();

        $('body').toggleClass('menu-opened');
    });

    $(window).on('scroll', function(){
        const scrollTop = $('html, body').scrollTop();
        
        if( scrollTop  >= 100 ){
            $('body').addClass('header-fixed');
        }else{
            $('body').removeClass('header-fixed')
        }

    }).trigger('scroll');


    //  DATA UPDATING
    const $modal = $('#data-update-modal')
    $modal.on('show.bs.modal', event => {
        const $btn = $(event.relatedTarget);
        const {id, title, control, controlName} = $btn.data();

        const $title = $modal.find('#modalLabel');
        const $label = $modal.find(`label[for="${control}"]`);
        const $input = $modal.find(`input[name="${control}"]`);

        
        
        $label.text(controlName);
        $input.val(title);
        $title.text(title);

        $('.js-update-data').on('click', function(e){
            e.preventDefault();
    
            const form = $(this).closest('form');
            const action = $(form).attr('action');
            
            $.ajax({
                url: `http://127.0.0.1:9999/${action}/${id}/edit`,
                method: "POST",
                data: $(form).serialize(),
                success: function(data, textStatus, jqXHR) {
                    $('[data-bs-dismiss="modal"]').trigger('click');
                    
                    // setTimeout(function(){
                        location.reload();
                    // }, 300);
                }
              });
        });
    });

    $modal.on('hidden.bs.modal', event => {
        const $title = $modal.find('#modalLabel');
        const $label = $modal.find(`label[for="*"]`);
        const $input = $modal.find(`[name="*"]`);

        $label.text('');
        $input.val('');
        $title.text('');
    });    

})(jQuery)
