# -*- coding: utf-8 -*-
import io, re, sys

SRC = "/sessions/epic-vibrant-newton/mnt/uploads/Best Hair Salon North Shore _ Premium Haircuts & Styling.html"
OUT = "/sessions/epic-vibrant-newton/mnt/outputs/blinc-blonde.html"

html = io.open(SRC, encoding="utf-8", errors="ignore").read()

PREFIX = "./Best Hair Salon North Shore _ Premium Haircuts &amp; Styling_files/"

# 1) Re-link local assets to live absolute URLs so layout + animations work
asset_map = {
    "showit.css": "https://lib.showit.co/engine/2.8.0/showit.css",
    "pub.css": "https://sloans.com.au/wp-content/themes/showit/pubs/n7f9tbloei4at67favelyw/20260522034444Sxbppav/assets/pub.css?ver=1781106696",
    "all.min.css": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    "animate.min.css": "https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.4.0/animate.min.css",
    "css": "https://fonts.googleapis.com/css?family=Didact+Gothic:regular|Abril+Fatface:regular",
    "jquery.tosrus.min.css": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/assets/tosrus/jquery.tosrus.min.css?ver=2.5.0",
    "jquery.min.js": "https://sloans.com.au/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "jquery-migrate.min.js": "https://sloans.com.au/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "purify.min.js": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/assets/dompurify/purify.min.js?ver=3.3.1",
    "sanitizer.js": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/js/sanitizer.js?ver=2.7.6",
    "jquery.tosrus.min.js": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/assets/tosrus/jquery.tosrus.min.js?ver=2.5.0",
    "underscore.min.js": "https://sloans.com.au/wp-includes/js/underscore.min.js?ver=1.13.7",
    "infinite-scroll.pkgd.min.js": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/assets/infinitescroll/infinite-scroll.pkgd.min.js?ver=4.0.1",
    "front.js": "https://sloans.com.au/wp-content/plugins/responsive-lightbox/js/front.js?ver=2.7.6",
    "pub.js": "https://sloans.com.au/wp-content/themes/showit/pubs/n7f9tbloei4at67favelyw/20260522034444Sxbppav/assets/pub.js?ver=1781106696",
    "showit-lib.min.js": "https://lib.showit.co/engine/2.8.0/showit-lib.min.js",
    "showit.min.js": "https://lib.showit.co/engine/2.8.0/showit.min.js",
    # local fallback images -> showit absolute (runtime JS later swaps to Blinc)
    "sloans_best_hairdressers_in_sydney.jpg": "https://static.showit.co/1600/L28-Gwfzl_96geP_hnFYPw/shared/sloans_best_hairdressers_in_sydney.jpg",
    "sloans_lux_hair_salon.jpg": "https://static.showit.co/1600/dYDSGLbN6lHMxeyDiVa5GQ/shared/sloans_lux_hair_salon.jpg",
    "sloans_sydney_hairdresser.jpg": "https://static.showit.co/1600/cYlglZ9hdLVA92_C2xsewg/shared/sloans_sydney_hairdresser.jpg",
    "sloans_lane_cove_hairdresser_sydney.jpg": "https://static.showit.co/1600/cYlglZ9hdLVA92_C2xsewg/shared/sloans_sydney_hairdresser.jpg",
}
for fname, url in asset_map.items():
    html = html.replace(PREFIX + fname, url)

# 2) Remove Sloans tracking script tags + disable GA/GTM ids
for tag in [
    '<script async="" src="https://www.googletagmanager.com/gtm.js?id=GTM-TVB43KQC"></script>',
    '<script async="" src="' + PREFIX + 'gtm.js"></script>',
    '<script async="" src="' + PREFIX + 'js"></script>',
    '<script src="' + PREFIX + 'wp-emoji-release.min.js" defer=""></script>',
]:
    html = html.replace(tag, "")
html = html.replace("GTM-TVB43KQC", "").replace("G-13YCEK0HGP", "")

# 3) Title / meta / favicon -> Blinc
html = html.replace("Best Hair Salon North Shore | Premium Haircuts &amp; Styling",
                    "Blinc Blonde | Hair &amp; Beauty Salon, Highgate Perth")
