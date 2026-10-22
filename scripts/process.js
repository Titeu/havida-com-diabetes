(function(){
  var box=document.querySelector('.proc'),pin=document.querySelector('.pin');
  if(!box||!pin||window.matchMedia('(max-width:900px)').matches||window.matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var cards=[].slice.call(box.children),off=[0,14,28,14];
  function clamp(v){return v<0?0:v>1?1:v}
  function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2}
  function update(){
    var r=pin.getBoundingClientRect(),run=r.height-window.innerHeight;
    // progresso 0 → 1 ao longo de toda a dobra (acompanha a rolagem; termina no fim)
    var p=run>0?clamp(-r.top/run):1;
    cards.forEach(function(c,i){
      var l=ease(clamp((p-0.04-i*0.22)/0.3));
      c.style.setProperty('--a',l.toFixed(3));
      c.style.setProperty('--y',((1-l)*180+off[i]*l).toFixed(1)+'px');
    });
  }
  window.addEventListener('scroll',update,{passive:true});window.addEventListener('resize',update);
  update();
})();
