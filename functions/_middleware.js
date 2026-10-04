/*
  Private preview gate for Maldives National Debt Clock.
  Runs on Cloudflare Pages in front of every request.

  Visitors enter a 4-digit code once. Each code works one time only, then that
  device stays unlocked. Codes are stored here only as salted SHA-256 hashes.

  Settings (Cloudflare Pages > Settings > Variables and Secrets):
    LOCKED          "true" keeps the site private. Any other value opens it to everyone.
    SESSION_SECRET  a long random string used to sign the unlock cookie.
  Binding (Cloudflare Pages > Settings > Bindings):
    CODES_KV        a KV namespace that records used codes and failed attempts.
*/

const SALT = "2c930bc38a800aad2f39886075fb5188";
const CODE_HASHES = new Set([
  "94b4600906cba160778ed59629ad38f0951b4280f59a605a791834de0e43c2b7",
  "6fdc464eb5685663b9e34964d8c7b339a2cd287aa73362cebea2d00a5033873f",
  "a84e000944971b4ac099645a150628642401fc08cb17744d3c8d2a7b2e6c6654",
  "e8a45b0daca2f3ff864246c0ed74c92a450b78664b638c795d60cf6bfdd90ad6",
  "440a604584e2a239fc7c92b9ffdf7306ef34e97a1d2c27585f7a659f09a87a9b",
  "143958c928fb855b634aec30234e62e0e4480cad1ac20d5b652b1f4399c30bfd",
  "b96f44aa3c7c983aa484d1f31f2c829b3e66fc6244f337960a10e8167b76de5d",
  "11083ccfe59098e8c805b0011255569d41a8a6ab9ab3ad4e6005030a74a8591f",
  "6991ad46f4792501a320a26d7c4d47e9c03d5f5ca16e3088cb4282f9cec9120a",
  "31440439f35ac50517e432bd99499a2e435c6898bd6d3dea85e80603b5bd9d96",
  "9b30b05f9ca5d4ab0096104943a6defeaf8ee6f2d40a434f18ade27d7f31131e",
  "91c2aae4a1169f86ae5b02c4f92b53e1e5ed4c79dfffdccbef7937c137491bfa",
  "17b75ff0fbdb3f18c64de86331b14ec15d5c29b06d1c35fd4119fd6b903e1330",
  "92b3871fc86c4b664c1b04530eb0ab635184a3310ea76e291becdbe6672255e3",
  "bf3e672831dba47919b7afec2d90169be6ccd97b94cd9bb4169f40c4f5407721",
  "f20e7814251872bc8f960c16276440acb4b9f679b48cf835251bc7f052a80729",
  "d74d7d07ec359978c33e3bf65b367ac567bf09bba1692682ab674648c62ce635",
  "41ca629e7470295bd977850a164aabb2614361ce30c490d83ca79b12514e335d",
  "9de4805a912c2a497c5f979ce6a1608128225fc2f76a20472ba41995c9d06b7a",
  "4ff6d6e2b9d0c799c52d51c66d8b19818739e0c2740590abf85725be4359c772",
  "c4ab531702c9380ca96c36338809a1a9fe36f6ac9166d21012df5e332107075a",
  "bbd84f37bf0dfe2f0469a4a2e56ea84cc4f47a8fcf46fcaeebb7b795cd53fa65",
  "1f49f3de8301d02859f6ce8b02a9f25eff2f834a661e7f99336a1e3ce5cdb28c",
  "07e93775af7dabd1d8cfae95ae41401967bc0ebd7aadaa7f24a008cc2b67caca",
  "a5a3b04f7e6e450a222a2c29d6b8a645f78c55512dd68d0e969ee0dff0c0f41d",
  "c350aa97e4bbe5169820d0c54ebcadaee2e9dc202d2945b6540ff02cb24a95ee",
  "4616166731de80eae59ec8609050fd257c84be96f10ba92d1d85b4ef00a7d89a",
  "6ed142d7bda9f3fc2a77dd80b69b8af83a290cd5c1cd6b5eccf9fd063770e677",
  "e09c83b79c5ee029f789c589e792222cb8525990c2ca86d119fd192017c2f43e",
  "7202881265428803bb3ec99a7846c974acc4ea9b2f8987dd80b07b4eebd24935",
  "92f0a76203247bf9e05a967120cc99043f4f7d7b13df79cdcb7fe12388eac48f",
  "91a992e1cbe0bf342de40f6fd9dd24e9f02f8eb048e5b1275cc1065c1175d309",
  "58d2f26ac6c52b43b44b03fa3de3ea80d55f6afa4d92606b4c8381ecff4105f4",
  "9131f81660d835f63900085ac549b6cb749593e272a02f5f36ac1c7558269564",
  "951a6fedb5850ae465595eae3174e0ae46ce845fb4dffa7499560740f2642c30",
  "0c11bf46003708490608d4c4490e84a9ebcd3e4ef63bed47f677c53e46e355af",
  "7652617e125ef7e013c4f3deb7dce8666e84616ccade2f8d8ee8747384b75cbd",
  "87d39d570ee1a376ba9b43e91eebc636b5170c501ff98b929a57bd66882b9ddc",
  "be8574ec827619e88fb2889c1839f6e855c168da3d63e39bbbf3038b95453ca3",
  "d398e1e43587006cbdce5d0f0d211d079ed3198ebd5ae05bc408fd1767023452",
  "063632a9f34ac19dcc9a5f3a97d6c5b5d7946e06df282ecaf0aeb946447cd48c",
  "a9d27d087f5ca3188d33a0c9aa61ceee4ef3d6f409fad8b03d757c84d87f93ea",
  "21b3fa52ec0b3383f0c78c3da20c010cd319723128d29d562f56be5ea0aa2399",
  "2ba174cb5df6ceab298890400f8e590560595b09aea1640a5ac0628ff716633c",
  "2c543bb8de76289c53f4c9cb86007a7a96c13ab3fec29e05e12f5f9fc0e7f522",
  "76901fdf776734212b24385d2b90856e5ad4b1283046ebc7a99fc54aeb342160",
  "80dc3ada8f084adde8f046e62563853b05c10c2868f9f58fbce41c714c31222e",
  "5137665d5e9f0977bf6ad9cd123535458fa0410b51d8e8d78b1138e62c5a1384",
  "e0b9ba62a0c6f08b5ce71a13bf404edd335b94296436003791243853163d2b7c",
  "851463d8bac375fabc3222a556cfde58a31be2df23da1bfdfc3d89d46db94b0c"
]);
const COOKIE = "mvdc_pass";
const MAX_TRIES = 8;          // wrong codes allowed per connection
const LOCKOUT_SECONDS = 1800; // before trying again