html = html.replace(
    "Experience on trend professional hair styling at North Shore&#39;s luxury hair salon. We craft impeccable cuts &amp; colours tailored to you. Book your experience now.",
    "Blinc Blonde is a boutique hair &amp; beauty salon in Highgate / Mount Lawley, Perth. Aveda salon specialising in cuts, balayage, colour, straightening and styling.")
html = html.replace('content="Sloans"', 'content="Blinc Blonde"')
html = html.replace('content="https://sloans.com.au/"', 'content="https://blincblonde.com/"')
html = html.replace("https://sloans.com.au/wp-content/uploads/2025/04/Home.jpg",
                    "https://blincblonde.com/wp-content/uploads/2023/03/hashtage_blinc.jpg")
html = html.replace("https://static.showit.co/200/MmrrKL0fjPY14t29KhgV_g/300807/sloans-sloans-s-arch-green-rgb-900px-w-72ppi.png",
                    "https://blincblonde.com/wp-content/uploads/2023/03/Blinc_mobile.png")

# 4) Inject the Blinc rebrand runtime overrides before </body>
REBRAND = r'''
<style id="blinc-overrides">
@media (min-width:1px){
  .blinc-logo-img{display:block;width:100%;height:100%;object-fit:contain;object-position:left center;}
}
</style>
<script id="blinc-rebrand">
(function(){
  var LOGO = "https://blincblonde.com/wp-content/uploads/2023/03/BB_Logo_tran-01.png";
  // ---- image map (Sloans/showit stem -> Blinc image) ----
  var IMG = [
    ["sloans_luxury_hair_salon_north_shore","https://blincblonde.com/wp-content/uploads/2018/04/h2-slider1-background-img.jpg"],
    ["sloans_sydney_hairdresser","https://blincblonde.com/wp-content/uploads/2022/12/1BBSALONCANDIDS-1024x683-1.jpg"],
    ["sloans_best_hairdressers_in_sydney","https://blincblonde.com/wp-content/uploads/2022/12/48BBSALONCANDIDS-1024x683-2.jpg"],
    ["sloans_lux_hair_salon","https://blincblonde.com/wp-content/uploads/2022/12/About-Us.jpg"],
    ["sloans_lane_cove_hairdresser_sydney","https://blincblonde.com/wp-content/uploads/2018/04/port-gallery-img-3.jpg"],
    ["sloans_sydney_salon","https://blincblonde.com/wp-content/uploads/2022/12/1BBSALONCANDIDS-1024x683-1.jpg"],
    ["sloans_salon_owner_and_director_scott","https://blincblonde.com/wp-content/uploads/2023/03/hashtage_blinc.jpg"],
    ["sloans_hair_salon_for_women","https://blincblonde.com/wp-content/uploads/2022/12/48BBSALONCANDIDS-1024x683-2.jpg"],
    ["sloans_formal_hair_and_makeup_services_sydney","https://blincblonde.com/wp-content/uploads/2018/04/port-gallery-img-3.jpg"],
    ["sloans_bridal_hair_and_makeup_services_sydney","https://blincblonde.com/wp-content/uploads/2022/12/About-Us.jpg"],
    ["sloans_hair_salon_for_ladies","https://blincblonde.com/wp-content/uploads/2022/12/Screen-Shot-2019-03-30-at-4.57.09-pm-1024x545-1.png"]
  ];
  var DEFAULTS = [
    "https://blincblonde.com/wp-content/uploads/2022/12/1BBSALONCANDIDS-1024x683-1.jpg",
    "https://blincblonde.com/wp-content/uploads/2022/12/48BBSALONCANDIDS-1024x683-2.jpg",
    "https://blincblonde.com/wp-content/uploads/2018/04/port-gallery-img-3.jpg"
  ];
  var dCount=0;
  function mapUrl(u){
    if(!u) return null;
    if(u.indexOf("blincblonde.com")>-1) return null;
    for(var i=0;i<IMG.length;i++){ if(u.indexOf(IMG[i][0])>-1) return IMG[i][1]; }
    if(u.indexOf("static.showit.co")>-1 || u.indexOf("sloans_")>-1 || u.indexOf("/Home.jpg")>-1){
      return DEFAULTS[(dCount++)%DEFAULTS.length];
    }
    return null;
  }
  function swapImages(root){
    (root||document).querySelectorAll("img").forEach(function(im){
      ["data-src","src"].forEach(function(a){
        var v=im.getAttribute(a); var n=mapUrl(v);
        if(n){ im.setAttribute(a,n); if(a==="src"){im.src=n;} }
      });
      im.classList && im.classList.remove("slzy");
    });
    (root||document).querySelectorAll("[style*='background-image']").forEach(function(el){
      var bg=el.style.backgroundImage||""; var m=bg.match(/url\(["']?([^"')]+)/);
      if(m){ var n=mapUrl(m[1]); if(n){ el.style.backgroundImage='url("'+n+'")'; } }
    });
  }
  // ---- colour remap (Sloans sage green -> Blinc warm neutral) ----
  var DARK="#2a2622", SOFT="#efe6d8";
  function isGreen(c){ return c==="rgb(45, 74, 60)"||c==="rgb(40, 72, 52)"; }
  function remapColours(){
    var els=document.querySelectorAll("#si-sp *");
    for(var i=0;i<els.length;i++){
      var el=els[i], cs=getComputedStyle(el);
      if(isGreen(cs.color)) el.style.color=DARK;
      if(isGreen(cs.borderTopColor)){ el.style.borderColor=DARK; }
      var bg=cs.backgroundColor;
      if(isGreen(bg)) el.style.backgroundColor=DARK;
      else if(bg==="rgb(203, 220, 210)") el.style.backgroundColor=SOFT;
      else if(bg==="rgba(40, 72, 52, 0.8)") el.style.backgroundColor="rgba(42,38,34,0.82)";
    }
  }
  // ---- logo swap (Sloans wordmark SVG -> Blinc logo) ----
  function swapLogos(){
    document.querySelectorAll('svg[viewBox="0 0 117.8 37.7"]').forEach(function(svg){
      if(svg.dataset.blinc) return; svg.dataset.blinc=1;
      if(svg.closest("#industry-awards")){ var h=svg.closest(".se-icon")||svg; h.style.display="none"; return; }
      var wrap=document.createElement("span");
      wrap.style.cssText="display:flex;align-items:center;justify-content:center;width:100%;height:100%;background:#f4ede1;border-radius:10px;box-sizing:border-box;padding:8% 10%;";
      var img=document.createElement("img"); img.src=LOGO; img.alt="Blinc Blonde";
      img.style.cssText="display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;";
      wrap.appendChild(img); svg.parentNode.replaceChild(wrap,svg);
    });
  }
  // ---- text content (by Showit element id) ----
  var T = {
    "nav-home_6":"BLINC BLONDE &nbsp;&middot;&nbsp; HIGHGATE",
    "new-client-offer_1":"Let Us Take Care Of You",
    "new-client-offer_2":"Step into our boutique salon in the heart of Highgate, where Perth’s most passionate hairdressers craft cuts, colour and balayage tailored entirely to you.<br><br>As an Aveda salon, every service blends naturally derived products with pure artistry — so you leave knowing your hair was treated with real care. We can’t wait to welcome you to the Blinc Blonde chair.",
    "best-hair-salon_1":"boutique salon",
    "best-hair-salon_4":"Perth’s home of<br>beautiful blonde,<br>balayage &amp;<br>natural colour.",
    "best-hair-salon_2":"Tucked into Beaufort Street in Highgate, Blinc Blonde is a boutique hair and beauty salon where every client is treated with pure passion. Our hairdressers are experts across classic cuts, professional straightening, curls, balayage and all-over colour. As an Aveda salon, we use naturally derived products that leave hair healthy, shiny and beautifully you.",
    "services_1":"Blinc Blonde hair &amp; beauty services",
    "services_3":"Cut",
    "services_4":"From a precision classic cut to a fresh restyle, your Blinc Blonde stylist tailors every line to suit your face, hair type and lifestyle — for women and men alike.",
    "services_7":"Colour",
    "services_8":"Balayage, all-over colour, foils and expert colour correction. Our colourists are blonde specialists who protect the integrity of your hair with every application.",
    "services_11":"Styling",
    "services_12":"Professional straightening, curls, blow-dries and event styling. Whether it’s an everyday finish or a special-occasion look, we style your hair to perfection.",
    "services_15":"Treatments",
    "services_16":"As an Aveda salon, we offer nourishing in-salon treatments and rituals that restore strength, condition and natural shine using plant-powered formulas.",
    "best-hairdressers-sydney_0":"Perth’s Best Hairdressers",
    "best-hairdressers-sydney_1":"Loved by locals across Highgate and Mount Lawley, Blinc Blonde brings together technical expertise and genuine care. Come and experience Perth’s best hairdressers and leave knowing your hair was treated with pure passion.",
    "best-hairdressers-sydney_6":"An Aveda Salon",
    "best-hairdressers-sydney_7":"Aveda believes nature is the best beauty artist of all. We use naturally derived ingredients — plants and flowers — to deliver powerful results, beautiful colour and healthier hair, while caring for body, mind and the planet.",
    "client-love_client-1_0":"SOPHIE",
    "client-love_client-1_1":"“The best blonde I’ve ever had. The team genuinely listens, and the salon feels so welcoming from the moment you walk in.”",
    "client-love_client-2_0":"MAYA",
    "client-love_client-2_1":"“I’ve never trusted anyone with my colour like I trust Blinc. My balayage grows out beautifully every single time.”",
    "client-love_client-3_0":"ELIZA",
    "client-love_client-3_1":"“Five-star from start to finish. Lovely people, a gorgeous space, and my hair has never been healthier.”",
    "bridal-hair-and-make-up_2":"Weddings &amp;<br>Special Occasions",
    "bridal-hair-and-make-up_3":"We love a little romance and glamour. Being trusted with your wedding or special-occasion hair is an honour — from trial to the aisle, we plan every detail together so the day feels effortless.",
    "latest-in-the-trend-less-and-timeless_1":"Latest from the Blinc journal",
    "latest-in-the-trend-less-and-timeless_view-1_0":"7 reasons you need a silk pillowcase",
    "latest-in-the-trend-less-and-timeless_view-1_1":"read more",
    "latest-in-the-trend-less-and-timeless_view-2_0":"7 hair colour trends to book in this season",
    "latest-in-the-trend-less-and-timeless_view-2_1":"read more",
    "latest-in-the-trend-less-and-timeless_view-3_0":"Colour maintenance — what you need to know",
    "latest-in-the-trend-less-and-timeless_view-3_1":"read more",
    "footer_3":"(08) 6222 6677",
    "footer_5":"BLINCBLONDE.COM",
    "footer_6":"479 BEAUFORT STREET HIGHGATE WA 6003",
    "footer_13":"WEDDINGS",
    "footer_21":"TERMS",
    "credit_1":"© Copyright Blinc Blonde 2026 · All Rights Reserved",
    "pop-out-nav_view-1_3":"WEDDINGS",
    "pop-out-nav_view-1_5":"CAREER"
  };
  function setText(){
    for(var sid in T){
      var host=document.querySelector('[data-sid="'+sid+'"]');
      var t = host ? host.querySelector(".se-t") : document.querySelector(".sie-"+sid+"-text");
      if(t){ t.innerHTML=T[sid]; }
    }
    // credit "curated by" line
    var c2=document.querySelector('[data-sid="credit_2"]');
    if(c2){ c2.innerHTML='<div class="si-embed" style="font-family:\'Didact Gothic\';font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#fff;opacity:.7">Hairdresser located in Highgate, Perth</div>'; }
  }
  function setButton(sid,label){
    var host=document.querySelector('[data-sid="'+sid+'"]'); if(!host) return;
    var spans=host.querySelectorAll("[class*='button-text']");
    if(spans.length){ spans.forEach(function(s){ var ic=s.querySelector("i"); s.innerHTML=(ic?ic.outerHTML+" ":"")+label; }); return; }
    var p=host.querySelector("p"); if(p){ var ic=p.querySelector("i"); p.innerHTML=(ic?ic.outerHTML+" ":"")+label; }
  }
  function setEmbeds(){
    var tl=document.querySelector('[data-sid="trend-led_0"]');
    if(tl){ tl.querySelectorAll("h1,h2,h3").forEach(function(h){ h.innerHTML="Hair &amp; beauty,<br>treated with pure passion."; }); }
    var ia=document.querySelector('[data-sid="industry-awards_0"]');
    if(ia){
      var B=[["AVEDA","Salon","Naturally derived products"],["BALAYAGE","& Blonde","Colour specialists"],["BOUTIQUE","Hair & Beauty","Highgate, Perth"],["OPEN","6 Days","Monday – Saturday"],["BOOK","Online","blincblonde.com"]];
      var tops=ia.querySelectorAll(".top-text"), mids=ia.querySelectorAll(".middle-text"), bots=ia.querySelectorAll(".bottom-text");
      tops.forEach(function(e,i){ e.innerHTML=B[i%B.length][0]; });
      mids.forEach(function(e,i){ e.innerHTML=B[i%B.length][1]; });
      bots.forEach(function(e,i){ e.innerHTML=B[i%B.length][2]; });
    }
  }
  function relabel(){ setButton("best-hairdressers-sydney_2","Meet The Team"); setButton("best-hairdressers-sydney_8","Discover Aveda"); setButton("bridal-hair-and-make-up_4","Enquire About Weddings"); }
  // ---- links ----
  var BOOK="https://home.shortcutssoftware.com/blincblonde";
  var NAV={HOME:"https://blincblonde.com/",ABOUT:"https://blincblonde.com/about-us/",SERVICES:"https://blincblonde.com/hair-services/",CUT:"https://blincblonde.com/hair-services/",COLOUR:"https://blincblonde.com/hair-services/",STYLING:"https://blincblonde.com/hair-services/",TREATMENTS:"https://blincblonde.com/hair-services/",NEWS:"https://blincblonde.com/blog/",CONTACT:"https://blincblonde.com/contact-us/",GALLERY:"https://blincblonde.com/weddings/",WEDDINGS:"https://blincblonde.com/weddings/",CAREER:"https://blincblonde.com/career/",CAREERS:"https://blincblonde.com/career/",TERMS:"https://blincblonde.com/terms-conditions/","SALON ETIQUETTE":"https://blincblonde.com/terms-conditions/","VIEW ALL SERVICES":"https://blincblonde.com/hair-services/"};
  function fixLinks(){
    document.querySelectorAll("a").forEach(function(a){
      var href=a.getAttribute("href")||"";
      var txt=(a.innerText||"").trim().toUpperCase();
      var html=a.innerHTML||"";
      if(href.indexOf("instagram")>-1 || /fa-instagram/.test(html)){ a.href="https://www.instagram.com/blincblonde/"; a.target="_blank"; return; }
      if(href.indexOf("facebook")>-1 || /fa-facebook/.test(html)){ a.href="https://www.facebook.com/blincblonde"; a.target="_blank"; return; }
      if(/fa-pinterest|fa-tiktok|fa-x-twitter|fa-twitter/.test(html)){ a.href="https://www.instagram.com/blincblonde/"; a.target="_blank"; return; }
      if(href.indexOf("tel:")===0){ a.href="tel:+61862226677"; return; }
      if(/BOOK/.test(txt)){ a.href=BOOK; a.target="_blank"; return; }
      if(NAV[txt]){ a.href=NAV[txt]; return; }
      if(href.indexOf("sloans.com.au")>-1){ a.href="https://blincblonde.com/"; }
    });
  }
  function applyLight(){ setText(); relabel(); setEmbeds(); swapLogos(); fixLinks(); swapImages(); }
  function applyOnce(){ applyLight(); remapColours(); }
  function boot(){
    applyLight();
    var n=0, iv=setInterval(function(){ applyLight(); n++; if(n>=24){clearInterval(iv);} },600);
    [200,800,2000,4000,7000].forEach(function(t){ setTimeout(remapColours,t); });
    window.addEventListener("scroll", function(){ applyLight(); }, {passive:true});
    var deb; new MutationObserver(function(){ clearTimeout(deb); deb=setTimeout(swapImages,100); }).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["style","src","data-src","class"]});
  }
  if(document.readyState!=="loading") boot(); else document.addEventListener("DOMContentLoaded",boot);
  window.addEventListener("load", applyOnce);
})();
</script>
'''

html = html.replace("</body>", REBRAND + "\n</body>")

io.open(OUT, "w", encoding="utf-8").write(html)
print("written", OUT, len(html), "bytes")
