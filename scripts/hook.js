// 获取 WeChatAppEx.exe 的基址
var module = Process.findModuleByName('WeChatAppEx Framework');
var base = module.base;

send("[+] WeChatAppEx 注入成功!");
send("[+] 等待小程序加载...");

// 延迟执行主逻辑
setImmediate(() => {
    // 修改 "devTools" 为 "DevTools"
    let devToolString = base.add(address.DevToolStringAddr);
    let oldDevToolString = devToolString.readCString();
    if (oldDevToolString === "devTools") {
        Memory.protect(devToolString, 8, 'rw-');
        devToolString.writeUtf8String("DevTools");
        Memory.protect(devToolString, 8, 'r--');
    }

    // 修改小程序调试页面 URL
    let devToolsPageString = base.add(address.WechatWebStringAddr);
    let devToolsPageStringVal = devToolsPageString.readCString();
    if (devToolsPageStringVal === "https://applet-debug.com/devtools/wechat_app.html") {
        Memory.protect(devToolsPageString, 0x20, 'rw-');
        devToolsPageString.writeUtf8String("https://applet-debug.com/devtools/wechat_web.html");
        Memory.protect(devToolsPageString, 0x20, 'r--');
    }

    // Hook json_get_bool 函数，拦截 enable_vconsole
    Interceptor.attach(base.add(address.JsonGetBoolFunc), {
        onEnter(args) {
            this.name = args[1].readCString();
        },
        onLeave(retval) {
            if (this.name === "enable_vconsole") {
                retval.replace(1);
            }
        }
    });

    // Hook xweb 地址函数，直接返回 true
    Interceptor.attach(base.add(address.xwebadress), {
        onLeave(retval) {
            retval.replace(1);
        }
    });
});