const enc = new TextEncoder();
const hex = buf => [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
const sha256 = async s => hex(await crypto.subtle.digest("SHA-256", enc.encode(s)));
async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, enc.encode(msg)));
}
function readCookie(request, name) {
  for (const part of (request.headers.get("Cookie") || "").split(/;\s*/)) {
    const i = part.indexOf("=");
    if (i > 0 && part.slice(0, i) === name) return part.slice(i + 1);
  }
  return null;
}
async function validPass(token, secret) {
  if (!token) return false;
  const cut = token.lastIndexOf(".");
  if (cut < 1) return false;
  const body = token.slice(0, cut), sig = token.slice(cut + 1), expect = await hmac(secret, body);
  if (sig.length !== expect.length) return false;
  let diff = 0;
  for (let i = 0; i < sig.length; i++) diff |= sig.charCodeAt(i) ^ expect.charCodeAt(i);
  return diff === 0;
}

export async function onRequest(context) {
  const { request, env, next } = context;
  if (String(env.LOCKED || "").trim().toLowerCase() !== "true") return next();
  try {
    if (!env.SESSION_SECRET || !env.CODES_KV) return gate("The site is being set up. Please try again shortly.", 503);
    const url = new URL(request.url);
    if (url.pathname === "/robots.txt") return new Response("User-agent: *\nDisallow: /\n", { headers: { "Content-Type": "text/plain" } });
    if (await validPass(readCookie(request, COOKIE), env.SESSION_SECRET)) {
      const res = await next(), out = new Response(res.body, res);
      out.headers.set("X-Robots-Tag", "noindex, nofollow");
      return out;
    }
    if (url.pathname === "/__unlock" && request.method === "POST") return unlock(request, env);
    if ((request.headers.get("Accept") || "").includes("text/html")) return gate("", 200);
    return new Response("Locked", { status: 401, headers: { "Cache-Control": "no-store" } });
  } catch (err) {
    return gate("Something went wrong. Please try again in a minute.", 500);
  }
}

