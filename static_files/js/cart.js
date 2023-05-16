/*console.log('hello world')*/

//variable button to handle adding to cart, increasing items in cart and reducing/removing items in cart by using class of the element clicked
var updateBtns = document.getElementsByClassName('update-cart')

//select an 'action' and 'product id' whenever element is clicked
for(i=0; i<updateBtns.length; i++){

    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if(user==='AnonymousUser'){
            //call function for anonymous user
            /*console.log('Not Logged in')*/
            addCookieItem(productId, action)
        }else{
            //call function for logged in user
            /*console.log('User is authenticated. sending data...')*/
            updateUserOrder(productId, action)
        }
    })
}

//function to handle adding, reducing or removing carts items for anonymous user
function addCookieItem(productId, action){
    console.log('User is not authenticated, or not Logged in')

    if(action == 'add'){
        //check if cart is empty
        if (cart[productId]==undefined){
            //add item to empty cart
            cart[productId] = {'quantity':1}
        }else{
            //add to items within the cart
            cart[productId]['quantity'] += 1
        }
    }

    if(action=='remove'){
        //reduce item within the cart
        cart[productId]['quantity'] -= 1

        //once reduction makes item 0, delete item
        if (cart[productId]['quantity'] <= 0){
            console.log('item is deleted')
            delete cart[productId];
        }
    }
    console.log('Cart:', cart);
    //return new cart and reload page
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

//function to handle adding, reducing or removing carts items for logged in user
function updateUserOrder(productId, action){

    console.log("User is already authenticated, sending data..")

    /*url (view function) to send the data of productId and action*/
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

    /*reload page*/
    .then((data) => {
        //console.log('datajs:',data)
        location.reload()
    })
}


