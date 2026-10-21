(function(root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.JatimMap = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  'use strict';
  const fmt = (n, d=0) => Number.isFinite(n)
    ? n.toLocaleString('id-ID', {minimumFractionDigits:d, maximumFractionDigits:d}) : '—';
  const safeJSON = value => JSON.stringify(value).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026');
  const value = (row, kind, level) => level === 'semua'
    ? ['sd','smp','sma'].reduce((sum,j) => sum + row[kind+'_'+j], 0)
    : row[kind+'_'+level];
  function payload(rows, all, points, options) {
    const {level='semua', indicator='sekolah', colorIpm=false, basemap=false} = options;
    const judul = 'Jumlah '+indicator+(level==='semua'?'':' '+level.toUpperCase());
    const ordered = all.map(r => value(r,indicator,level)).filter(Number.isFinite).sort((a,b)=>a-b);
    const ipm = Object.fromEntries(all.filter(r=>Number.isFinite(r.ipm)).map(r=>[r.kabupaten_kota,r.ipm]));
    const ipms = Object.values(ipm);
    const data = rows.filter(r=>points[r.kabupaten_kota]).map(r=>{
      const guru=value(r,'guru',level), murid=value(r,'murid',level);
      return {nama:r.kabupaten_kota,lat:points[r.kabupaten_kota][0],lon:points[r.kabupaten_kota][1],
        nilai:value(r,indicator,level),rincian:[
          [judul,fmt(value(r,indicator,level))],
          ['Jenjang',level==='semua'?'SD, SMP, SMA':level.toUpperCase()],
          ['IPM',fmt(r.ipm,2)],['Lama sekolah',fmt(r.rata_lama_sekolah,2)+' tahun'],
          ['Sekolah',fmt(value(r,'sekolah',level))],['Guru',fmt(guru)],['Murid',fmt(murid)],
          ['Murid per guru',guru?fmt(murid/guru,2):'—']
        ]};
    });
    return {data,cfg:{judul,t1:ordered[Math.floor(ordered.length/3)]??0,
      t2:ordered[Math.floor(2*ordered.length/3)]??0,warnaIpm:colorIpm&&ipms.length>0,petaDasar:basemap,
      ipm,ipmMin:ipms.length?Math.min(...ipms):0,ipmMax:ipms.length?Math.max(...ipms):1,
      atribusi:'Batas wilayah: BPS, WFP, OCHA ROAP via geoBoundaries (CC BY 3.0 IGO)'}};
  }
  function html(template, data) {
    return template.replace(/__(DATA|CFG)__/g, (_,name)=>safeJSON(name==='DATA'?data.data:data.cfg));
  }
  let previous = '';
  function render(rows, all, level) {
    const $=id=>document.getElementById(id);
    const options={level,indicator:$('map-indicator').value,colorIpm:$('map-ipm').checked,basemap:$('map-basemap').checked};
    const signature=JSON.stringify([rows,options]);
    if(signature===previous)return;
    previous=signature;
    const points=JSON.parse($('map-points').textContent);
    const p=payload(rows,all,points,options);
    $('map-frame').srcdoc=html(JSON.parse($('map-template').textContent),p);
    const missing=rows.length-p.data.length;
    $('map-summary').textContent=p.data.length+' wilayah · '+p.cfg.judul+' · total '+fmt(p.data.reduce((s,r)=>s+r.nilai,0))+
      (missing?' · '+missing+' wilayah belum memiliki batas peta':'');
  }
  return {payload,html,render};
});
