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
 // Stop the decorative animation when the portrait is outside the viewport.
 if('IntersectionObserver' in window){
  new IntersectionObserver(([entry])=>hero.classList.toggle('hud-out-of-view',!entry.isIntersecting)).observe(hero);
 }
}
// Quiet orientation cue for the current homepage section.
if(nav&&document.querySelector('#inicio')&&'IntersectionObserver' in window){
 const sectionLinks=[...nav.querySelectorAll('a[href^="#"]')];
 const tracked=sectionLinks.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
 const visible=new Set();
 // A single observer watches all navigation destinations, including contact.
 const observer=new IntersectionObserver(entries=>{
  entries.forEach(e=>e.isIntersecting?visible.add(e.target):visible.delete(e.target));
  const current=tracked.find(section=>visible.has(section));
  sectionLinks.forEach(a=>{if(current&&a.hash==='#'+current.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
 },{rootMargin:'-15% 0px -55% 0px'});
 tracked.forEach(section=>observer.observe(section));
}
// Native modal keeps keyboard focus inside; links remain usable without JavaScript.
const photoDialog=document.querySelector('.photo-dialog');
if(photoDialog&&typeof photoDialog.showModal==='function'){
 let photoOpener=null;
 document.querySelectorAll('.photo-open').forEach(link=>link.addEventListener('click',event=>{
  if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  event.preventDefault();photoOpener=link;
  const image=photoDialog.querySelector('img');image.src=link.href;image.alt=link.querySelector('img').alt;
  photoDialog.querySelector('.photo-caption').textContent=link.dataset.caption+(link.dataset.credit?'\n'+link.dataset.credit:'');
  photoDialog.showModal();document.body.classList.add('photo-viewing');
 }));
 photoDialog.querySelector('.photo-close').addEventListener('click',()=>photoDialog.close());
 photoDialog.addEventListener('click',event=>{if(event.target===photoDialog){const r=photoDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)photoDialog.close()}});
 photoDialog.addEventListener('close',()=>{document.body.classList.remove('photo-viewing');photoOpener?.focus()});
}
