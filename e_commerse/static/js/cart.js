var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function(){
        var product_id = this.dataset.product;
        var action = this.dataset.action;
        var price = this.dataset.price
        console.log('productId', product_id, 'action', action)

        if ( user === 'AnonymousUser'){
            updateUserOrder(product_id, action, price);
        }
        else {
            updateUserOrder(product_id, action, price);
        }
    })

}

function updateUserOrder(product_id, action)
{
    console.log('USER:', user, 'sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'product_id': product_id, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data),
        location.reload()
    })
}

var deleteSession = document.getElementsByClassName('delete-session')

deleteSession[0].addEventListener('click', function(e){
    var url = '/delete_session/'

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-type': 'application/json'
        }
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('Data:',data)
        location.reload()
    })
})