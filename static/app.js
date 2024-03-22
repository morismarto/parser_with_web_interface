window.addEventListener('beforeunload', listenerLoad)
function listenerLoad(ev) {
    ev.returnValue = ' ';
    fetch('http://127.0.0.1:5000/shutdown');    
}

document.addEventListener('DOMContentLoaded', listenerFocus)
function listenerFocus(ev) {
    setTimeout(() => {
        fetch('http://127.0.0.1:5000/focus')
    }, 500);
} 

function insertSpinner() {
    buttonResult.insertAdjacentHTML('beforebegin', `
    <div style="margin-bottom: 30px;" class="d-flex justify-content-center" id="spinner">
        <div class="spinner-border" role="status">
            <span class="sr-only"></span>
        </div>
    </div>
    `)
}


let products

button = document.getElementById('button').addEventListener('click', buttonPostHandler)
buttonResult = document.getElementById('button-result')
function buttonPostHandler(event) {
    let input = document.getElementById('basic-url')
    if (input.value.includes('http')) {
        ul.innerHTML = ''
        event.target.style.display = 'none'
        insertSpinner()
        fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({url: input.value})
        })
        .then(response => response.json())
        .then(response => products = response)
        .then(() => buttonResult.disabled = false)
        .then(() => document.getElementById('spinner').remove())
        input.value = ''
    } else {
        alert('Некорректный url')
    }
}

main = document.getElementById('main')
ul = document.getElementById("ul")
ul.style.display = "none"

buttonResult.addEventListener('click', buttonResultHandler)
function buttonResultHandler(ev) {
    main.style.display = 'none'
    ul.style.display = 'block'
    document.getElementById('back').style.display = 'block'
    document.getElementById('wrapper').style.display = 'block'
    for (key in products) {
        ul.insertAdjacentHTML('beforeend', `<li class='list-group-item list-group-item-primary'> ${products[key]} </li>`)
    }  
    
}

wrapper = document.getElementById('wrapper')
wrapper.style.display = 'none'
back = document.getElementById('back')
back.addEventListener('click', ev => {
    ev.target.style.display = 'none'
    document.getElementById('button').style.display = 'block'
    ul.style.display = 'none'; 
    main.style.display = 'flex'
    buttonResult.disabled = true
})




