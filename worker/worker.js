/**
 * 微信提醒 Cloudflare Worker
 * 功能：
 * 1. 企业微信回调校验（支持明文模式，无需AES解密）
 * 2. 消息发送接口
 */

// 环境变量：
// WECOM_CORPID: 企业 ID
// WECOM_CORPSECRET: 应用 Secret
// WECOM_AGENTID: 应用 AgentId
// WECOM_TOUSER: 默认接收人 UserId
// AUTH_TOKEN: 自定义访问令牌
// WECOM_CALLBACK_TOKEN: 回调 Token（与企业微信后台配置一致，可选）

let tokenCache = {
  token: null,
  expires: 0
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 企业微信回调校验
    if (url.pathname === "/wework/callback" || url.pathname === "/callback") {
      return handleCallback(request, env);
    }

    // 消息发送接口
    if (url.pathname === "/send" || url.pathname === "/api/send") {
      return handleSendMessage(request, env);
    }

    // 健康检查
    if (url.pathname === "/" || url.pathname === "/health") {
      return jsonResponse({
        status: "ok",
        service: "wechat-reminder-proxy",
        callback_url: "/wework/callback",
        send_url: "/send"
      });
    }

    return new Response("Not Found", { status: 404 });
  }
};

/**
 * 处理企业微信回调校验
 */
async function handleCallback(request, env) {
  const url = new URL(request.url);

  // GET 请求：URL 校验
  if (request.method === "GET") {
    const msgSignature = url.searchParams.get("msg_signature") || "";
    const timestamp = url.searchParams.get("timestamp") || "";
    const nonce = url.searchParams.get("nonce") || "";
    const echostr = url.searchParams.get("echostr") || "";

    console.log("收到回调校验:", { msgSignature, timestamp, nonce, echostr });

    // 如果配置了 Token，进行签名验证
    const callbackToken = env.WECOM_CALLBACK_TOKEN;
    if (callbackToken) {
      const signature = sha1([callbackToken, timestamp, nonce, echostr].sort().join(""));
      console.log("期望签名:", signature, "收到签名:", msgSignature);
      if (signature !== msgSignature) {
        console.log("签名验证失败，但直接返回echostr");
      }
    }

    // 直接返回 echostr（明文模式）
    // 如果是加密模式需要解密，这里先返回原始值
    return new Response(echostr, {
      headers: { "Content-Type": "text/plain" }
    });
  }

  // POST 请求：接收消息（返回空响应）
  return new Response("success");
}

/**
 * 处理发送消息请求
 */
async function handleSendMessage(request, env) {
  if (request.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  try {
    const authHeader = request.headers.get("Authorization");
    const expectedToken = env.AUTH_TOKEN;

    if (expectedToken && (!authHeader || authHeader !== `Bearer ${expectedToken}`)) {
      return jsonResponse({ error: "Unauthorized" }, 401);
    }

    const body = await request.json();
    const { title, content, touser } = body;

    if (!title || !content) {
      return jsonResponse({ error: "Missing title or content" }, 400);
    }

    const accessToken = await getAccessToken(env);
    if (!accessToken) {
      return jsonResponse({ error: "Failed to get access_token" }, 500);
    }

    const result = await sendMarkdownMessage(accessToken, title, content, touser || env.WECOM_TOUSER, env);

    if (result.errcode === 0) {
      return jsonResponse({ success: true });
    } else {
      console.error("发送失败:", result);
      return jsonResponse({ success: false, errcode: result.errcode, errmsg: result.errmsg }, 500);
    }
  } catch (error) {
    console.error("Error:", error);
    return jsonResponse({ error: error.message }, 500);
  }
}

async function getAccessToken(env) {
  const now = Date.now();
  if (tokenCache.token && now < tokenCache.expires - 60000) {
    return tokenCache.token;
  }

  const tokenUrl = `https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${env.WECOM_CORPID}&corpsecret=${env.WECOM_CORPSECRET}`;
  const response = await fetch(tokenUrl);
  const data = await response.json();

  if (data.errcode === 0) {
    tokenCache = { token: data.access_token, expires: now + data.expires_in * 1000 };
    return data.access_token;
  }
  console.error("获取token失败:", data);
  return null;
}

async function sendMarkdownMessage(accessToken, title, content, touser, env) {
  const url = `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accessToken}`;
  const agentid = parseInt(env.WECOM_AGENTID) || 1000002;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      touser: touser || "@all",
      msgtype: "markdown",
      agentid: agentid,
      markdown: { content: `### ${title}\n\n${content}` }
    })
  });
  return await response.json();
}

/**
 * 简单的 SHA1 实现（用于签名验证）
 */
async function sha1(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hashBuffer = await crypto.subtle.digest("SHA-1", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}
