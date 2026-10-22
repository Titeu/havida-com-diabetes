(function(){
  var box=document.querySelector('.proc'),pin=document.querySelector('.pin');
  if(!box||!pin||window.matchMedia('(max-width:900px)').matches||window.matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var cards=[].slice.call(box.children),off=[0,14,28,14],start=[0,0.14,0.42,0.72],dur=[0.22,0.26,0.28,0.28];
  function clamp(v){return v<0?0:v>1?1:v}
  function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2}
  function update(){
    var r=pin.getBoundingClientRect(),vh=window.innerHeight,run=r.height-vh,lead=vh*0.5;
    // 0 quando a dobra já aparece na tela (topo a 50% da altura); 1 no fim da dobra
    var p=clamp((lead-r.top)/(run+lead));
    cards.forEach(function(c,i){
      var l=ease(clamp((p-start[i])/dur[i]));
      c.style.setProperty('--a',l.toFixed(3));
      c.style.setProperty('--y',((1-l)*170+off[i]*l).toFixed(1)+'px');
    });
  }
  window.addEventListener('scroll',update,{passive:true});window.addEventListener('resize',update);
  update();
})();
