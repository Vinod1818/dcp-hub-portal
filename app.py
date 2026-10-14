import streamlit as st
import base64
import hmac

st.set_page_config(
    page_title="DCP Request Hub — DCP SRE",
    page_icon="🔴",
    layout="wide"
)

# ===== ACCESS CONTROL =====
def check_password():
    def login_form():
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }
        /* Nuclear option — hide ALL Streamlit branding everywhere */
        #MainMenu, footer, header,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stHeader"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarNav"],
        .st-emotion-cache-zq5wmm,
        .st-emotion-cache-1dp5vir,
        .st-emotion-cache-14xtw13,
        .st-emotion-cache-1avcm0n,
        .viewerBadge_container__r5tak,
        .viewerBadge_link__qRIco,
        #GithubIcon,
        a[href="https://streamlit.io"],
        a[href*="github.com/streamlit"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            height: 0 !important;
            overflow: hidden !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("""
            <div style='text-align:center; margin-bottom:32px;'>
                <div style='display:inline-flex; align-items:center; gap:4px; margin-bottom:16px;'>
                    <div style='width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#FF0000,#cc0000);'></div>
                    <div style='width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#FF5F00,#cc4c00);margin-left:-18px;'></div>
                </div>
                <div style='color:#fff;font-size:22px;font-weight:900;letter-spacing:-.5px;'>DCP Request Hub</div>
                <div style='color:rgba(255,255,255,.4);font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-top:6px;'>DCP SRE &middot; Restricted Access</div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("login"):
                st.text_input("Password", type="password", key="password", placeholder="Enter access password")
                submitted = st.form_submit_button("Access Portal", use_container_width=True)
                if submitted:
                    if hmac.compare_digest(st.session_state.password, st.secrets["APP_PASSWORD"]):
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Incorrect password. Contact DCP SRE team for access.")

    if st.session_state.get("authenticated"):
        return True
    login_form()
    return False

if not check_password():
    st.stop()

# Hide ALL Streamlit chrome + branding
st.markdown("""
<style>
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"],
    [data-testid="collapsedControl"],
    .st-emotion-cache-zq5wmm,
    .st-emotion-cache-1dp5vir,
    .st-emotion-cache-14xtw13,
    .st-emotion-cache-1avcm0n,
    .viewerBadge_container__r5tak,
    .viewerBadge_link__qRIco,
    #GithubIcon,
    a[href="https://streamlit.io"],
    a[href*="github.com/streamlit"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    .block-container {padding: 0 !important; max-width: 100% !important;}
    [data-testid="stAppViewContainer"] {padding: 0;}
</style>
""", unsafe_allow_html=True)

# ===== LOADER with Particle Background =====
LOADER = """
<div id="mc-loader" style="
    position:fixed;inset:0;z-index:99999;
    background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    font-family:'Inter','Segoe UI',sans-serif;
    transition:opacity 0.6s ease,visibility 0.6s ease;
    overflow:hidden;
">
    <!-- Particle canvas -->
    <canvas id="mc-particles" style="position:absolute;inset:0;pointer-events:none;"></canvas>

    <!-- Content -->
    <div style="position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;">
        <div style="display:flex;align-items:center;gap:4px;margin-bottom:32px;">
            <div style="width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#FF0000,#cc0000);box-shadow:0 4px 20px rgba(235,0,27,.4)"></div>
            <div style="width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,#FF5F00,#cc4c00);margin-left:-22px;box-shadow:0 4px 20px rgba(255,95,0,.3)"></div>
        </div>
        <div style="color:#fff;font-size:26px;font-weight:900;letter-spacing:-.5px;margin-bottom:6px;">DCP Request Hub</div>
        <div style="color:rgba(255,255,255,.4);font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:48px;">DCP SRE &middot; Your One-Stop Request Portal</div>
        <div style="width:280px;height:5px;background:rgba(255,255,255,.1);border-radius:5px;overflow:hidden;margin-bottom:20px;">
            <div id="mc-bar" style="height:100%;width:0%;border-radius:5px;background:linear-gradient(90deg,#EB001B,#FF5F00,#F79E1B);transition:width 0.4s ease;box-shadow:0 0 12px rgba(255,95,0,.6);"></div>
        </div>
        <div id="mc-status" style="color:rgba(255,255,255,.45);font-size:12px;font-weight:600;letter-spacing:.5px;">Initialising...</div>
    </div>
</div>
<script>
(function(){
    /* ---- Particle background ---- */
    var canvas=document.getElementById('mc-particles');
    canvas.width=window.innerWidth; canvas.height=window.innerHeight;
    var ctx=canvas.getContext('2d');
    var dots=[];
    for(var i=0;i<80;i++){
        dots.push({
            x:Math.random()*canvas.width, y:Math.random()*canvas.height,
            r:Math.random()*2+.5,
            vx:(Math.random()-.5)*.6, vy:(Math.random()-.5)*.6,
            a:Math.random()*.5+.15
        });
    }
    var pRunning=true;
    function drawParticles(){
        if(!pRunning) return;
        ctx.clearRect(0,0,canvas.width,canvas.height);
        dots.forEach(function(d){
            ctx.beginPath();
            ctx.arc(d.x,d.y,d.r,0,Math.PI*2);
            ctx.fillStyle='rgba(255,255,255,'+d.a+')';
            ctx.fill();
            d.x+=d.vx; d.y+=d.vy;
            if(d.x<0||d.x>canvas.width) d.vx*=-1;
            if(d.y<0||d.y>canvas.height) d.vy*=-1;
        });
        /* draw connecting lines */
        for(var i=0;i<dots.length;i++){
            for(var j=i+1;j<dots.length;j++){
                var dx=dots[i].x-dots[j].x, dy=dots[i].y-dots[j].y;
                var dist=Math.sqrt(dx*dx+dy*dy);
                if(dist<100){
                    ctx.beginPath();
                    ctx.strokeStyle='rgba(255,255,255,'+(0.08*(1-dist/100))+')';
                    ctx.lineWidth=.6;
                    ctx.moveTo(dots[i].x,dots[i].y);
                    ctx.lineTo(dots[j].x,dots[j].y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(drawParticles);
    }
    drawParticles();

    /* ---- Progress bar ---- */
    var bar=document.getElementById('mc-bar');
    var status=document.getElementById('mc-status');
    var loader=document.getElementById('mc-loader');
    var steps=[
        {w:20,t:'Loading assets...'},
        {w:40,t:'Building components...'},
        {w:65,t:'Preparing CRQ engine...'},
        {w:85,t:'Almost ready...'},
        {w:100,t:'Welcome!'}
    ];
    var i=0;
    function next(){
        if(i>=steps.length)return;
        bar.style.width=steps[i].w+'%';
        status.textContent=steps[i].t;
        i++;
        if(i<steps.length){ setTimeout(next,420); }
        else{
            setTimeout(function(){
                loader.style.opacity='0';
                loader.style.visibility='hidden';
                pRunning=false;
            },600);
        }
    }
    setTimeout(next,200);
})();
</script>
"""

# ===== ALL ENHANCEMENTS =====
EXTRA = """
<style>
/* ===== 3. TAB SLIDE ===== */
.page.active { animation: pageSlideIn 0.38s cubic-bezier(0.4,0,0.2,1); }
.page.slide-left { animation: pageSlideInLeft 0.38s cubic-bezier(0.4,0,0.2,1) !important; }
@keyframes pageSlideIn {
    from { opacity:0; transform:translateX(36px); }
    to   { opacity:1; transform:translateX(0); }
}
@keyframes pageSlideInLeft {
    from { opacity:0; transform:translateX(-36px); }
    to   { opacity:1; transform:translateX(0); }
}

/* ===== 5. STEP CHECKMARK ANIMATION ===== */
@keyframes checkDraw {
    from { stroke-dashoffset: 40; opacity:0; }
    to   { stroke-dashoffset: 0;  opacity:1; }
}
.step-check-svg { display:inline-block; vertical-align:middle; margin-right:6px; }
.step-check-svg path {
    stroke-dasharray: 40;
    stroke-dashoffset: 40;
    animation: checkDraw 0.5s cubic-bezier(0.4,0,0.2,1) forwards;
}

/* ===== 7. DARK MODE ===== */
body.dark-mode {
    --bg:#0f172a !important; --card:#1e293b !important; --ink:#f1f5f9 !important;
    --soft:#94a3b8 !important; --muted:#64748b !important;
    --border:#334155 !important; --border-l:#1e293b !important;
}
body.dark-mode .step-card { background:var(--card); border-color:#334155; }
body.dark-mode .step-head:hover { background:#263347; }
body.dark-mode .opt-btn { background:#1e293b; color:#f1f5f9; border-color:#334155; }
body.dark-mode .ev-row { background:#1e293b; border-color:#334155; }
body.dark-mode .ev-input { background:#0f172a; color:#f1f5f9; border-color:#334155; }
body.dark-mode .evidence-section { background:#1e293b; border-color:#334155; }
body.dark-mode .summary-panel { background:#1e293b; }
body.dark-mode .wf-card { background:#1e293b; border-color:#334155; }
body.dark-mode .wf-row { background:#263347; }
body.dark-mode .progress-strip { background:#1e293b; border-color:#334155; }
body.dark-mode .footer { background:#1e293b; border-color:#334155; }
body.dark-mode .team-dept { background:#1e293b; }
body.dark-mode .oc-root,.dark-mode .oc-person { background:#263347; border-color:#334155; }
body.dark-mode .wf-legend { background:#1e293b; border-color:#334155; }
body.dark-mode .chk-item { background:#1e293b; border-color:#334155; color:#f1f5f9; }
body.dark-mode .sub-q { background:linear-gradient(135deg,#1e293b,#263347); }
body.dark-mode .sub-q select, body.dark-mode .sub-q input { background:#0f172a; color:#f1f5f9; border-color:#334155; }

/* Dark mode toggle button */
#dm-toggle {
    position:fixed; bottom:80px; right:24px; z-index:9999;
    width:48px; height:48px; border-radius:50%;
    background:linear-gradient(135deg,#1e293b,#334155);
    border:2px solid #475569; cursor:pointer;
    display:flex; align-items:center; justify-content:center;
    font-size:22px; box-shadow:0 4px 20px rgba(0,0,0,.3);
    transition:all .3s; user-select:none;
}
#dm-toggle:hover { transform:scale(1.12) rotate(15deg); box-shadow:0 6px 28px rgba(0,0,0,.4); }

/* ===== 8. BACK TO TOP BUTTON ===== */
#back-top {
    position:fixed; bottom:24px; right:24px; z-index:9999;
    width:48px; height:48px; border-radius:50%;
    background:linear-gradient(135deg,#EB001B,#FF5F00);
    border:none; cursor:pointer;
    display:flex; align-items:center; justify-content:center;
    font-size:20px; color:#fff;
    box-shadow:0 4px 20px rgba(235,0,27,.35);
    transition:all .3s; opacity:0; pointer-events:none;
    user-select:none;
}
#back-top.visible { opacity:1; pointer-events:all; }
#back-top:hover { transform:translateY(-4px) scale(1.08); box-shadow:0 8px 28px rgba(235,0,27,.5); }
</style>

<!-- Dark mode toggle -->
<div id="dm-toggle" title="Toggle Dark Mode">🌙</div>

<!-- Back to top -->
<div id="back-top" title="Back to top">↑</div>

<script>
(function(){

  /* ========== 1. CONFETTI BURST ========== */
  function launchConfetti(){
    var canvas=document.createElement('canvas');
    canvas.style.cssText='position:fixed;inset:0;z-index:99998;pointer-events:none;';
    canvas.width=window.innerWidth; canvas.height=window.innerHeight;
    document.body.appendChild(canvas);
    var ctx=canvas.getContext('2d');
    var colors=['#EB001B','#FF5F00','#F79E1B','#2563eb','#7c3aed','#059669','#ec4899','#fff','#facc15'];
    var pieces=[];
    for(var i=0;i<180;i++){
        pieces.push({
            x:Math.random()*canvas.width,
            y:Math.random()*canvas.height - canvas.height,
            w:Math.random()*14+5, h:Math.random()*7+3,
            color:colors[Math.floor(Math.random()*colors.length)],
            rot:Math.random()*360,
            vx:(Math.random()-.5)*6, vy:Math.random()*6+2,
            vr:(Math.random()-.5)*10
        });
    }
    var frame=0;
    function draw(){
        ctx.clearRect(0,0,canvas.width,canvas.height);
        pieces.forEach(function(p){
            ctx.save();
            ctx.translate(p.x+p.w/2, p.y+p.h/2);
            ctx.rotate(p.rot*Math.PI/180);
            ctx.fillStyle=p.color;
            ctx.globalAlpha=Math.max(0,1-frame/140);
            ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);
            ctx.restore();
            p.x+=p.vx; p.y+=p.vy; p.rot+=p.vr;
        });
        frame++;
        if(frame<160) requestAnimationFrame(draw);
        else canvas.remove();
    }
    draw();
  }
  var _st=window.sendToTeams, _se=window.sendToEmail;
  window.sendToTeams=function(){ launchConfetti(); _st&&_st.apply(this,arguments); };
  window.sendToEmail=function(){ launchConfetti(); _se&&_se.apply(this,arguments); };

  /* ========== 2. ANIMATED NUMBER COUNTERS ========== */
  function animateCounter(el,target){
    var start=null, dur=1400;
    function step(ts){
        if(!start) start=ts;
        var p=Math.min((ts-start)/dur,1);
        var ease=1-Math.pow(1-p,4);
        el.textContent=Math.floor(ease*target);
        if(p<1) requestAnimationFrame(step);
        else el.textContent=target;
    }
    requestAnimationFrame(step);
  }
  if('IntersectionObserver' in window){
    var obs=new IntersectionObserver(function(entries){
        entries.forEach(function(e){
            if(e.isIntersecting){
                var el=e.target, n=parseInt(el.textContent,10);
                if(!isNaN(n)) animateCounter(el,n);
                obs.unobserve(el);
            }
        });
    },{threshold:0.5});
    document.querySelectorAll('.wph-stat-num').forEach(function(el){ obs.observe(el); });
  }

  /* ========== 3. TAB SLIDE ANIMATION ========== */
  var tabOrder={crq:0,workflow:1,team:2};
  var currentTab='crq';
  var _sw=window.switchTab;
  window.switchTab=function(t){
    var fromIdx=tabOrder[currentTab], toIdx=tabOrder[t];
    currentTab=t;
    _sw&&_sw.apply(this,arguments);
    var page=document.getElementById('page-'+t);
    if(page){
        page.classList.remove('slide-left');
        void page.offsetWidth;
        if(toIdx<fromIdx) page.classList.add('slide-left');
    }
  };

  /* ========== 5. STEP COMPLETION CHECKMARK ANIMATION ========== */
  var _orig_activateStep=window.activateStep;
  window.activateStep=function(n){
    _orig_activateStep&&_orig_activateStep.apply(this,arguments);
    /* For each completed step, swap the number with animated SVG checkmark */
    setTimeout(function(){
        for(var i=1;i<n;i++){
            var numEl=document.querySelector('#step-'+i+' .step-num');
            if(numEl && !numEl.querySelector('svg')){
                numEl.innerHTML='<svg class="step-check-svg" width="22" height="22" viewBox="0 0 22 22" fill="none"><circle cx="11" cy="11" r="10" fill="#059669"/><path d="M6 11.5l3.5 3.5 6.5-7" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:40;stroke-dashoffset:40;animation:checkDraw 0.5s cubic-bezier(0.4,0,0.2,1) forwards;"/></svg>';
            }
        }
    },50);
  };

  /* ========== 6. TYPING EFFECT ON HERO BANNER ========== */
  var heroP=document.querySelector('#page-crq .hero-banner p');
  if(heroP){
    var fullText=heroP.textContent;
    heroP.textContent='';
    heroP.style.borderRight='2px solid rgba(255,255,255,.6)';
    var ci=0;
    function typeChar(){
        if(ci<=fullText.length){
            heroP.textContent=fullText.substring(0,ci);
            ci++;
            setTimeout(typeChar, ci<fullText.length ? 28 : 500);
        } else {
            heroP.style.borderRight='none';
        }
    }
    setTimeout(typeChar, 1800); /* start after loader fades */
  }

  /* ========== 7. DARK MODE TOGGLE ========== */
  var dmBtn=document.getElementById('dm-toggle');
  var dark=false;
  dmBtn.addEventListener('click',function(){
    dark=!dark;
    document.body.classList.toggle('dark-mode',dark);
    dmBtn.textContent=dark?'☀️':'🌙';
    try{ localStorage.setItem('crq_dark',dark?'1':'0'); }catch(e){}
  });
  try{
    if(localStorage.getItem('crq_dark')==='1'){
        dark=true;
        document.body.classList.add('dark-mode');
        dmBtn.textContent='☀️';
    }
  }catch(e){}

  /* ========== 8. BACK TO TOP ========== */
  var topBtn=document.getElementById('back-top');
  window.addEventListener('scroll',function(){
    topBtn.classList.toggle('visible', window.scrollY>300);
  });
  topBtn.addEventListener('click',function(){
    window.scrollTo({top:0,behavior:'smooth'});
  });

})();
</script>
"""

with open("CRQ_Companion_v3.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Inject loader right after <body>
html_content = html_content.replace("<body>", "<body>" + LOADER, 1)

# Inject all enhancements right before </body>
html_content = html_content.replace("</body>", EXTRA + "</body>", 1)

encoded = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
data_url = f"data:text/html;base64,{encoded}"
st.iframe(data_url, height=950)
