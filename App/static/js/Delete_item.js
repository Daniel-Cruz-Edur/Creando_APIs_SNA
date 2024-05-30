$(document).ready(function(){
    console.log('Document is ready.');
    
    $('.delete-item-cart').on('click', function(){
        console.log('Delete button clicked.');
        
        const ID_Song = $(this).data('id');
        console.log('Song ID to delete:', ID_Song);
        
        $.post('/Borrar_Item_Carrito', {
            ID_Song_DEL: ID_Song
        }, function(data){
            console.log('Response from server:', data);
            
            if(data.success){
                alert('Canción eliminada del carro.');
                location.reload(); // Reload the page to update the cart
            } else {
                alert('Error al eliminar la canción.');
            }
        });
    });
});