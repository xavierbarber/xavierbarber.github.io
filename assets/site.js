const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
if(toggle&&nav){
 const close=()=>{toggle.setAttribute('aria-expanded','false');nav.classList.remove('open')};
 toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
 nav.addEventListener('click',e=>{if(e.target.closest('a'))close()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){close();toggle.focus()}});
}
const filters=[...document.querySelectorAll('[data-filter]')];
const papers=[...document.querySelectorAll('[data-category]')];
filters.forEach(button=>button.addEventListener('click',()=>{
 const selected=button.dataset.filter;
 filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 let count=0;papers.forEach(p=>{p.hidden=selected!=='0'&&p.dataset.category!==selected;if(!p.hidden)count++});
 const status=document.querySelector('.filter-count');if(status)status.textContent=count+' '+status.dataset.countLabel;
}));
// Keep the corresponding section when changing language, without forcing a language on first visit.
document.querySelectorAll('.languages a').forEach(a=>a.addEventListener('click',()=>{if(location.hash)a.href=a.href.split('#')[0]+location.hash}));
// Progressive enhancement: an unchanged portrait when JS is absent or motion is reduced.
const hero=document.querySelector('.hero[data-hud]');
const hudToggle=document.querySelector('.hud-toggle');
if(hero&&hudToggle){
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 const setHud=state=>{
  hero.dataset.hud=state;
  hudToggle.querySelector('.hud-toggle-label').textContent=state==='running'?hudToggle.dataset.pause:state==='paused'?hudToggle.dataset.resume:hudToggle.dataset.enable;
  hudToggle.querySelector('.hud-toggle-icon').textContent=state==='running'?'Ⅱ':'▷';
 };
 hudToggle.hidden=false;setHud(reduced.matches?'off':'running');
 hudToggle.addEventListener('click',()=>setHud(hero.dataset.hud==='running'?'paused':'running'));
 reduced.addEventListener('change',e=>{if(e.matches)setHud('off')});
}
