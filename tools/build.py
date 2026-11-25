#!/usr/bin/env python3
"""Generates the static pages of the BMB Tech Firm site into ../public.
Edit the text below (or the HTML files directly), set DOMAIN, then run:  python3 tools/build.py
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'public')
DOMAIN = 'https://YOUR-DOMAIN.com'   # <-- change to your real address (used in sitemap.xml and robots.txt)
CUR = 'GHS'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- content
ICON = {
    'web': '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M8 20h8M12 16v4M9.5 8.5L8 10l1.5 1.5M14.5 8.5L16 10l-1.5 1.5"/>',
    'brand': '<path d="M12 3l7 8-7 10-7-10z"/><circle cx="12" cy="11" r="1.6"/><path d="M12 12.6V21"/>',
    'video': '<rect x="3" y="6" width="18" height="12" rx="1"/><path d="M10 9.5v5l4.5-2.5z"/>',
    'it': '<rect x="5" y="5" width="14" height="10" rx="1"/><path d="M2 19h20M9 10l2 2 4-4"/>',
    'cctv': '<path d="M3 7h13l4 3v4l-4 3H3z"/><circle cx="9" cy="12" r="2.5"/>',
    'network': '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/>',
    'marketing': '<path d="M3 10v4h4l8 5V5L7 10z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
    'software': '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>',
    'more': '<rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/><rect x="4" y="14" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/>',
}


def icon(k):
    return ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICON[k])


SERVICES = [
    dict(id='web', n='01', t='Website design & development', cat='Digital & creative', ic='web', badge=('POPULAR', 'y'),
         s='Business sites, portfolios and online shops.',
         b=['Business and portfolio websites', 'E-commerce websites', 'Website maintenance', 'Domain and hosting support']),
    dict(id='brand', n='02', t='Graphic design & branding', cat='Digital & creative', ic='brand',
         s='A look that makes your business memorable.',
         b=['Logo and brand identity design', 'Business cards and stationery', 'Flyers, posters and banners', 'Brochures and promotional materials']),
    dict(id='video', n='03', t='Multimedia & video editing', cat='Digital & creative', ic='video',
         s='Photo and video content that gets attention.',
         b=['Video and photo editing', 'Promotional videos', 'Motion graphics', 'Social media video content']),
    dict(id='it', n='04', t='Computer & IT support', cat='IT & infrastructure', ic='it',
         s='Fast help when your technology slows you down.',
         b=['Computer troubleshooting', 'Software installation', 'Hardware upgrades', 'Routine IT maintenance']),
    dict(id='cctv', n='05', t='CCTV & security systems', cat='IT & infrastructure', ic='cctv', badge=('SURVEY FIRST', 't'),
         s='Cameras and access control, installed properly.',
         b=['CCTV installation', 'Camera system maintenance', 'Video surveillance setup', 'Access control solutions']),
    dict(id='network', n='06', t='Networking services', cat='IT & infrastructure', ic='network',
         s='Wi-Fi and office networks that stay up.',
         b=['Wi-Fi installation and setup', 'Office network configuration', 'Router configuration', 'Network troubleshooting']),
    dict(id='marketing', n='07', t='Digital marketing', cat='Growth & software', ic='marketing',
         s='Plan, create and promote online.',
         b=['Social media account management', 'Content planning and creation', 'Online advertising support', 'Digital marketing strategy']),
    dict(id='software', n='08', t='Software & application development', cat='Growth & software', ic='software',
         s='Custom tools that fit how you work.',
         b=['Business software solutions', 'Mobile application development', 'Desktop applications', 'Workflow and task automation']),
]
MORE = [('Computer training', 'Practical digital skills and software training.'),
        ('Printing & photocopying', 'Documents and basic print services.'),
        ('Data recovery', 'Help recovering accessible files and information.'),
        ('IT consultancy', 'Guidance on technology choices and setup.'),
        ('Email setup', 'Business email configuration and support.'),
        ('Web hosting', 'Domain and hosting assistance.')]
MORE_IMAGES = {'Computer training': 'service-training.jpg', 'Printing & photocopying': 'service-printing.jpg',
               'Data recovery': 'service-data-recovery.jpg', 'IT consultancy': 'service-consultancy.jpg',
               'Email setup': 'service-email.jpg', 'Web hosting': 'service-hosting.jpg'}
SERVICE_IMAGES = {'web': 'service-web.jpg', 'brand': 'service-branding.jpg', 'video': 'service-video.jpg',
                  'it': 'service-it-support.jpg', 'cctv': 'service-cctv.jpg', 'network': 'service-networking.jpg',
                  'marketing': 'service-marketing.jpg', 'software': 'service-software.jpg'}
WHY = [('Practical solutions', 'Technology that fits how you actually work, without unnecessary complexity.'),
       ('Clear scope', 'We confirm the service, deliverables and timeline before work begins.'),
       ('Many services, one team', 'Websites, branding, video, IT, security and software from a single partner.'),
       ('Support after delivery', 'We complete the work, then discuss ongoing support.')]
AUD = [('Individuals', 'Personal websites, computer support and creative projects.', ['Personal websites', 'Computer support', 'Graphic design & video', 'Computer training']),
       ('Small businesses', 'Branding, websites, marketing and day-to-day IT.', ['Branding & stationery', 'Websites & e-commerce', 'Digital marketing', 'Email & hosting']),
       ('Schools & organisations', 'Networking, technical support and digital tools.', ['Networking & Wi-Fi', 'IT support', 'CCTV & access control', 'Software & automation'])]
ENG = [('Project-based', 'Defined scope, deliverables and timeline, for websites, branding, apps and installations.'),
       ('Ongoing support', 'Website maintenance, routine IT maintenance and camera system maintenance.'),
       ('Consultation', 'IT consultancy and guidance on technology choices and setup.')]
STEPS = [('Tell us what you need', 'Share your goal, challenge or project idea.'),
         ('Agree on the scope', 'Confirm the service, deliverables and timeline.'),
         ('Review the proposal', 'Discuss the plan and any applicable costs.'),
         ('Deliver & support', 'Complete the work and discuss ongoing support.')]
FAQ = [('Who do you work with?', 'Individuals, small businesses, and schools and organisations.'),
       ('What services do you offer?', 'Website design and development, graphic design and branding, video editing, IT support, CCTV and security, networking, digital marketing, and software and app development, plus training, printing, data recovery, IT consultancy, email setup and web hosting.'),
       ('How do we get started?', 'Tell us what you need. We then agree the scope, you review the proposal, and we deliver and discuss support.'),
       ('How is pricing handled?', 'Any applicable costs are discussed with you when you review the proposal, before work starts. Package prices on this site are starting points.'),
       ('Do you offer ongoing support?', 'Yes. After delivery we discuss ongoing support, including website, IT and camera system maintenance.'),
       ('I’m not sure what I need. Can you help?', 'Yes. Our IT consultancy gives guidance on technology choices and setup. You can book a consultation from the contact page.')]
# EXAMPLE PRICES: edit these before you publish.
PACKAGES = [
    dict(t='Starter Website', p='1,500', per='', ic='web', svc='Website design & development',
         b=['Up to 5 pages', 'Mobile-friendly design', 'Contact form and WhatsApp button', 'Domain and hosting setup help']),
    dict(t='Business Website', p='3,500', per='', ic='web', svc='Website design & development', badge=('MOST POPULAR', 'y'),
         b=['Up to 10 pages', 'Design matched to your brand', 'Optional online shop', 'Help updating your content']),
    dict(t='Brand Starter', p='800', per='', ic='brand', svc='Graphic design & branding',
         b=['Logo and brand identity', 'Business card design', 'One flyer or banner design']),
    dict(t='CCTV Installation', p='3,500', per='', ic='cctv', svc='CCTV & security systems', badge=('SURVEY FIRST', 't'),
         b=['Site survey, then a fixed quote', 'Camera installation and setup', 'Viewing on your phone', 'Maintenance available']),
    dict(t='Office Wi-Fi & Network', p='1,200', per='', ic='network', svc='Networking services',
         b=['Wi-Fi installation and setup', 'Router configuration', 'Network troubleshooting']),
    dict(t='IT Support Plan', p='500', per=' / month', ic='it', svc='Computer & IT support', badge=('MONTHLY', 'k'),
         b=['Routine IT maintenance', 'Computer troubleshooting', 'Software installation and updates']),
]

NAV = [('services.html', 'Services', 'services'), ('packages.html', 'Packages', 'packages'),
       ('portfolio.html', 'Portfolio', 'portfolio'), ('solutions.html', 'Solutions', 'solutions'),
       ('process.html', 'How we work', 'process')]
CATLINKS = [('Websites', 'services.html#web'), ('Branding', 'services.html#brand'), ('Video', 'services.html#video'),
            ('IT support', 'services.html#it'), ('CCTV', 'services.html#cctv'), ('Networking', 'services.html#network'),
            ('Marketing', 'services.html#marketing'), ('Software', 'services.html#software')]

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>'
SEARCH_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v15M6 13l6 6 6-6"/></svg>'


# ---------------------------------------------------------------- shared pieces
def topbar():
    def i(p):
        return '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % p
    return ('<div class="topbar"><div class="wrap">'
            '<span>%s Clear scope before work begins</span>'
            '<span>%s Quick answers on WhatsApp</span>'
            '<span>%s Support after delivery</span>'
            '<a href="contact.html#consultation">%s Book a consultation</a>'
            '</div></div>') % (i('<path d="M5 12l5 5 9-10"/>'), i('<path d="M21 12a8 8 0 0 1-12 7l-5 1 1-5a8 8 0 1 1 16-3z"/>'),
                               i('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'), i('<rect x="4" y="5" width="16" height="15"/><path d="M4 10h16M9 3v4M15 3v4"/>'))


def header(active):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if k == active else '', t) for h, t, k in NAV)
    cats = ''.join('<a href="%s">%s</a>' % (h, t) for t, h in CATLINKS) + '<a class="hot" href="contact.html#quote">Get a quote</a>'
    drawer = ''.join('<a class="dl" href="%s">%s</a>' % (h, t) for h, t, k in NAV) + \
        ''.join('<a class="dl" href="%s">%s</a>' % (h, t) for t, h in CATLINKS) + \
        '<form class="qf" role="search"><input class="qin" placeholder="Search services…" aria-label="Search services" autocomplete="off"><button class="qb" type="button" aria-label="Search">%s</button><div class="qr" hidden></div></form>' % SEARCH_SVG + \
        '<a class="btn" href="contact.html#quote">Get a quote</a>'
    return ('<header class="hd"><div class="hd1 wrap">'
            '<div class="hl"><button class="ib burger" id="bg" aria-label="Menu" aria-expanded="false" aria-controls="dr"><span></span><span></span><span></span></button><nav class="hn" aria-label="Main">%s</nav></div>'
            '<a class="logo" href="index.html" aria-label="BMB Tech Firm, home"><img src="assets/bmb-mark.png" alt="BMB" height="34"><span>Tech Firm</span></a>'
            '<div class="hr"><button class="ib" id="th" aria-label="Toggle light and dark theme"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 4a8 8 0 0 0 0 16z"/></svg></button>'
            '<a class="ib" data-wa aria-label="Chat on WhatsApp">%s</a><a class="btn sm" href="contact.html#quote">Get a quote</a></div></div>'
            '<div class="hd2"><div class="wrap"><nav class="hc" aria-label="Services">%s</nav>'
            '<form class="qf" role="search"><input class="qin" placeholder="Search services…" aria-label="Search services" autocomplete="off"><button class="qb" type="button" aria-label="Search">%s</button><div class="qr" hidden></div></form></div></div>'
            '<div class="drawer" id="dr" hidden>%s</div></header>') % (nav, WA_SVG, cats, SEARCH_SVG, drawer)


def footer():
    return ('<footer><div class="wrap"><div class="fg">'
            '<div><img class="flogo" src="assets/bmb-mark.png" alt="BMB Tech Firm"><p class="tag">Smart technology. Practical solutions.</p><a class="btn sm" href="contact.html#quote">Get a quote</a></div>'
            '<div><h4>Services</h4><a href="services.html#web">Websites &amp; design</a><a href="services.html#it">IT &amp; networking</a><a href="services.html#cctv">CCTV &amp; security</a><a href="services.html#software">Software &amp; marketing</a><a href="packages.html">Packages</a></div>'
            '<div><h4>Company</h4><a href="index.html">Home</a><a href="solutions.html">Solutions</a><a href="portfolio.html">Portfolio</a><a href="process.html">How we work</a><a href="contact.html">Contact</a></div>'
            '<div data-ctgroup><h4>Contact</h4>'
            '<div class="ctr"><a data-ct="whatsapp" href="#"></a></div><div class="ctr"><a data-ct="phone" href="#"></a></div>'
            '<div class="ctr"><a data-ct="email" href="#"></a></div><div class="ctr"><span data-ct="address"></span></div>'
            '<p class="ct-none">Use the <a href="contact.html" style="display:inline;text-decoration:underline">contact form</a> and we will reply.</p>'
            '<a href="contact.html#support">Request IT support</a><a href="contact.html#survey">Request a site survey</a></div>'
            '</div><div class="cr"><span>© 2026 BMB Tech Firm</span><a href="#top">Back to top ↑</a></div></div></footer>'
            '<a class="wafab" data-wa="Hello BMB Tech Firm, I would like to know more about your services." aria-label="Chat on WhatsApp">%s<span>Chat</span></a>') % WA_SVG


def cta(h='Let’s build something', p='Tell us your goal, challenge or project idea and we’ll agree the scope with you.', btn='Get in touch', href='contact.html#quote'):
    return '<section class="cta"><div class="wrap rv"><h2>%s</h2><p>%s</p><a class="btn" href="%s">%s →</a></div></section>' % (h, p, href, btn)


def page(fn, title, desc, active, body, schema=None):
    ld = ''.join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False) for s in (schema or []))
    doc = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<title>%s</title>\n<meta name="description" content="%s">\n'
           '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:type" content="website"><meta property="og:site_name" content="BMB Tech Firm">\n'
           '<meta name="theme-color" content="#111111">\n'
           '<meta name="google-site-verification" content="T5hwgGoe7ivBJZnzHj7hSd4D3R1VaDBqhXe4ufpOLjc" />\n'
           '<link rel="manifest" href="/manifest.json">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
           '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">\n'
           '<link rel="stylesheet" href="assets/style.css">\n'
           '<script>try{var t=localStorage.getItem("bmb-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}</script>\n%s</head>\n'
           '<body id="top">\n%s\n%s\n<main>\n%s\n</main>\n%s\n'
           '<script src="assets/site-data.js"></script><script src="assets/search-index.js"></script><script src="assets/app.js"></script>\n</body>\n</html>\n'
           ) % (esc(title), esc(desc), esc(title), esc(desc), ld, topbar(), header(active), body, footer())
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(doc)


def hero_sm(eb, h1, lead):
    return '<section class="hero sm"><div class="wrap"><span class="eb">%s</span><h1>%s</h1><p>%s</p></div></section>' % (eb, h1, lead)


def service_photo(filename):
    return '<img class="service-photo" src="assets/%s" alt="" aria-hidden="true" loading="lazy" decoding="async">' % filename

def service_card(s, detailed=False):
    badge = '<span class="badge %s">%s</span>' % (s['badge'][1], s['badge'][0]) if s.get('badge') else ''
    link = '<a class="lk" href="contact.html?service=%s#quote">Request this service →</a>' % esc(s['t'].replace(' ', '%20').replace('&', '%26'))
    if detailed:
        lis = ''.join('<li>%s</li>' % esc(x) for x in s['b'])
        return ('<article class="pc" id="%s">%s<span class="num">%s</span><div class="im">%s</div><div class="tx"><h3>%s</h3><p>%s</p><ul>%s</ul>%s</div></article>'
                % (s['id'], badge, s['n'], service_photo(SERVICE_IMAGES[s['id']]), esc(s['t']), esc(s['s']), lis, link))
    return ('<a class="pc ctr" href="services.html#%s">%s<div class="im">%s</div><div class="tx"><h3>%s</h3><p>%s</p></div></a>'
            % (s['id'], badge, service_photo(SERVICE_IMAGES[s['id']]), esc(s['t']), esc(s['s'])))


def package_card(p):
    badge = '<span class="badge %s">%s</span>' % (p['badge'][1], p['badge'][0]) if p.get('badge') else ''
    lis = ''.join('<li>%s</li>' % esc(x) for x in p['b'])
    href = 'contact.html?service=%s#quote' % p['svc'].replace(' ', '%20').replace('&', '%26')
    return ('<article class="pc ctr">%s<div class="im">%s</div><div class="tx"><h3>%s</h3><p class="pr">From <b>%s %s</b>%s</p><ul>%s</ul>'
            '<a class="lk" href="%s">Choose this package →</a></div></article>'
            % (badge, icon(p['ic']), esc(p['t']), CUR, p['p'], p['per'], lis, esc(href)))


def faq(items):
    return '<div class="fq">%s</div>' % ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', esc(q), esc(a)) for i, (q, a) in enumerate(items))


def steps():
    return '<div class="steps">%s</div>' % ''.join('<div class="stp"><i>0%d</i><h3>%s</h3><p>%s</p></div>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(STEPS))


def audience():
    return '<div class="cols c3">%s</div>' % ''.join(
        '<div class="col"><b>0%d</b><h3>%s</h3><p>%s</p><ul>%s</ul></div>' % (i + 1, esc(t), esc(d), ''.join('<li>%s</li>' % esc(x) for x in b))
        for i, (t, d, b) in enumerate(AUD))


def projects_blocks():
    return ('<section class="sec" id="proj-home" hidden><div class="wrap rv"><div class="sh"><h2>Recent work</h2><a class="more" href="portfolio.html">View portfolio →</a></div><div class="cards"></div></div></section>'
            '<section class="sec g" id="tm" hidden><div class="wrap rv"><div class="sh"><h2>What clients say</h2></div><div class="tms"></div></div></section>')


# ---------------------------------------------------------------- pages
def build():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)

    # search index
    idx = [dict(t=s['t'], u='services.html#' + s['id'], c=s['cat'], k=' '.join(s['b'])) for s in SERVICES]
    idx += [dict(t=t, u='services.html#more', c='Additional services', k=d) for t, d in MORE]
    idx += [dict(t=p['t'], u='packages.html', c='Package from %s %s' % (CUR, p['p']), k=' '.join(p['b'])) for p in PACKAGES]
    idx += [dict(t='Book a consultation', u='contact.html#consultation', c='Contact', k='appointment meeting advice'),
            dict(t='Request a site survey', u='contact.html#survey', c='Contact', k='cctv wifi installation visit'),
            dict(t='Request IT support', u='contact.html#support', c='Contact', k='problem repair help fix')]
    with open(os.path.join(OUT, 'assets', 'search-index.js'), 'w', encoding='utf-8') as f:
        f.write('window.SEARCH=%s;\n' % json.dumps(idx, ensure_ascii=False))

    offers = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['t'], "description": s['s']}} for s in SERVICES]
    biz = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "BMB Tech Firm",
           "description": "Website design, branding, video, IT support, CCTV, networking, digital marketing and software development.",
           "slogan": "Smart technology. Practical solutions.", "areaServed": "Ghana",
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": offers}}

    # ---- home
    cards = ''.join(service_card(s) for s in SERVICES)
    pk = ''.join(package_card(p) for p in PACKAGES[:3])
    why = '<div class="cols">%s</div>' % ''.join('<div class="col"><b>0%d</b><h3>%s</h3><p>%s</p></div>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(WHY))
    body = ('<section class="hero"><div class="wrap"><span class="eb">Smart technology. Practical solutions.</span>'
            '<h1>Technology that moves business <em>forward.</em></h1>'
            '<p>BMB Tech Firm supports people and organisations with practical digital, creative and IT services.</p>'
            '<a class="btn" href="services.html">Discover services</a></div><a class="down" href="#services" aria-label="Scroll down">%s</a></section>'
            '<section class="sec" id="services"><div class="wrap rv"><div class="sh"><h2>Our services</h2><a class="more" href="services.html">Discover all services →</a></div><div class="cards">%s</div></div></section>'
            '<section class="sec g"><div class="wrap rv"><div class="sh"><div><h2>Popular packages</h2><p>Clear starting prices. We confirm the final scope with you before work begins.</p></div><a class="more" href="packages.html">See all packages →</a></div><div class="cards c3">%s</div></div></section>'
            '<section class="sec"><div class="wrap rv"><div class="sh"><h2>Why BMB Tech Firm</h2></div>%s</div></section>'
            '<section class="sec g"><div class="wrap rv"><div class="sh"><h2>Who we serve</h2><a class="more" href="solutions.html">Our solutions →</a></div>%s</div></section>'
            '%s'
            '<section class="sec"><div class="wrap rv"><div class="sh"><h2>How we work</h2><a class="more" href="process.html">Learn more →</a></div>%s</div></section>'
            '<section class="sec g"><div class="wrap rv"><div class="sh"><h2>Questions, answered</h2></div>%s</div></section>'
            '%s') % (ARROW, cards, pk, why, audience(), projects_blocks(), steps(), faq(FAQ[:4]), cta())
    page('index.html', 'BMB Tech Firm | Technology that moves business forward',
         'BMB Tech Firm: website design, branding, video, IT support, CCTV, networking, digital marketing and software development.',
         'home', body, [biz])

    # ---- services
    cats = []
    for c in ['Digital & creative', 'IT & infrastructure', 'Growth & software']:
        cs = ''.join(service_card(s, True) for s in SERVICES if s['cat'] == c)
        cats.append('<section class="sec%s"><div class="wrap rv"><div class="sh"><h2>%s</h2></div><div class="cards c3">%s</div></div></section>' % (' g' if len(cats) % 2 else '', c, cs))
    more = ''.join('<div class="pc"><div class="im">%s</div><div class="tx"><h3>%s</h3><p>%s</p><a class="lk" href="contact.html?service=Additional%%20services#quote">Ask about this →</a></div></div>' % (service_photo(MORE_IMAGES[t]), esc(t), esc(d)) for t, d in MORE)
    body = (hero_sm('Our services', 'Digital, creative <em>&amp; IT services</em>', 'From websites and branding to networks and software: practical help that keeps your business moving.')
            + ''.join(cats)
            + '<section class="sec" id="more"><div class="wrap rv"><div class="sh"><h2>Additional services</h2></div><div class="cards c3">%s</div></div></section>' % more
            + cta('Not sure what you need?', 'Book a short consultation and we will guide you on technology choices and setup.', 'Book a consultation', 'contact.html#consultation'))
    page('services.html', 'Services | BMB Tech Firm', 'Website design, graphic design and branding, video editing, IT support, CCTV, networking, digital marketing and software development.', 'services', body)

    # ---- packages
    body = (hero_sm('Packages', 'Clear prices, <em>clear scope</em>', 'Starting points for the most requested services. We confirm the final scope and cost with you before work begins.')
            + '<section class="sec"><div class="wrap rv"><div class="cards c3">%s</div><p class="note">Prices are “from” prices in %s and may change with the size of the project. Every request starts with a conversation about what you need.</p></div></section>' % (''.join(package_card(p) for p in PACKAGES), CUR)
            + cta('Need something different?', 'Tell us what you have in mind and we will put together a proposal.', 'Request a custom quote'))
    page('packages.html', 'Packages and starting prices | BMB Tech Firm', 'Starting prices for websites, branding, CCTV installation, office networking and IT support from BMB Tech Firm.', 'packages', body)

    # ---- portfolio
    body = (hero_sm('Portfolio', 'Work we are <em>proud of</em>', 'A look at recent websites, designs, installations and software projects.')
            + '<section class="sec"><div class="wrap rv"><div class="cards c3" id="proj-grid"></div>'
              '<div class="empty" id="proj-empty"><h3>Projects coming soon</h3><p>We are adding our recent work here. Have a project in mind? Let’s make it the next one.</p><a class="btn k" href="contact.html#quote">Start a project →</a></div></div></section>'
            + '<section class="sec g" id="cl" hidden><div class="wrap rv"><div class="sh"><h2>Trusted by</h2></div><div class="cl"></div></div></section>'
            + '<section class="sec" id="tm" hidden><div class="wrap rv"><div class="sh"><h2>What clients say</h2></div><div class="tms"></div></div></section>'
            + cta())
    page('portfolio.html', 'Portfolio | BMB Tech Firm', 'Recent websites, branding, installations and software projects by BMB Tech Firm.', 'portfolio', body)

    # ---- solutions
    eng = '<div class="cols c3">%s</div>' % ''.join('<div class="col"><b>0%d</b><h3>%s</h3><p>%s</p></div>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(ENG))
    body = (hero_sm('Solutions', 'Built around <em>who you are</em>', 'Whether you’re an individual, a growing business or a school, we match the right services to your needs.')
            + '<section class="sec"><div class="wrap rv">%s</div></section>' % audience()
            + '<section class="sec g"><div class="wrap rv"><div class="sh"><h2>Flexible engagement</h2></div>%s</div></section>' % eng
            + cta('Not sure what you need?', 'Our IT consultancy gives guidance on technology choices and setup.', 'Talk to us', 'contact.html#consultation'))
    page('solutions.html', 'Solutions for individuals, businesses and schools | BMB Tech Firm', 'Technology solutions for individuals, small businesses, schools and organisations, delivered project by project or as ongoing support.', 'solutions', body)

    # ---- process
    fq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = (hero_sm('How we work', 'A simple way <em>to get started</em>', 'Four clear steps from your first message to delivery and ongoing support.')
            + '<section class="sec"><div class="wrap rv">%s</div></section>' % steps()
            + '<section class="sec g"><div class="wrap rv"><div class="sh"><h2>Questions, answered</h2></div>%s</div></section>' % faq(FAQ)
            + cta())
    page('process.html', 'How we work and FAQ | BMB Tech Firm', 'How BMB Tech Firm works: tell us what you need, agree the scope, review the proposal, then delivery and support. Plus answers to common questions.', 'process', body, [fq])

    # ---- contact
    def fld(label, inner):
        return '<label class="fld"><span>%s</span>%s</label>' % (label, inner)

    def sel(name, lst, ph, req=False):
        return '<select name="%s" data-list="%s" data-ph="%s"%s></select>' % (name, lst, ph, ' required' if req else '')

    def wrapf(typ, intro_h, intro_p, fields, wa_label='Send via WhatsApp only'):
        return ('<div class="fp" data-p="%s" hidden><form class="fm" data-type="%s"><h2>%s</h2><p class="lead">%s</p>%s'
                '<input class="ps" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
                '<label class="chkr" data-needwa><input type="checkbox" class="bw" checked> Also send this to us on WhatsApp</label>'
                '<button class="btn k" type="submit">Send request</button><div class="or" data-needwa>or</div>'
                '<button class="btn wa waonly" type="button" data-needwa>%s%s</button><div class="ok" role="status"></div></form></div>'
                % (typ, typ, intro_h, intro_p, fields, WA_SVG, wa_label))

    name_phone = '<div class="row2">%s%s</div>' % (fld('Your name', '<input required name="name" maxlength="100" autocomplete="name">'),
                                                    fld('Phone / WhatsApp', '<input type="tel" name="phone" maxlength="25" autocomplete="tel" placeholder="e.g. 024 000 0000">'))
    email = fld('Email address', '<input type="email" name="email" maxlength="150" autocomplete="email">')
    quote = wrapf('quote', 'Get a quote', 'Tell us about your goal or project. Costs are discussed when you review the proposal.',
                  name_phone + email + '<div class="row2">%s%s</div>' % (fld('Service', sel('service', 'service', 'Select a service')), fld('Estimated budget', sel('budget', 'budget', 'Select your budget')))
                  + fld('Tell us about your project', '<textarea required name="message" rows="4" maxlength="3000"></textarea>'))
    consult = wrapf('consultation', 'Book a consultation', 'Pick a day and time that suits you. We will confirm by WhatsApp, phone or email.',
                    name_phone + email + '<div class="row2">%s%s</div>' % (fld('Topic', sel('service', 'service', 'What is it about?')), fld('How should we talk?', sel('mode', 'mode', 'Choose', True)))
                    + '<div class="row2">%s%s</div>' % (fld('Preferred date', '<input required type="date" name="date">'), fld('Preferred time', sel('slot', 'slot', 'Choose', True)))
                    + fld('Anything we should know? (optional)', '<textarea name="message" rows="3" maxlength="3000"></textarea>'), 'Book via WhatsApp only')
    survey = wrapf('survey', 'Request a site survey', 'For CCTV, Wi-Fi and network projects we visit first, then give you a fixed quote. You can send photos of the area on WhatsApp.',
                   name_phone + email + '<div class="row2">%s%s</div>' % (fld('What do you need?', sel('service', 'survey', 'Choose', True)), fld('Type of property', sel('property', 'property', 'Choose')))
                   + fld('Location of the site', '<input required name="location" maxlength="200" placeholder="Area / town and a landmark">')
                   + '<div class="row2">%s%s</div>' % (fld('Size (rooms, cameras, points)', '<input name="quantity" maxlength="60" placeholder="e.g. 6 rooms, about 8 cameras">'), fld('Preferred visit date', '<input type="date" name="date">'))
                   + fld('Notes (optional)', '<textarea name="message" rows="3" maxlength="3000"></textarea>'), 'Send photos on WhatsApp')
    support = wrapf('support', 'Request IT support', 'Already a client or just need help? Describe the problem and we will get back to you.',
                    name_phone + email + '<div class="row2">%s%s</div>' % (fld('What needs help?', sel('service', 'issue', 'Choose', True)), fld('How urgent is it?', sel('urgency', 'urgency', 'Choose')))
                    + fld('Describe the problem', '<textarea required name="message" rows="4" maxlength="3000"></textarea>'), 'Message us on WhatsApp')
    side = ('<aside class="side" data-ctgroup><h3>Talk to us directly</h3><p>Prefer to chat? WhatsApp is the fastest way to reach us.</p>'
            '<a class="btn wa" data-wa style="width:100%%">%s Chat on WhatsApp</a><div style="height:18px"></div>'
            '<div class="ctr"><b>Phone</b><a data-ct="phone" href="#"></a></div><div class="ctr"><b>Email</b><a data-ct="email" href="#"></a></div>'
            '<div class="ctr"><b>Address</b><span data-ct="address"></span></div></aside>') % WA_SVG
    tabs = ''.join('<button class="ft" role="tab" data-t="%s" aria-selected="false">%s</button>' % (k, l)
                   for k, l in [('quote', 'Get a quote'), ('consultation', 'Book a consultation'), ('survey', 'Site survey'), ('support', 'IT support')])
    body = (hero_sm('Contact', 'Smart technology. <em>Practical solutions.</em>', 'Tell us what you need and we’ll reply with next steps.')
            + '<section class="sec"><div class="wrap"><div class="ftabs" role="tablist">%s</div><div class="cgrid"><div>%s%s%s%s</div>%s</div></div></section>'
            % (tabs, quote, consult, survey, support, side))
    page('contact.html', 'Contact, quotes and bookings | BMB Tech Firm', 'Get a quote, book a consultation, request a site survey or ask for IT support from BMB Tech Firm.', 'contact', body)

    # ---- sitemap + robots
    urls = ['index.html', 'services.html', 'packages.html', 'portfolio.html', 'solutions.html', 'process.html', 'contact.html']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % ''.join(
        '  <url><loc>%s/%s</loc></url>\n' % (DOMAIN, '' if u == 'index.html' else u) for u in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8').write('User-agent: *\nAllow: /\nDisallow: /admin.html\nDisallow: /api/\n\nSitemap: %s/sitemap.xml\n' % DOMAIN)
    print('built', len(urls), 'pages')


if __name__ == '__main__':
    build()


