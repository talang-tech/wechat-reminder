/**
 * 微信提醒 Cloudflare Worker
 * 功能：
 * 1. 企业微信回调校验（解锁可信IP限制）
 * 2. 企业微信 API 代理（绕过IP白名单）
 * 3. 消息发送接口
 */

// 环境变量（在 Cloudflare Worker Settings → Variables 中配置）：
// WECOM_CORPID: 企业 ID
// WECOM_CORPSECRET: 应用 Secret
// WECOM_AGENTID: 应用 AgentId (如 1000002)
// WECOM_TOUSER: 默认接收人 UserId (如 Admin)
// AUTH_TOKEN: 自定义访问令牌（用于验证请求）
// WECOM_TOKEN: 回调 Token（与企业微信后台配置一致，可选）
// WECOM_AES_KEY: 回调 EncodingAESKey（可选）

// 缓存 access_token
let tokenCache = {
  token: null,
  expires: 0
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // ========== 1. 企业微信回调校验 ==========
    if (url.pathname === "/wework/callback" || url.pathname === "/callback") {
      // GET 请求：校验回调 URL
      if (request.method === "GET") {
        const echostr = url.searchParams.get("echostr");
        console.log("收到回调校验请求，echostr:", echostr);
        return new Response(echostr ?? "", {
          headers: { "Content-Type": "text/plain" }
        });
      }
      // POST 请求：接收消息（暂不处理，返回空）
      return new Response("success");
    }

    // ========== 2. 消息发送接口 ==========
    if (url.pathname === "/send" || url.pathname === "/api/send") {
      return handleSendMessage(request, env);
    }

    // ========== 3. 企业微信 API 代理 ==========
    // 将所有 /cgi-bin/* 请求转发到企业微信 API
    if (url.pathname.startsWith("/cgi-bin/")) {
      return proxyWecomAPI(request, url);
    }

    // ========== 4. 健康检查 ==========
    if (url.pathname === "/" || url.pathname === "/health") {
      return new Response(JSON.stringify({
        status: "ok",
        service: "wechat-reminder-proxy",
        endpoints: {
          callback: "/wework/callback",
          send: "/send",
          proxy: "/cgi-bin/*"
        }
      }), {
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response("Not Found", { status: 404 });
  }
};

/**
 * 处理发送消息请求
 */
async function handleSendMessage(request, env) {
  if (request.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  try {
    // 验证 token
    const authHeader = request.headers.get("Authorization");
    const expectedToken = env.AUTH_TOKEN;

    if (expectedToken && (!authHeader || authHeader !== `Bearer ${expectedToken}`)) {
      return jsonResponse({ error: "Unauthorized" }, 401);
    }

    // 解析请求
    const body = await request.json();
    const { title, content, touser } = body;

    if (!title || !content) {
      return jsonResponse({ error: "Missing title or content" }, 400);
    }

    // 获取 access_token
    const accessToken = await getAccessToken(env);
    if (!accessToken) {
      return jsonResponse({ error: "Failed to get access_token" }, 500);
    }

    // 发送消息
    const result = await sendMarkdownMessage(accessToken, title, content, touser || env.WECOM_TOUSER, env);

    if (result.errcode === 0) {
      return jsonResponse({ success: true, message: "Message sent" });
    } else {
      console.error("Send message failed:", result);
      return jsonResponse({ success: false, error: result }, 500);
    }

  } catch (error) {
    console.error("Error:", error);
    return jsonResponse({ error: error.message }, 500);
  }
}

/**
 * 获取 access_token（带缓存）
 */
async function getAccessToken(env) {
  const now = Date.now();

  if (tokenCache.token && now < tokenCache.expires - 60000) {
    return tokenCache.token;
  }

  const corpid = env.WECOM_CORPID;
  const corpsecret = env.WECOM_CORPSECRET;

  if (!corpid || !corpsecret) {
    console.error("Missing WECOM_CORPID or WECOM_CORPSECRET");
    return null;
  }

  const tokenUrl = `https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${corpid}&corpsecret=${corpsecret}`;

  const response = await fetch(tokenUrl);
  const data = await response.json();

  if (data.errcode === 0) {
    tokenCache = {
      token: data.access_token,
      expires: now + data.expires_in * 1000
    };
    return data.access_token;
  } else {
    console.error("Failed to get access_token:", data);
    return null;
  }
}

/**
 * 发送 Markdown 消息
 */
async function sendMarkdownMessage(accessToken, title, content, touser, env) {
  const url = `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accessToken}`;

  const agentid = parseInt(env.WECOM_AGENTID) || 1000002;
  const finalTouser = touser || "@all";

  const markdownContent = `### ${title}\n\n${content}`;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      touser: finalTouser,
      msgtype: "markdown",
      agentid: agentid,
      markdown: {
        content: markdownContent
      }
    })
  });

  return await response.json();
}

/**
 * 代理企业微信 API 请求
 */
async function proxyWecomAPI(request, url) {
  const targetUrl = new URL(url.pathname + url.search, "https://qyapi.weixin.qq.com");

  const newHeaders = new Headers(request.headers);
  newHeaders.set("Host", "qyapi.weixin.qq.com");

  const proxyReq = new Request(targetUrl, {
    method: request.method,
    headers: newHeaders,
    body: request.body,
    redirect: "follow"
  });

  return fetch(proxyReq);
}

/**
 * JSON 响应
 */
function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}
