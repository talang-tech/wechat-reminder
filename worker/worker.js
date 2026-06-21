/**
 * 微信提醒 Cloudflare Worker 代理
 * 用于解决 GitHub Actions IP 不固定的问题
 */

// 企业微信配置（在 Cloudflare Worker 环境变量中设置）
// WECOM_CORPID: 企业 ID
// WECOM_CORPSECRET: 应用 Secret
// WECOM_AGENTID: 应用 AgentId
// AUTH_TOKEN: 自定义访问令牌（用于验证请求）

// 缓存 access_token
let accessTokenCache = {
  token: null,
  expires: 0
};

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  // 只允许 POST 请求
  if (request.method !== 'POST') {
    return jsonResponse({ error: 'Method not allowed' }, 405);
  }

  try {
    // 验证 auth token
    const authHeader = request.headers.get('Authorization');
    const expectedToken = AUTH_TOKEN;

    if (!expectedToken) {
      return jsonResponse({ error: 'Worker not configured: missing AUTH_TOKEN' }, 500);
    }

    if (!authHeader || authHeader !== `Bearer ${expectedToken}`) {
      return jsonResponse({ error: 'Unauthorized' }, 401);
    }

    // 解析请求
    const body = await request.json();
    const { title, content, touser } = body;

    if (!title || !content) {
      return jsonResponse({ error: 'Missing title or content' }, 400);
    }

    // 获取 access_token
    const accessToken = await getAccessToken();
    if (!accessToken) {
      return jsonResponse({ error: 'Failed to get access_token, check WECOM_CORPID/WECOM_CORPSECRET' }, 500);
    }

    // 发送消息
    const result = await sendMessage(accessToken, title, content, touser);

    if (result.errcode === 0) {
      return jsonResponse({ success: true, message: 'Message sent' });
    } else {
      return jsonResponse({ success: false, error: result }, 500);
    }

  } catch (error) {
    return jsonResponse({ error: error.message }, 500);
  }
}

async function getAccessToken() {
  const now = Date.now();

  // 返回缓存的 token
  if (accessTokenCache.token && now < accessTokenCache.expires - 60000) {
    return accessTokenCache.token;
  }

  const corpid = WECOM_CORPID;
  const corpsecret = WECOM_CORPSECRET;

  if (!corpid || !corpsecret) {
    return null;
  }

  const url = `https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${corpid}&corpsecret=${corpsecret}`;

  const response = await fetch(url);
  const data = await response.json();

  if (data.errcode === 0) {
    accessTokenCache = {
      token: data.access_token,
      expires: now + data.expires_in * 1000
    };
    return data.access_token;
  } else {
    console.error('Failed to get access_token:', data);
    return null;
  }
}

async function sendMessage(accessToken, title, content, touser) {
  const url = `https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${accessToken}`;

  const finalTouser = touser || WECOM_TOUSER || '@all';
  const agentid = parseInt(WECOM_AGENTID) || 1000002;

  const markdownContent = `### ${title}\n\n${content}`;

  const body = {
    touser: finalTouser,
    msgtype: 'markdown',
    agentid: agentid,
    markdown: {
      content: markdownContent
    }
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  return await response.json();
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}
