wrk.method = "POST"
wrk.body   = '{"text":"test"}'
wrk.headers["Content-Type"] = "application/json"

-- wrk -t12 -c400 -d30s -s wrk_post.lua http://localhost:80/notes
