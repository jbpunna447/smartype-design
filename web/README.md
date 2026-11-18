# SmarType website

The keyboard's website: Home, Privacy policy, Terms, Help and Contact. Static HTML and CSS, no framework.

- Build: `python3 web/tools/build.py` writes `web/site`. Edit `web/tools/build.py` (pages) and `web/tools/site.css`, never `web/site` by hand.
- Brand marks, favicons, illustrations and the store screenshots come from `design/assets`, so rebuild after changing those.
- Vercel serves `web/site` (root directory `web/site` in the website's Vercel project), published through the mirror to jbpunna447/smartype-design.
- The privacy policy and terms pages reflect how the app works today and are published for Google Play.
