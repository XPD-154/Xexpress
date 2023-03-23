/*console.log('hello world')*/
var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length; i++){

    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if(user==='AnonymousUser'){
            console.log('Not Logged in')
        }else{
            /*console.log('User is authenticated. sending data...')*/
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log("User is already authenticated, sending data..")

    /*url to send the data of productId and action*/
    var url = '/update_item/'

    /*api to use to send data*/
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'Accept': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    /*after the fetch is complete, return data*/
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        //console.log('datajs:',data)
        location.reload()
    })
}
