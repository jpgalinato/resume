const button=document.getElementById('menu-button');
const nav=document.getElementById('navigation');
function closeMenu(){nav.classList.remove('open');button.setAttribute('aria-expanded','false');}
button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';nav.classList.toggle('open',open);button.setAttribute('aria-expanded',String(open));});
nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeMenu();button.focus();}});
