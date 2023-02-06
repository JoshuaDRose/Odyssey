var a = 1, b = 2;
var div = document.createElement('div');
div.setAttribute('class', 'post block bc2');
div.innerHTML = `
    <div class="parent">
    <div class="child">${a}</div>
    <div class="child">+</div>
    <div class="child">${b}</div>
    <div class="child">=</div>
    <div class="child">${a + b}</div>
    </div>
    `;
document.getElementById('posts').appendChild(div);
