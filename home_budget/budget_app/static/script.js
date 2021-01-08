const desc = document.querySelector('#description');

desc.addEventListener('keyup', function () {
    fetch(`/hint?text=${desc.value}`)
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            let ul = document.querySelector('#hints');
            ul.innerHTML = '';
            data.hints.forEach((el) => {
                let newLi = document.createElement('li');
                newLi.innerText = el;
                ul.appendChild(newLi);
                newLi.addEventListener('click', () => {
                    desc.value = el;
                    ul.innerHTML = '';
                });
            });
    });
})

























// const hints = document.querySelector('#hints');
// desc.addEventListener('keyup', function (event) {
//     fetch('/hint?text=' + event.target.value, {
//         method : 'GET'
//     }).then(response => response.json())
//     .then(data => {
//         hints.innerHTML = '';
//         data.forEach((hint) => {
//             let newLi = document.createElement('li');
//             newLi.innerText = hint
//         })
//     })
// })