async function unlock(request, env) {
  const ip = request.headers.get("CF-Connecting-IP") || "unknown", triesKey = "tries:" + ip;
  const tries = parseInt((await env.CODES_KV.get(triesKey)) || "0", 10);
  if (tries >= MAX_TRIES) return gate("Too many attempts. Please wait 30 minutes and try again.", 429);
  const form = await request.formData();
  const code = String(form.get("code") || "").replace(/\D/g, "");
  const hash = await sha256(SALT + code);
  if (code.length !== 4 || !CODE_HASHES.has(hash)) {
    await env.CODES_KV.put(triesKey, String(tries + 1), { expirationTtl: LOCKOUT_SECONDS });
    const left = MAX_TRIES - tries - 1;
    return gate(left > 0 ? `That code isn't valid. Please check it and try again (${left} ${left === 1 ? "try" : "tries"} left).` : "Too many attempts. Please wait 30 minutes and try again.", 401);
  }
  const usedKey = "used:" + hash;
  if (await env.CODES_KV.get(usedKey)) return gate("That code has already been used. Each code works once, so please ask for a new one.", 403);
  await env.CODES_KV.put(usedKey, new Date().toISOString());
  const body = "v1." + Date.now() + "." + hash.slice(0, 10);
  const token = body + "." + (await hmac(env.SESSION_SECRET, body));
  return new Response(null, {
    status: 303,
    headers: { "Location": "/", "Cache-Control": "no-store", "Set-Cookie": `${COOKIE}=${token}; Path=/; Max-Age=34560000; HttpOnly; Secure; SameSite=Lax` },
  });
}

function gate(message, status) {
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#072f40">
<title>Maldives National Debt Clock</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌊</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,700..800&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; } html, body { margin: 0; height: 100%; }
  body { font-family: "Atkinson Hyperlegible", "Segoe UI", Roboto, Arial, sans-serif; color: #fff; background: linear-gradient(to bottom, #d7ecef 0 30%, #3fb8b0 30%, #0b4f6c 45%, #072f40 100%); display: grid; place-items: center; padding: 1.25rem; }
  .box { width: 100%; max-width: 24rem; background: rgba(7,47,64,.92); border-radius: 12px; padding: 2rem 1.6rem; box-shadow: 0 20px 60px rgba(0,0,0,.35); text-align: center; }
  .brand { font-family: "Archivo", "Arial Narrow", Arial, sans-serif; font-weight: 800; font-variation-settings: "wdth" 80; font-size: 1.15rem; }
  .brand span { color: #f4c95d; }
  h1 { font-family: "Archivo", "Arial Narrow", Arial, sans-serif; font-weight: 800; font-variation-settings: "wdth" 75; font-size: 1.9rem; margin: 1.2rem 0 .5rem; line-height: 1.1; }
  p { color: #a9cdd6; margin: 0 0 1.4rem; line-height: 1.5; }
  input { width: 100%; font: 700 2rem "Atkinson Hyperlegible", Arial, sans-serif; letter-spacing: .6em; text-align: center; padding: .7rem .2rem .7rem .8rem; border-radius: 8px; border: 2px solid transparent; background: #fff; color: #072f40; }
  input:focus { outline: none; border-color: #f4c95d; }
  button { margin-top: 1rem; width: 100%; font: 700 1rem "Atkinson Hyperlegible", Arial, sans-serif; background: #f4c95d; color: #072f40; border: 0; border-radius: 8px; padding: .9rem; cursor: pointer; }
  .msg { min-height: 1.4em; margin: 1rem 0 0; color: #ff8a6b; font-size: .95rem; }
</style></head>
<body><main class="box">
  <div class="brand">MV <span>Debt Clock</span></div>
  <h1>Private preview</h1>
  <p>This site isn't public yet. Enter the 4-digit code you were given to continue. You only need to do this once on each device.</p>
  <form method="post" action="/__unlock" autocomplete="off">
    <input name="code" inputmode="numeric" pattern="[0-9]{4}" maxlength="4" autocomplete="one-time-code" aria-label="4-digit code" required autofocus>
    <button type="submit">Enter</button>
  </form>
  <div class="msg" role="alert">${message}</div>
</main></body></html>`;
  return new Response(html, { status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
}
