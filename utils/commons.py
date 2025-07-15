from utils.colors import Color
from utils.wechatutils import WechatUtils
import frida,sys
import platform


class Commons:
    def __init__(self):
        self.wechatutils_instance = WechatUtils()
        self.device = frida.get_local_device()
        self.process = self.device.enumerate_processes()
        self.pid = -1
        self.version_list = []
        self.configs_path = ""

    def onMessage(self, message, data):
        if message['type'] == 'send':
            print(Color.GREEN + message['payload'], Color.END)
        elif message['type'] == 'error':
            print(Color.RED + message['stack'], Color.END)

    def inject_wehcatEx(self, pid, code):
        session = frida.attach(pid)
        try:
            script = session.create_script(code)
            script.on("message", self.onMessage)
            script.load()
            print(Color.GREEN + "[+] 脚本已加载，按 Ctrl+C 退出..." + Color.END)
            sys.stdin.read()  # 等待用户输入
        except KeyboardInterrupt:
            print(Color.YELLOW + "\n[!] 接收到退出信号" + Color.END)
        finally:
            if session:
                session.detach()  # 确保会话被正确关闭

    def get_architecture_suffix(self):
        """获取系统架构后缀(x64或arm)"""
        machine = platform.machine()
        if 'arm' in machine.lower() or 'aarch64' in machine.lower():
            return 'arm'
        else:
            return 'x64'

    def load_wechatEx_configs(self):
        path = self.wechatutils_instance.get_configs_path()
        pid, version = self.wechatutils_instance.get_wechat_pid_and_version_mac()
        if pid and version is not None:
            # 根据架构选择配置文件
            arch_suffix = self.get_architecture_suffix()
            wehcatEx_hookcode = open(path + "../scripts/hook.js", "r", encoding="utf-8").read()
            wechatEx_addresses = open(path + f"../configs/address_{version}_{arch_suffix}.json").read()
            wehcatEx_hookcode = "var address=" + wechatEx_addresses + wehcatEx_hookcode
            self.inject_wehcatEx(pid, wehcatEx_hookcode)
        else:
            self.wechatutils_instance.print_process_not_found_message()

    def load_wechatEx_configs_pid(self, pid):
        path = self.wechatutils_instance.get_configs_path()
        version = self.wechatutils_instance.get_wechat_version_mac()
        if pid and version is not None:
            # 根据架构选择配置文件
            arch_suffix = self.get_architecture_suffix()
            wehcatEx_hookcode = open(path + "../scripts/hook.js", "r", encoding="utf-8").read()
            wechatEx_addresses = open(path + f"../configs/address_{version}_{arch_suffix}.json").read()
            wehcatEx_hookcode = "var address=" + wechatEx_addresses + wehcatEx_hookcode
            self.inject_wehcatEx(pid, wehcatEx_hookcode)
        else:
            self.wechatutils_instance.print_process_not_found_message()