import{u as i,a as _}from"./theme.1b9aac4f.js";import{d as l,h as p,v as c,j as u,o as f,c as m,_ as b}from"./framework.fe1fa53f.js";const v=l({__name:"VPCarbonAds",props:{carbonAds:{}},setup(r){const{page:d}=i(),s=r.carbonAds,{isAsideEnabled:a}=_(),o=p();let n=!1;function t(){if(!n){n=!0;const e=document.createElement("script");e.id="_carbonads_js",e.src=`//cdn.carbonads.com/carbon.js?serve=${s.code}&placement=${s.placement}`,e.async=!0,o.value.appendChild(e)}}return c(()=>d.value.relativePath,()=>{var e;n&&a.value&&((e=window._carbonads)==null||e.refresh())}),s&&u(()=>{a.value?t():c(a,e=>e&&t())}),(e,h)=>(f(),m("div",{class:"VPCarbonAds",ref_key:"container",ref:o},null,512))}});const x=b(v,[["__scopeId","data-v-888f8d4e"]]);export{x as default};
