/* BLINC BLONDE — shared interactions (v2) */
(function(){
  const navwrap = document.querySelector('.navwrap');
  const hero = document.querySelector('.hero');
  function onScroll(){
    if(!navwrap) return;
    const y = window.scrollY;
    navwrap.classList.toggle('solid', y > 30);
    if(hero) navwrap.classList.toggle('on-hero', y < hero.offsetHeight - 120);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, {passive:true});

  // Mobile nav
  const toggle = document.querySelector('.nav-toggle');
  const mnav = document.querySelector('.mobile-nav');
  if(toggle && mnav){
    const close = mnav.querySelector('.mobile-close');
    const open = ()=>{mnav.classList.add('open');document.body.style.overflow='hidden';};
    const shut = ()=>{mnav.classList.remove('open');document.body.style.overflow='';};
    toggle.addEventListener('click', open);
    if(close) close.addEventListener('click', shut);
    mnav.querySelectorAll('a').forEach(a=>a.addEventListener('click', shut));
  }

  // Scroll reveal
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
  },{threshold:.1, rootMargin:'0px 0px -7% 0px'});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  // FAQ accordion
  document.querySelectorAll('.faq-q').forEach(q=>{
    q.addEventListener('click', ()=>{
      const item = q.closest('.faq-item');
      const a = item.querySelector('.faq-a');
      const isOpen = item.classList.contains('open');
      item.parentElement.querySelectorAll('.faq-item.open').forEach(o=>{
        if(o!==item){o.classList.remove('open');o.querySelector('.faq-a').style.maxHeight=null;}
      });
      if(isOpen){ item.classList.remove('open'); a.style.maxHeight=null; }
      else{ item.classList.add('open'); a.style.maxHeight = a.scrollHeight+'px'; }
    });
  });

  // Reel videos: lazy-load source + autoplay while on screen, pause when off
  const reelVids = document.querySelectorAll('.reel-vid');
  if(reelVids.length){
    const vio = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        const v = e.target;
        const src = v.querySelector('source[data-src]');
        if(e.isIntersecting){
          if(src && !src.src){ src.src = src.dataset.src; v.load(); }
          const p = v.play(); if(p && p.catch) p.catch(()=>{}); // ignore autoplay block / missing file
        } else { v.pause(); }
      });
    },{threshold:.45});
    reelVids.forEach(v=>vio.observe(v));
  }

  // Before/After slider
  document.querySelectorAll('.ba').forEach(ba=>{
    const after = ba.querySelector('.after-img');
    const handle = ba.querySelector('.ba-handle');
    const range = ba.querySelector('.ba-range');
    if(!range) return;
    const set = v=>{ after.style.clipPath = `inset(0 0 0 ${v}%)`; handle.style.left = v+'%'; };
    range.addEventListener('input', e=>set(e.target.value));
    set(50);
  });
})();
