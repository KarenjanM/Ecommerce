hideButton = document.getElementsByClassName('close')

hideButton[0].addEventListener('click', function (e) {
    console.log('hiding message...')
    document.getElementById('message').classList.add('hidden')
})