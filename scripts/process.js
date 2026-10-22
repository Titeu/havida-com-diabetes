(function(){
  var box=document.querySelector('.proc');
  if(!box||window.matchMedia('(max-width:900px)').matches||window.matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var cards=[].slice.call(box.children),off=[0,14,28,14],ticking=false;
  function clamp(v){return v<0?0:v>1?1:v}
  function ease(t){return 1-Math.pow(1-t,3)}
  function update(){
    ticking=false;
    var vh=window.innerHeight,top=box.getBoundingClientRect().top;
    // 0 quando a fileira aparece na base da tela; 1 quando já subiu para o alto
    var p=clamp((vh*0.92-top)/(vh*0.92-vh*0.16));
    cards.forEach(function(c,i){
      var l=ease(clamp((p-i*0.2)/0.4));
      c.style.setProperty('--a',l.toFixed(3));
      c.style.setProperty('--y',((1-l)*150+off[i]*l).toFixed(1)+'px');
    });
  }
  function req(){update()}
  window.addEventListener('scroll',req,{passive:true});window.addEventListener('resize',req);
  update();
})();
