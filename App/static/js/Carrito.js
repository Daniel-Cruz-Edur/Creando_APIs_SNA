$(document).ready(function(){

    $('.add-to-cart').on('click', function(){
        const ID_Song = $(this).data('id');
        const Titulo_Song_JS = $(this).data('title');
        const Precio_Song_JS = $(this).data('price');

        $.post('/Agregar_Al_Carrito', {
            ID_Song_LA: ID_Song,
            Titulo_Song_LA: Titulo_Song_JS,
            Precio_Song_LA: Precio_Song_JS

        }, function(data)
        {    
            alert(data.message || 'Cancion agregada al carro.');

        });

    });

});


