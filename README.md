# Nexora Technologies website (Netlify)

A multi-page static site (`public/`) plus two Netlify Functions for requests and the admin page.

## Pages
`index`, `services`, `packages`, `portfolio`, `solutions`, `process` (how we work + FAQ) and `contact` (quote, consultation booking, site survey, IT support). `admin.html` is the private enquiries page.

## Deploy to Netlify
1. Push this folder to Git and import it in Netlify (settings are read from `netlify.toml`), or use `netlify deploy --prod`.
   Drag-and-drop deploys do not build functions, so use Git or the CLI.
2. In Netlify go to Site configuration > Environment variables and add the values from `.env.example`
   (SMTP_*, MAIL_TO, ADMIN_TOKEN and, optionally, WHATSAPP_*). Redeploy afterwards.

## Things to edit before launch
1. **`public/assets/site-data.js`**: your WhatsApp number (digits with country code, e.g. `233201234567`), phone, email, address, plus your portfolio projects, testimonials and client names. Empty lists simply hide those sections.
2. **Package prices**: the six prices on the packages page are examples. Change them in `tools/build.py` (the `PACKAGES` list) and run `python3 tools/build.py`, or search for `GHS` in `public/packages.html` and `public/index.html`.
3. **`DOMAIN`** at the top of `tools/build.py`: set your real address, then run the build again. It is used in `sitemap.xml` and `robots.txt`. After deploying, submit the sitemap in Google Search Console.
4. **Photos**: replace `public/assets/bg-team.jpg` and `bg-office.jpg` with licensed or free photos (about 1600px wide, under 250 KB).

`python3 tools/build.py` regenerates the HTML pages (and the search index) from the text in that file. You can also edit the HTML files directly.

## Requests: email and WhatsApp
Each form (quote, consultation, site survey, support) posts to `/api/contact`, which validates it, saves it (Netlify Blobs) and emails it to `MAIL_TO`. If the visitor ticks "Also send this to us on WhatsApp", WhatsApp opens with the message ready to send. Optional automatic WhatsApp alerts use the `WHATSAPP_*` variables (create an approved template with 5 variables: name, email or phone, request type and service, budget or details, message).

## Admin page
Open `/admin.html` and enter your `ADMIN_TOKEN`. You can search enquiries, filter by type or status, call or WhatsApp the client, and mark items as done. The page is hidden from search engines.

## Offline and install
`sw.js` saves the pages for offline use. Together with your existing `manifest.json` and icons, phones can install the site as an app.

## Local development
`npm install`, `npm install -g netlify-cli`, then `netlify dev`.
