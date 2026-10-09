/*
  Request filter for Maldives National Debt Clock.
  Runs on Cloudflare Pages in front of every request.

  The site is open to everyone. Only the files visitors need are served:
  scripts, raw inputs, logs, the README and workflow files return "Not found".
*/

const PUBLIC = [
  /^\/$/,
  /^\/[a-z0-9_-]+(\.html)?$/i,                                   // pages, with or without .html
  /^\/(data|budget|revenue|priorities|population)\.json$/,       // data the pages read
  /^\/assets\/[\w.-]+$/,
  /^\/downloads\/[\w.-]+$/,
  /^\/budget-detail\/\d{4}\.json$/,                               // line-by-line figures for earlier weeks
  /^\/robots\.txt$/,
];
const isPublic = path => PUBLIC.some(re => re.test(path));

export async function onRequest(context) {
  const { request, next } = context;
  if (!isPublic(new URL(request.url).pathname)) {
    return new Response("Not found", { status: 404, headers: { "Content-Type": "text/plain", "Cache-Control": "no-store" } });
  }
  return next();
}
